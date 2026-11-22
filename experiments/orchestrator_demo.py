from ai_agent.application.orchestrator import (
    AgentOrchestrator,
)


def main() -> None:
    agent = AgentOrchestrator(
        max_turns=5,
        max_tool_calls=10,
    )

    answer = agent.run(
        "Where is my order #4821, and how long does shipping take?"
    )

    print(answer)


if __name__ == "__main__":
    main()
