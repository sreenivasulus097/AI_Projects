from langgraph.prebuilt import create_react_agent, ToolNode
from agent_tools import tools

# Prompt: instruct the agent to plan the trip
PROMPT = """You are an AI travel planner.
Given user preferences, plan the trip by deciding which tools to use in order:
- Flight Planner
- Hotel Finder
- Weather Checker
- Attractions Finder
Then generate a final itinerary."""

# Use LangGraph prebuilt helper to compose the model, prompt and tools
# `create_react_agent` returns an executable compiled graph-like object.
agent = create_react_agent(
    model="openai:gpt-4o-mini",
    tools=tools,
    prompt=PROMPT,
)

# Export agent and ToolNode for external use
__all__ = ["agent", "ToolNode"]
