import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, PLANNER_PROMPT, EXECUTOR_PROMPT

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content


def planner_agent(task):
    prompt = PLANNER_PROMPT.format(task=task)
    print("planner prompt before calling planner function::",prompt)
    return call_llm(prompt)


def executor_agent(plan):
    print("executor plan before calling executor function::",plan)
    prompt = EXECUTOR_PROMPT.format(plan=plan)
    return call_llm(prompt)
