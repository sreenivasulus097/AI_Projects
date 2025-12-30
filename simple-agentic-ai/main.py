from agent import planner_agent, executor_agent

def run():
    task = input("Enter a task: ")

    print("\n--- PLAN ---")
    print("task::",task)
    plan = planner_agent(task)
    print(plan)

    print("\n--- EXECUTION ---")
    result = executor_agent(plan)
    print(result)


if __name__ == "__main__":
    run()
