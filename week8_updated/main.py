def main():

    print("""
========================================
LangGraph + Gemini Hands-on Exercises
========================================

1. Persistence & Checkpoints
2. Human-in-the-Loop
3. Subgraphs
4. Combined Workflow
""")

    choice = input("Select exercise: ").strip()

    if choice == "1":

        from exercise_1.persistence import run
        run()

    elif choice == "2":

        from exercise_2.human_approval import run
        run()

    elif choice == "3":

        from exercise_3.main_graph import run
        run()

    elif choice == "4":

        from exercise_4.combined_workflow import run
        run()

    else:

        print("Invalid choice.")


if __name__ == "__main__":
    main()
