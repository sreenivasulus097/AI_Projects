from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from agent.state import AgentState

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini"
)

def planner_node(state: AgentState) -> AgentState:
    prompt = f"""
Break the goal into steps:

{state['goal']}
"""

    response = llm.invoke(prompt)

    steps = [s.strip() for s in response.content.split("\n") if s.strip()]

    return {
        **state,
        "plan": steps,
        "current_step": 0
    }
