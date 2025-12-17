import os
from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from langchain_openai import ChatOpenAI

from prompts import SYSTEM_PROMPT
from tools import reset_tool_counters, tools


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
    
    return create_deep_agent(
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        model=llm,
        backend=make_backend,
    )


__all__ = ["build_agent", "reset_tool_counters"]

