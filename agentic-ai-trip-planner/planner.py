# planner.py
from openai import OpenAI
client = OpenAI()

def planner_node(state):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a travel planner AI"},
            {"role": "user", "content": state["query"]}
        ]
    )
    state["result"] = response.choices[0].message.content
    return state
