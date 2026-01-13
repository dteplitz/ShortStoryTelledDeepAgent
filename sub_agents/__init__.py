"""Sub-agents package - Specialized agents for tasks"""

from .emotions_manager import emotions_manager_agent
from .topics_manager import topics_manager_agent
from .personality_manager import personality_manager_agent
from .research_agent import research_agent  # Old simple version (kept for reference)
from .memory_manager import memory_manager_agent  # Old simple version (kept for reference)
from .writer_agent import writer_agent

# Sub-graph versions (Phase 4B)
from .topics_subgraph import topics_manager_subgraph_tool

# Nested Deep Agent versions (Phase 5)
from .research_deep_agent import research_deep_agent
from .memory_deep_agent import memory_deep_agent

__all__ = [
    "emotions_manager_agent",
    "topics_manager_agent",
    "personality_manager_agent",
    "research_agent",  # Old
    "memory_manager_agent",  # Old
    "writer_agent",
    "topics_manager_subgraph_tool",  # Sub-graph
    "research_deep_agent",  # NEW: Nested Deep Agent
    "memory_deep_agent",  # NEW: Nested Deep Agent
]
