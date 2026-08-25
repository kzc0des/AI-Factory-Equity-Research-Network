import os
import time
from dotenv import load_dotenv

# Load local environment variables (.env)
load_dotenv()

from src.agents.graph import build_parent_graph
from src.agents.ingestion import SEED_LIST

def main():
    print("=" * 60)
    print("🚀 AI Factory Growth Equity Identification Pipeline 🚀")
    print("=" * 60)
    
    demo_mode = os.environ.get("DEMO_MODE", "True").strip().lower() == "true"
    colab_tunnel = os.environ.get("COLAB_TUNNEL_URL", "")
    
    print(f"Execution Mode: {'DEMO/OFFLINE' if demo_mode else 'LIVE'}")
    if colab_tunnel:
        print(f"Colab Tunnel URL configured: {colab_tunnel}")
        print("Routing Moat and Growth analysis queries to your custom Colab model...")
    else:
        print("No Colab Tunnel URL set. Falling back to default APIs/Caches.")
        
    print(f"\nIngesting seed list of target companies...")
    
    # Initialize state
    initial_state = {
        "seed_list": SEED_LIST,
        "profiles": [],
        "top_20": []
    }
    
    # Compile graph
    print("Compiling LangGraph pipeline...")
    graph = build_parent_graph().compile()
    
    # Run pipeline
    print("Running pipeline (Map-Reduce)... This might take a moment...")
    start_time = time.time()
    
    result = graph.invoke(initial_state)
    
    elapsed = time.time() - start_time
    print(f"\nPipeline finished in {elapsed:.2f} seconds.")
    
    top_20 = result.get("top_20", [])
    print(f"\n🏆 Top {len(top_20)} AI Factory Growth Equity Targets:")
    print("-" * 60)
    for rank, profile in enumerate(top_20, 1):
        print(
            f"{rank:02d}. {profile.company_name} ({profile.ticker}) "
            f"- Score: {profile.total_score:.1f} "
            f"(Moat: {profile.moat_score or 0.0}, Growth: {profile.growth_cagr or 0.0}%)"
        )
    print("-" * 60)
    
    report_path = os.path.join("output", "report.md")
    if os.path.exists(report_path):
        print(f"Success! Report generated at: {report_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
