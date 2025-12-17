import argparse
from langchain_core.messages import HumanMessage

from agent import build_agent, reset_tool_counters


def run_once(query: str, thread_id: str = "demo-run"):
    graph_app = build_agent()
    reset_tool_counters()
    initial_state = {"messages": [HumanMessage(content=query)]}

    # Stream events for visibility
    for event in graph_app.stream(
        initial_state, {"configurable": {"thread_id": thread_id}}
    ):
        for _, value in event.items():
            print(value)

    final = graph_app.invoke(initial_state)
    print("\nFinal response:\n", final["messages"][-1].content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creative Story Writer Agent - Automatically generates stories based on interesting topics."
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="Create a story.",
        help="Custom prompt to send to the agent (optional - defaults to automatic story creation).",
    )
    parser.add_argument(
        "--thread-id",
        default="story-writer",
        help="Thread ID for LangGraph configurable context.",
    )
    args = parser.parse_args()
    run_once(args.query, thread_id=args.thread_id)

