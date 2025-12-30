from agent.graph import build_graph

if __name__ == "__main__":
    app = build_graph()

    goal = input("🎯 Enter your goal: ")

    result = app.invoke({
        "goal": goal,
        "plan": [],
        "current_step": 0,
        "result": ""
    })

    print("\n🧠 Agent Plan:")
    for step in result["plan"]:
        print("-", step)
