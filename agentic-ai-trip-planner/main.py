# main.py
from dotenv import load_dotenv
import os

# Load environment variables (must happen before importing `agent` which
# constructs the LangGraph agent and initializes OpenAI clients).
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

from agentic_graph import 
user_query = {
    "preferences": {
        "cities": ["Paris", "Rome"],
        "budget": 1500,
        "days": 5,
        "activities": ["sightseeing", "local cuisine"]
    }
}

import asyncio
from inspect import isawaitable


def run_agent(agent, payload):
    # Try common execution APIs in order of likelihood
    if hasattr(agent, "run"):
        return agent.run(payload)
    if hasattr(agent, "invoke"):
        result = agent.invoke(payload)
        if isawaitable(result):
            return asyncio.run(result)
        return result
    if callable(agent):
        res = agent(payload)
        if isawaitable(res):
            return asyncio.run(res)
        return res
    raise RuntimeError("Agent object has no executable interface (no run/invoke/call)")


output = run_agent(agent, {"context": user_query})

print("----- FINAL ITINERARY -----")
print(output)

