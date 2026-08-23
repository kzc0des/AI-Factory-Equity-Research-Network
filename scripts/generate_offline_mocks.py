import os
import json

companies_data = [
    # Hyperscalers
    {
        "ticker": "MSFT",
        "company_name": "Microsoft Corporation",
        "ai_factory_role": None,
        "is_hyperscaler": True,
        "margin_value": 44.6,
    },
    {
        "ticker": "GOOGL",
        "company_name": "Alphabet Inc.",
        "ai_factory_role": None,
        "is_hyperscaler": True,
        "margin_value": 29.4,
    },
    {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "ai_factory_role": None,
        "is_hyperscaler": True,
        "margin_value": 30.2,
    },
    {
        "ticker": "AMZN",
        "company_name": "Amazon.com, Inc.",
        "ai_factory_role": None,
        "is_hyperscaler": True,
        "margin_value": 9.8,
    },
    {
        "ticker": "META",
        "company_name": "Meta Platforms, Inc.",
        "ai_factory_role": None,
        "is_hyperscaler": True,
        "margin_value": 41.2,
    },
    {
        "ticker": "ORCL",
        "company_name": "Oracle Corporation",
        "ai_factory_role": None,
        "is_hyperscaler": True,
        "margin_value": 28.5,
    },
    # Compute / Servers
    {
        "ticker": "NVDA",
        "company_name": "NVIDIA Corporation",
        "ai_factory_role": "Compute",
        "moat_score": 5.0,
        "growth_cagr": 45.0,
        "backlog_growth": 150,
        "cagr_range": "40% - 50%",
        "risks": ["cyclicality", "customer concentration"],
        "margin_value": 65.596
    },
    {
        "ticker": "AMD",
        "company_name": "Advanced Micro Devices, Inc.",
        "ai_factory_role": "Compute",
        "moat_score": 3.75,
        "growth_cagr": 30.0,
        "backlog_growth": 80,
        "cagr_range": "25% - 35%",
        "risks": ["execution", "cyclicality"],
        "margin_value": 17.25
    },
    {
        "ticker": "SMCI",
        "company_name": "Super Micro Computer, Inc.",
        "ai_factory_role": "Compute",
        "moat_score": 2.5,
        "growth_cagr": 35.0,
        "backlog_growth": 120,
        "cagr_range": "30% - 40%",
        "risks": ["execution", "customer concentration"],
        "margin_value": 13.382
    },
    {
        "ticker": "DELL",
        "company_name": "Dell Technologies Inc.",
        "ai_factory_role": "Compute",
        "moat_score": 2.5,
        "growth_cagr": 15.0,
        "backlog_growth": 45,
        "cagr_range": "12% - 18%",
        "risks": ["execution"],
        "margin_value": 8.857
    },
    {
        "ticker": "HPE",
        "company_name": "Hewlett Packard Enterprise",
        "ai_factory_role": "Compute",
        "moat_score": 2.5,
        "growth_cagr": 12.0,
        "backlog_growth": 35,
        "cagr_range": "10% - 14%",
        "risks": ["execution"],
        "margin_value": 8.7
    },
    {
        "ticker": "INTC",
        "company_name": "Intel Corporation",
        "ai_factory_role": "Compute",
        "moat_score": 1.25,
        "growth_cagr": 5.0,
        "backlog_growth": 10,
        "cagr_range": "3% - 7%",
        "risks": ["execution", "cyclicality"],
        "margin_value": 3.5
    },
    {
        "ticker": "MU",
        "company_name": "Micron Technology, Inc.",
        "ai_factory_role": "Compute",
        "moat_score": 3.75,
        "growth_cagr": 25.0,
        "backlog_growth": 90,
        "cagr_range": "20% - 30%",
        "risks": ["cyclicality", "execution"],
        "margin_value": 15.5
    },
    {
        "ticker": "WDC",
        "company_name": "Western Digital Corporation",
        "ai_factory_role": "Compute",
        "moat_score": 2.5,
        "growth_cagr": 18.0,
        "backlog_growth": 50,
        "cagr_range": "15% - 21%",
        "risks": ["cyclicality"],
        "margin_value": 9.2
    },
    {
        "ticker": "STX",
        "company_name": "Seagate Technology Holdings plc",
        "ai_factory_role": "Compute",
        "moat_score": 2.5,
        "growth_cagr": 16.0,
        "backlog_growth": 40,
        "cagr_range": "13% - 19%",
        "risks": ["cyclicality"],
        "margin_value": 8.5
    },
    # Networking
    {
        "ticker": "ANET",
        "company_name": "Arista Networks, Inc.",
        "ai_factory_role": "Networking",
        "moat_score": 5.0,
        "growth_cagr": 25.0,
        "backlog_growth": 60,
        "cagr_range": "22% - 28%",
        "risks": ["customer concentration"],
        "margin_value": 45.393
    },
    {
        "ticker": "AVGO",
        "company_name": "Broadcom Inc.",
        "ai_factory_role": "Networking",
        "moat_score": 5.0,
        "growth_cagr": 22.0,
        "backlog_growth": 50,
        "cagr_range": "20% - 24%",
        "risks": ["execution", "cyclicality"],
        "margin_value": 48.988
    },
    {
        "ticker": "LITE",
        "company_name": "Lumentum Holdings Inc.",
        "ai_factory_role": "Networking",
        "moat_score": 2.5,
        "growth_cagr": 18.0,
        "backlog_growth": 40,
        "cagr_range": "15% - 21%",
        "risks": ["customer concentration", "cyclicality"],
        "margin_value": 28.292
    },
    {
        "ticker": "COHR",
        "company_name": "Coherent Corp.",
        "ai_factory_role": "Networking",
        "moat_score": 2.5,
        "growth_cagr": 16.0,
        "backlog_growth": 30,
        "cagr_range": "14% - 18%",
        "risks": ["execution"],
        "margin_value": 11.827
    },
    {
        "ticker": "CSCO",
        "company_name": "Cisco Systems, Inc.",
        "ai_factory_role": "Networking",
        "moat_score": 3.75,
        "growth_cagr": 10.0,
        "backlog_growth": 25,
        "cagr_range": "8% - 12%",
        "risks": ["execution"],
        "margin_value": 27.0
    },
    {
        "ticker": "JNPR",
        "company_name": "Juniper Networks, Inc.",
        "ai_factory_role": "Networking",
        "moat_score": 2.5,
        "growth_cagr": 12.0,
        "backlog_growth": 35,
        "cagr_range": "10% - 14%",
        "risks": ["execution"],
        "margin_value": 14.5
    },
    {
        "ticker": "CIEN",
        "company_name": "Ciena Corporation",
        "ai_factory_role": "Networking",
        "moat_score": 2.5,
        "growth_cagr": 14.0,
        "backlog_growth": 40,
        "cagr_range": "12% - 16%",
        "risks": ["execution", "cyclicality"],
        "margin_value": 12.2
    },
    {
        "ticker": "FN",
        "company_name": "Fabrinet",
        "ai_factory_role": "Networking",
        "moat_score": 3.75,
        "growth_cagr": 20.0,
        "backlog_growth": 70,
        "cagr_range": "17% - 23%",
        "risks": ["customer concentration"],
        "margin_value": 11.5
    },
    {
        "ticker": "EXTR",
        "company_name": "Extreme Networks, Inc.",
        "ai_factory_role": "Networking",
        "moat_score": 2.5,
        "growth_cagr": 11.0,
        "backlog_growth": 20,
        "cagr_range": "9% - 13%",
        "risks": ["execution"],
        "margin_value": 9.5
    },
    # Power Infrastructure
    {
        "ticker": "CEG",
        "company_name": "Constellation Energy Corporation",
        "ai_factory_role": "Power",
        "moat_score": 5.0,
        "growth_cagr": 20.0,
        "backlog_growth": 70,
        "cagr_range": "18% - 22%",
        "risks": ["cyclicality"],
        "margin_value": 8.662
    },
    {
        "ticker": "VST",
        "company_name": "Vistra Corp.",
        "ai_factory_role": "Power",
        "moat_score": 5.0,
        "growth_cagr": 28.0,
        "backlog_growth": 90,
        "cagr_range": "25% - 31%",
        "risks": ["cyclicality"],
        "margin_value": 13.766
    },
    {
        "ticker": "GE",
        "company_name": "General Electric Company",
        "ai_factory_role": "Power",
        "moat_score": 3.75,
        "growth_cagr": 10.0,
        "backlog_growth": 25,
        "cagr_range": "8% - 12%",
        "risks": ["execution"],
        "margin_value": 20.571
    },
    {
        "ticker": "ETN",
        "company_name": "Eaton Corporation plc",
        "ai_factory_role": "Power",
        "moat_score": 3.75,
        "growth_cagr": 14.0,
        "backlog_growth": 55,
        "cagr_range": "12% - 16%",
        "risks": ["cyclicality"],
        "margin_value": 16.563
    },
    {
        "ticker": "NEE",
        "company_name": "NextEra Energy, Inc.",
        "ai_factory_role": "Power",
        "moat_score": 3.75,
        "growth_cagr": 12.0,
        "backlog_growth": 45,
        "cagr_range": "10% - 14%",
        "risks": ["cyclicality"],
        "margin_value": 22.4
    },
    {
        "ticker": "DUK",
        "company_name": "Duke Energy Corporation",
        "ai_factory_role": "Power",
        "moat_score": 2.5,
        "growth_cagr": 8.0,
        "backlog_growth": 20,
        "cagr_range": "6% - 10%",
        "risks": ["cyclicality"],
        "margin_value": 18.2
    },
    {
        "ticker": "SO",
        "company_name": "The Southern Company",
        "ai_factory_role": "Power",
        "moat_score": 2.5,
        "growth_cagr": 9.0,
        "backlog_growth": 22,
        "cagr_range": "7% - 11%",
        "risks": ["cyclicality"],
        "margin_value": 19.5
    },
    {
        "ticker": "AEP",
        "company_name": "American Electric Power Company, Inc.",
        "ai_factory_role": "Power",
        "moat_score": 2.5,
        "growth_cagr": 7.0,
        "backlog_growth": 15,
        "cagr_range": "5% - 9%",
        "risks": ["cyclicality"],
        "margin_value": 17.5
    },
    {
        "ticker": "AES",
        "company_name": "The AES Corporation",
        "ai_factory_role": "Power",
        "moat_score": 2.5,
        "growth_cagr": 11.0,
        "backlog_growth": 35,
        "cagr_range": "9% - 13%",
        "risks": ["cyclicality"],
        "margin_value": 12.5
    },
    # Cooling Systems
    {
        "ticker": "VRT",
        "company_name": "Vertiv Holdings Co.",
        "ai_factory_role": "Cooling",
        "moat_score": 5.0,
        "growth_cagr": 26.0,
        "backlog_growth": 85,
        "cagr_range": "24% - 28%",
        "risks": ["execution", "customer concentration"],
        "margin_value": 20.362
    },
    {
        "ticker": "MOD",
        "company_name": "Modine Manufacturing Company",
        "ai_factory_role": "Cooling",
        "moat_score": 3.75,
        "growth_cagr": 15.0,
        "backlog_growth": 40,
        "cagr_range": "13% - 17%",
        "risks": ["execution"],
        "margin_value": 9.004
    },
    {
        "ticker": "AAON",
        "company_name": "AAON, Inc.",
        "ai_factory_role": "Cooling",
        "moat_score": 3.75,
        "growth_cagr": 13.0,
        "backlog_growth": 35,
        "cagr_range": "11% - 15%",
        "risks": ["execution"],
        "margin_value": 10.987
    },
    {
        "ticker": "JCI",
        "company_name": "Johnson Controls International plc",
        "ai_factory_role": "Cooling",
        "moat_score": 2.5,
        "growth_cagr": 10.0,
        "backlog_growth": 25,
        "cagr_range": "8% - 12%",
        "risks": ["execution"],
        "margin_value": 8.5
    },
    {
        "ticker": "CARR",
        "company_name": "Carrier Global Corporation",
        "ai_factory_role": "Cooling",
        "moat_score": 3.75,
        "growth_cagr": 12.0,
        "backlog_growth": 30,
        "cagr_range": "10% - 14%",
        "risks": ["execution"],
        "margin_value": 14.2
    },
    {
        "ticker": "TT",
        "company_name": "Trane Technologies plc",
        "ai_factory_role": "Cooling",
        "moat_score": 3.75,
        "growth_cagr": 14.0,
        "backlog_growth": 45,
        "cagr_range": "12% - 16%",
        "risks": ["execution"],
        "margin_value": 16.8
    },
    {
        "ticker": "SPXC",
        "company_name": "SPX Technologies, Inc.",
        "ai_factory_role": "Cooling",
        "moat_score": 2.5,
        "growth_cagr": 11.0,
        "backlog_growth": 28,
        "cagr_range": "9% - 13%",
        "risks": ["execution"],
        "margin_value": 10.5
    },
    {
        "ticker": "HON",
        "company_name": "Honeywell International Inc.",
        "ai_factory_role": "Cooling",
        "moat_score": 3.75,
        "growth_cagr": 8.0,
        "backlog_growth": 20,
        "cagr_range": "6% - 10%",
        "risks": ["execution"],
        "margin_value": 21.0
    },
    # Engineering & Construction
    {
        "ticker": "ACM",
        "company_name": "AECOM",
        "ai_factory_role": "Construction",
        "moat_score": 1.25,
        "growth_cagr": 8.0,
        "backlog_growth": 20,
        "cagr_range": "6% - 10%",
        "risks": ["execution"],
        "margin_value": -1.844
    },
    {
        "ticker": "J",
        "company_name": "Jacobs Solutions Inc.",
        "ai_factory_role": "Construction",
        "moat_score": 1.25,
        "growth_cagr": 9.0,
        "backlog_growth": 22,
        "cagr_range": "7% - 11%",
        "risks": ["execution"],
        "margin_value": 7.387
    },
    {
        "ticker": "EME",
        "company_name": "EMCOR Group, Inc.",
        "ai_factory_role": "Construction",
        "moat_score": 2.5,
        "growth_cagr": 11.0,
        "backlog_growth": 28,
        "cagr_range": "9% - 13%",
        "risks": ["cyclicality"],
        "margin_value": 10.618
    },
    {
        "ticker": "PWR",
        "company_name": "Quanta Services, Inc.",
        "ai_factory_role": "Construction",
        "moat_score": 2.5,
        "growth_cagr": 12.0,
        "backlog_growth": 32,
        "cagr_range": "10% - 14%",
        "risks": ["execution"],
        "margin_value": 7.217
    },
    {
        "ticker": "FLR",
        "company_name": "Fluor Corporation",
        "ai_factory_role": "Construction",
        "moat_score": 1.25,
        "growth_cagr": 6.0,
        "backlog_growth": 15,
        "cagr_range": "4% - 8%",
        "risks": ["execution"],
        "margin_value": 2.5
    },
    {
        "ticker": "KBR",
        "company_name": "KBR, Inc.",
        "ai_factory_role": "Construction",
        "moat_score": 2.5,
        "growth_cagr": 10.0,
        "backlog_growth": 25,
        "cagr_range": "8% - 12%",
        "risks": ["execution"],
        "margin_value": 5.5
    },
    {
        "ticker": "TTEK",
        "company_name": "Tetra Tech, Inc.",
        "ai_factory_role": "Construction",
        "moat_score": 2.5,
        "growth_cagr": 11.0,
        "backlog_growth": 27,
        "cagr_range": "9% - 13%",
        "risks": ["execution"],
        "margin_value": 8.2
    },
    {
        "ticker": "DY",
        "company_name": "Dycom Industries, Inc.",
        "ai_factory_role": "Construction",
        "moat_score": 2.5,
        "growth_cagr": 13.0,
        "backlog_growth": 30,
        "cagr_range": "11% - 15%",
        "risks": ["execution"],
        "margin_value": 6.8
    },
    {
        "ticker": "MTZ",
        "company_name": "MasTec, Inc.",
        "ai_factory_role": "Construction",
        "moat_score": 2.5,
        "growth_cagr": 10.0,
        "backlog_growth": 22,
        "cagr_range": "8% - 12%",
        "risks": ["execution"],
        "margin_value": 4.5
    }
]

