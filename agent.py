import os
from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from langchain_openai import ChatOpenAI

from prompts import SYSTEM_PROMPT
from tools import reset_tool_counters, tools

# Import specialized sub-agents
from sub_agents import (
    emotions_manager_agent,
    topics_manager_subgraph_tool,  # Sub-graph (Phase 4B)
    personality_manager_agent,
    research_deep_agent,  # Nested Deep Agent (Phase 5)
    memory_deep_agent,  # Nested Deep Agent (Phase 5)
    writer_agent,
)


def build_agent():
    """
    Construct a Deep Agent using the official creator (planning + fs tools included).
    """
    # Configure the OpenAI model
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.2,
    )
    
    # Configure backend to allow file access in agent state
    def make_backend(runtime):
        return StateBackend(runtime)
    
    # Combine basic tools with specialized sub-agents
    all_tools = tools + [
        research_deep_agent,           # UPGRADED: Nested Deep Agent (Phase 5)
        memory_deep_agent,             # UPGRADED: Nested Deep Agent (Phase 5)
        emotions_manager_agent,        # Simple tool (TODO: upgrade to sub-graph)
        topics_manager_subgraph_tool,  # UPGRADED: Sub-graph (Phase 4B)
        personality_manager_agent,     # Simple tool (TODO: upgrade to sub-graph)
        writer_agent,                  # Simple tool (works well as-is)
    ]
    
    return create_deep_agent(
        tools=all_tools,
        system_prompt=SYSTEM_PROMPT,
        model=llm,
        backend=make_backend,
    )


__all__ = ["build_agent", "reset_tool_counters"]

