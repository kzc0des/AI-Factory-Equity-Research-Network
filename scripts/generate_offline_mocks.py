import os
import json

companies_data = [
    {
        "ticker": "NVDA",
        "company_name": "NVIDIA Corporation",
        "ai_factory_role": "Compute",
        "moat_score": 5.0,
        "growth_cagr": 45.0,
        "backlog_growth": 150,
        "cagr_range": "40% - 50%",
        "risks": ["cyclicality", "customer concentration"]
    },
    {
        "ticker": "AMD",
        "company_name": "Advanced Micro Devices, Inc.",
        "ai_factory_role": "Compute",
        "moat_score": 3.75,
        "growth_cagr": 30.0,
        "backlog_growth": 80,
        "cagr_range": "25% - 35%",
        "risks": ["execution", "cyclicality"]
    },
    {
        "ticker": "SMCI",
        "company_name": "Super Micro Computer, Inc.",
        "ai_factory_role": "Compute",
        "moat_score": 2.5,
        "growth_cagr": 35.0,
        "backlog_growth": 120,
        "cagr_range": "30% - 40%",
        "risks": ["execution", "customer concentration"]
    },
    {
        "ticker": "DELL",
        "company_name": "Dell Technologies Inc.",
        "ai_factory_role": "Compute",
        "moat_score": 2.5,
        "growth_cagr": 15.0,
        "backlog_growth": 45,
        "cagr_range": "12% - 18%",
        "risks": ["execution"]
    },
    {
        "ticker": "HPE",
        "company_name": "Hewlett Packard Enterprise",
        "ai_factory_role": "Compute",
        "moat_score": 2.5,
        "growth_cagr": 12.0,
        "backlog_growth": 35,
        "cagr_range": "10% - 14%",
        "risks": ["execution"]
    },
    {
        "ticker": "ANET",
        "company_name": "Arista Networks, Inc.",
        "ai_factory_role": "Networking",
        "moat_score": 3.75,
        "growth_cagr": 25.0,
        "backlog_growth": 60,
        "cagr_range": "22% - 28%",
        "risks": ["customer concentration"]
    },
    {
        "ticker": "AVGO",
        "company_name": "Broadcom Inc.",
        "ai_factory_role": "Networking",
        "moat_score": 5.0,
        "growth_cagr": 22.0,
        "backlog_growth": 50,
        "cagr_range": "20% - 24%",
        "risks": ["execution", "cyclicality"]
    },
    {
        "ticker": "LITE",
        "company_name": "Lumentum Holdings Inc.",
        "ai_factory_role": "Networking",
        "moat_score": 2.5,
        "growth_cagr": 18.0,
        "backlog_growth": 40,
        "cagr_range": "15% - 21%",
        "risks": ["customer concentration", "cyclicality"]
    },
    {
        "ticker": "COHR",
        "company_name": "Coherent Corp.",
        "ai_factory_role": "Networking",
        "moat_score": 2.5,
        "growth_cagr": 16.0,
        "backlog_growth": 30,
        "cagr_range": "14% - 18%",
        "risks": ["execution"]
    },
    {
        "ticker": "CEG",
        "company_name": "Constellation Energy Corporation",
        "ai_factory_role": "Power",
        "moat_score": 3.75,
        "growth_cagr": 20.0,
        "backlog_growth": 70,
        "cagr_range": "18% - 22%",
        "risks": ["cyclicality"]
    },
    {
        "ticker": "VST",
        "company_name": "Vistra Corp.",
        "ai_factory_role": "Power",
        "moat_score": 3.75,
        "growth_cagr": 28.0,
        "backlog_growth": 90,
        "cagr_range": "25% - 31%",
        "risks": ["cyclicality"]
    },
    {
        "ticker": "GE",
        "company_name": "General Electric Company",
        "ai_factory_role": "Power",
        "moat_score": 2.5,
        "growth_cagr": 10.0,
        "backlog_growth": 25,
        "cagr_range": "8% - 12%",
        "risks": ["execution"]
    },
    {
        "ticker": "ETN",
        "company_name": "Eaton Corporation plc",
        "ai_factory_role": "Power",
        "moat_score": 3.75,
        "growth_cagr": 14.0,
        "backlog_growth": 55,
        "cagr_range": "12% - 16%",
        "risks": ["cyclicality"]
    },
    {
        "ticker": "VRT",
        "company_name": "Vertiv Holdings Co.",
        "ai_factory_role": "Cooling",
        "moat_score": 5.0,
        "growth_cagr": 26.0,
        "backlog_growth": 85,
        "cagr_range": "24% - 28%",
        "risks": ["execution", "customer concentration"]
    },
    {
        "ticker": "MOD",
        "company_name": "Modine Manufacturing Company",
        "ai_factory_role": "Cooling",
        "moat_score": 2.5,
        "growth_cagr": 15.0,
        "backlog_growth": 40,
        "cagr_range": "13% - 17%",
        "risks": ["execution"]
    },
    {
        "ticker": "AAON",
        "company_name": "AAON, Inc.",
        "ai_factory_role": "Cooling",
        "moat_score": 2.5,
        "growth_cagr": 13.0,
        "backlog_growth": 35,
        "cagr_range": "11% - 15%",
        "risks": ["execution"]
    },
    {
        "ticker": "ACM",
        "company_name": "AECOM",
        "ai_factory_role": "Construction",
        "moat_score": 1.25,
        "growth_cagr": 8.0,
        "backlog_growth": 20,
        "cagr_range": "6% - 10%",
        "risks": ["execution"]
    },
    {
        "ticker": "J",
        "company_name": "Jacobs Solutions Inc.",
        "ai_factory_role": "Construction",
        "moat_score": 1.25,
        "growth_cagr": 9.0,
        "backlog_growth": 22,
        "cagr_range": "7% - 11%",
        "risks": ["execution"]
    },
    {
        "ticker": "EME",
        "company_name": "EMCOR Group, Inc.",
        "ai_factory_role": "Construction",
        "moat_score": 2.5,
        "growth_cagr": 11.0,
        "backlog_growth": 28,
        "cagr_range": "9% - 13%",
        "risks": ["cyclicality"]
    },
    {
        "ticker": "PWR",
        "company_name": "Quanta Services, Inc.",
        "ai_factory_role": "Construction",
        "moat_score": 2.5,
        "growth_cagr": 12.0,
        "backlog_growth": 32,
        "cagr_range": "10% - 14%",
        "risks": ["execution"]
    }
]

