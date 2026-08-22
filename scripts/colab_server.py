import os
import json
import uuid
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Try importing FastAPI/Uvicorn/Transformers
try:
    from fastapi import FastAPI, Request  # type: ignore
    from fastapi.middleware.cors import CORSMiddleware  # type: ignore
    import uvicorn  # type: ignore
    import torch  # type: ignore
    from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore
except ImportError:
    # Fallback placeholders so writing/linting passes locally if not installed
    class DummyFastAPI:
        def __init__(self, *args, **kwargs):
            pass
        def add_middleware(self, *args, **kwargs):
            pass
        def post(self, *args, **kwargs):
            return lambda func: func

    FastAPI = DummyFastAPI  # type: ignore
    Request = Any  # type: ignore
    CORSMiddleware = Any  # type: ignore
    uvicorn = Any  # type: ignore
    torch = Any  # type: ignore
    AutoModelForCausalLM = Any  # type: ignore
    AutoTokenizer = Any  # type: ignore



app = FastAPI(title="Colab Custom Model Inference Server", version="1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and tokenizer
model = None
tokenizer = None

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1024
    tools: Optional[List[Dict[str, Any]]] = None

def load_model_and_tokenizer(model_path: str):
    global model, tokenizer
    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    # Configure model loading for GPU
    if torch.cuda.is_available():
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="cpu"
        )
    print("Model loaded successfully.")

def extract_json_block(text: str) -> str:
    """
    Extracts the JSON substring out of raw text.
    """
    text = text.strip()
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        return text[first_brace:last_brace+1]
    return text

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    global model, tokenizer
    if model is None or tokenizer is None:
        return {"error": "Model not loaded yet."}
        
    messages_list = [{"role": m.role, "content": m.content} for m in req.messages]
    
    # Extract structural constraints if tools are present
    has_tools = req.tools is not None and len(req.tools) > 0
    target_tool = None
    
    if has_tools:
        target_tool = req.tools[0]
        schema = target_tool["function"]["parameters"]
        # Append target JSON Schema instruction to the user's prompt
        if messages_list and messages_list[-1]["role"] == "user":
            messages_list[-1]["content"] += (
                f"\n\nReturn ONLY a JSON object matching this schema:\n"
                f"{json.dumps(schema, indent=2)}\n"
                f"Do not include any explanation or markdown code wrappers."
            )
        else:
            messages_list.append({
                "role": "user",
                "content": (
                    f"Return ONLY a JSON object matching this schema:\n"
                    f"{json.dumps(schema, indent=2)}\n"
                    f"Do not include any explanation or markdown code wrappers."
                )
            })

            
    # Format chat using model's chat template
    text = tokenizer.apply_chat_template(
        messages_list,
        tokenize=False,
        add_generation_prompt=True
    )
    
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    # Generate completion
    with torch.no_grad():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature if req.temperature > 0 else 0.01,
            do_sample=req.temperature > 0
        )
        
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    # Map generated response back to OpenAI structure
    if has_tools and target_tool:
        json_content = extract_json_block(generated_text)
        tool_call_id = f"call_{uuid.uuid4().hex[:12]}"
        
        choices = [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tool_call_id,
                            "type": "function",
                            "function": {
                                "name": target_tool["function"]["name"],
                                "arguments": json_content
                            }
                        }
                    ]
                },
                "finish_reason": "tool_calls"
            }
        ]
    else:
        choices = [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": generated_text.strip()
                },
                "finish_reason": "stop"
            }
        ]
        
    return {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": choices
    }

def run_server(model_path: str, port: int = 8000):
    load_model_and_tokenizer(model_path)
    print(f"Starting API Server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Colab API Server")
    parser.add_argument("--model", type=str, required=True, help="Path/name of HF model")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind server")
    args = parser.parse_args()
    
    run_server(args.model, args.port)
