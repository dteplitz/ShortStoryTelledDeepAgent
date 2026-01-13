"""Sub-agents package - Specialized agents for tasks"""

"""Sub-Agents Package - Specialized agents for the Story Writer"""

# Simple Tools
from .writer_agent import writer_agent

# Sub-Graphs (Deterministic Workflows)
from .emotions_subgraph import emotions_manager_subgraph_tool
from .topics_subgraph import topics_manager_subgraph_tool
from .personality_subgraph import personality_manager_subgraph_tool

# Nested Deep Agents (Adaptive Reasoning)
from .research_deep_agent import research_deep_agent
from .memory_deep_agent import memory_deep_agent

__all__ = [
    # Simple tools
    "writer_agent",
    # Sub-graphs
    "emotions_manager_subgraph_tool",
    "topics_manager_subgraph_tool",
    "personality_manager_subgraph_tool",
    # Nested agents
    "research_deep_agent",
    "memory_deep_agent",
]