def main():
    transcripts_dir = os.path.join("data", "transcripts")
    llm_cache_dir = os.path.join("data", "llm_cache")
    
    os.makedirs(transcripts_dir, exist_ok=True)
    os.makedirs(llm_cache_dir, exist_ok=True)
    
    for comp in companies_data:
        ticker = comp["ticker"]
        # 1. Generate transcript
        transcript_content = (
            f"Recent 10-K and Earnings Call Transcript for {ticker}:\n\n"
            f"Management Guidance Summary:\n"
            f"- Demand environment: Strong, driven by AI Factory and hyperscale data center builds.\n"
            f"- Backlog: Stated backlog has grown by {comp['backlog_growth']}% year-over-year.\n"
            f"- Capacity: Committing capital expenditure to expand production/service capacity.\n"
            f"- 3-Year Outlook: Management guides/expects revenue to grow at a 3-year CAGR of {comp['growth_cagr']}% "
            f"(midpoint of {comp['cagr_range']}%).\n"
        )
        
        transcript_path = os.path.join(transcripts_dir, f"{ticker}.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_content)
        print(f"Generated transcript: {transcript_path}")
        
        # 2. Generate LLM cache JSON
        cache_json = {
            "ticker": ticker,
            "company_name": comp["company_name"],
            "ai_factory_role": comp["ai_factory_role"],
            "is_hyperscaler": False,
            "moat_score": comp["moat_score"],
            "growth_cagr": comp["growth_cagr"],
            "risks": comp["risks"]
        }
        
        cache_path = os.path.join(llm_cache_dir, f"{ticker}.json")
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache_json, f, indent=2)
        print(f"Generated LLM cache: {cache_path}")

if __name__ == "__main__":
    main()
