from typing import List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send

from src.schema.company import CompanyProfile
from src.schema.state import ParentState
from src.agents.ingestion import filter_companies
from src.agents.margin import margin_analysis_node
from src.agents.moat import moat_analysis_node
from src.agents.growth import growth_forecast_node
from src.agents.ranking import ranking_node
from src.agents.report import report_node

def build_company_subgraph() -> StateGraph:
    """
    Builds the single-company sub-graph that processes a CompanyProfile.
    Routes sequentially: Margin -> Moat -> Growth.
    """
    workflow = StateGraph(CompanyProfile)
    
    workflow.add_node("margin", margin_analysis_node)
    workflow.add_node("moat", moat_analysis_node)
    workflow.add_node("growth", growth_forecast_node)
    
    workflow.add_edge(START, "margin")
    workflow.add_edge("margin", "moat")
    workflow.add_edge("moat", "growth")
    workflow.add_edge("growth", END)
    
    return workflow

# Compile the subgraph once to be used by the wrapper node
subgraph_runnable = build_company_subgraph().compile()

def process_company_node(state: CompanyProfile) -> Dict[str, Any]:
    """
    Wrapper node that executes the compiled sub-graph for a single company.
    Returns the final state wrapped in a dictionary under the 'profiles' key
    so that the parent graph's operator.add can aggregate them.
    """
    result = subgraph_runnable.invoke(state)
    return {"profiles": [result]}

def ingest_node(state: ParentState) -> Dict[str, Any]:
    """
    LangGraph node to ingest and filter the seed list.
    """
    seed_list = state.get("seed_list", [])
    # We can perform ingestion/filtering here if needed.
    return {"seed_list": seed_list}

def map_companies(state: ParentState) -> List[Send]:
    """
    Conditional edge function that maps the filtered targets to the sub-graph.
    """
    seed_list = state.get("seed_list", [])
    valid_targets = filter_companies(seed_list)
    
    sends = []
    for target in valid_targets:
        sends.append(Send("process_company", target))
    return sends

def build_parent_graph():
    """
    Builds the parent map-reduce graph.
    """
    parent_workflow = StateGraph(ParentState)
    
    # Define nodes
    parent_workflow.add_node("ingest", ingest_node)
    parent_workflow.add_node("process_company", process_company_node)
    parent_workflow.add_node("rank", ranking_node)
    parent_workflow.add_node("report", report_node)
    
    # Define edges
    parent_workflow.add_edge(START, "ingest")
    
    # Map edge: from ingest, fan-out to process_company
    parent_workflow.add_conditional_edges("ingest", map_companies, ["process_company"])
    
    # Reduce edge: after all process_company instances complete, go to rank
    parent_workflow.add_edge("process_company", "rank")
    
    parent_workflow.add_edge("rank", "report")
    parent_workflow.add_edge("report", END)
    
    return parent_workflow
