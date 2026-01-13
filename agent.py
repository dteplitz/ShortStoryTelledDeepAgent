import os
from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from langchain_openai import ChatOpenAI

from prompts import SYSTEM_PROMPT
from tools import reset_tool_counters, tools

# Import specialized sub-agents
from sub_agents import (
    emotions_manager_agent,
    topics_manager_agent,
    personality_manager_agent,
    research_agent,
    memory_manager_agent,
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
        research_agent,
        memory_manager_agent,
        emotions_manager_agent,
        topics_manager_agent,
        personality_manager_agent,
    ]
    
    return create_deep_agent(
        tools=all_tools,
        system_prompt=SYSTEM_PROMPT,
        model=llm,
        backend=make_backend,
    )


__all__ = ["build_agent", "reset_tool_counters"]

