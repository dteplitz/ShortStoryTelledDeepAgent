"""Sub-agents package - Specialized agents for tasks"""

from .emotions_manager import emotions_manager_agent
from .topics_manager import topics_manager_agent
from .personality_manager import personality_manager_agent
from .research_agent import research_agent
from .memory_manager import memory_manager_agent
from .writer_agent import writer_agent

# Sub-graph versions (Phase 4B)
from .topics_subgraph import topics_manager_subgraph_tool

__all__ = [
    "emotions_manager_agent",
    "topics_manager_agent",
    "personality_manager_agent",
    "research_agent",
    "memory_manager_agent",
    "writer_agent",
    "topics_manager_subgraph_tool",  # NEW: Sub-graph version
]
