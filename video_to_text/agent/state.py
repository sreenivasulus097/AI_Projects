from typing import TypedDict, List


class AgentState(TypedDict):
    goal: str
    plan: List[str]
    current_step: int
    result: str
