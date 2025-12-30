from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.planner import planner_node


def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("planner", planner_node)

    # Flow
    graph.set_entry_point("planner")
    graph.add_edge("planner", END)

    return graph.compile()
