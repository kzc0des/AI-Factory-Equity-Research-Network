import os
from typing import Any, Dict
from src.schema.state import ParentState

def generate_markdown_report(state: ParentState) -> str:
    """
    Generates a Markdown report from the Top 20 ranking.
    """
    top_20 = state.get("top_20", [])
    
    report = ["# Top 20 AI Factory Growth Equity Targets\n"]
    
    for rank, profile in enumerate(top_20, start=1):
        report.append(f"## {rank}. {profile.company_name} ({profile.ticker})")
        report.append(f"**Total AI Factory Growth Score:** {profile.total_score:.2f}")
        role_str = profile.ai_factory_role.value if profile.ai_factory_role else 'N/A'
        report.append(f"**AI Factory Role:** {role_str}")
        report.append(f"**Moat Score:** {profile.moat_score}")
        report.append(f"**Margin Score:** {profile.margin_score}")
        report.append(f"**Growth CAGR:** {profile.growth_cagr}%")
        
        discount = profile.risk_discount
        if discount is not None and discount < 1.0:
            report.append(f"**Risk Discount Applied:** {discount:.2f}x")
        
        if profile.catalysts:
            report.append("**Catalysts:**")
            for catalyst in profile.catalysts:
                report.append(f"- {catalyst}")
                
        if profile.risks:
            report.append("**Risks:**")
            for risk in profile.risks:
                report.append(f"- {risk.value}")
        
        report.append("\n---\n")
        
    return "\n".join(report)

def report_node(state: ParentState) -> Dict[str, Any]:
    """
    LangGraph node to generate the final formatted Markdown document.
    Writes the report to an output file.
    """
    markdown_content = generate_markdown_report(state)
    
    os.makedirs("output", exist_ok=True)
    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    return {"report_generated": True}