def generate_moat_criteria_from_score(score: float):
    count = round(score / 1.25)
    return {
        "has_architectural_lock_in": count >= 1,
        "has_ecosystem_dominance": count >= 2,
        "has_high_switching_costs": count >= 3,
        "has_scarcity_or_bottleneck": count >= 4
    }

def main():
    print("Generating seed_list.json...")
    seed_list = []
    financials = {}
    
    # Ensure folders exist
    os.makedirs("data", exist_ok=True)
    transcripts_dir = os.path.join("data", "transcripts")
    llm_cache_dir = os.path.join("data", "llm_cache")
    os.makedirs(transcripts_dir, exist_ok=True)
    os.makedirs(llm_cache_dir, exist_ok=True)
    
    for comp in companies_data:
        ticker = comp["ticker"]
        is_hyperscaler = comp.get("is_hyperscaler", False)
        
        # 1. Build seed list entry
        seed_list.append({
            "ticker": ticker,
            "company_name": comp["company_name"],
            "ai_factory_role": comp["ai_factory_role"],
            "is_hyperscaler": is_hyperscaler
        })
        
        # 2. Build financials entry
        financials[ticker] = comp["margin_value"]
        
        # Skip generating mock files for hyperscalers
        if is_hyperscaler:
            continue
            
        # 3. Generate mock transcript
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
            
        # 4. Generate LLM cache JSON
        moat_criteria = generate_moat_criteria_from_score(comp["moat_score"])
        cache_json = {
            "ticker": ticker,
            "company_name": comp["company_name"],
            "ai_factory_role": comp["ai_factory_role"],
            "is_hyperscaler": False,
            "moat_score": comp["moat_score"],
            "growth_cagr": comp["growth_cagr"],
            "risks": comp["risks"],
            **moat_criteria
        }
        
        cache_path = os.path.join(llm_cache_dir, f"{ticker}.json")
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache_json, f, indent=2)

    # Save data/seed_list.json
    seed_list_path = os.path.join("data", "seed_list.json")
    with open(seed_list_path, "w", encoding="utf-8") as f:
        json.dump(seed_list, f, indent=2)
    print(f"Saved seed list to {seed_list_path}")
    
    # Save data/financials.json
    financials_path = os.path.join("data", "financials.json")
    with open(financials_path, "w", encoding="utf-8") as f:
        json.dump(financials, f, indent=2)
    print(f"Saved financials to {financials_path}")
    print("Done generating offline mocks.")

if __name__ == "__main__":
    main()
