"""Sub-agents package - Specialized agents for tasks"""

from .emotions_manager import emotions_manager_agent  # Old (kept for reference)
from .topics_manager import topics_manager_agent  # Old (kept for reference)
from .personality_manager import personality_manager_agent  # Old (kept for reference)
from .research_agent import research_agent  # Old (kept for reference)
from .memory_manager import memory_manager_agent  # Old (kept for reference)
from .writer_agent import writer_agent

# Sub-graph versions (Phase 4B & 6)
from .topics_subgraph import topics_manager_subgraph_tool
from .emotions_subgraph import emotions_manager_subgraph_tool
from .personality_subgraph import personality_manager_subgraph_tool

# Nested Deep Agent versions (Phase 5)
from .research_deep_agent import research_deep_agent
from .memory_deep_agent import memory_deep_agent

__all__ = [
    # Old simple tools (kept for reference)
    "emotions_manager_agent",
    "topics_manager_agent",
    "personality_manager_agent",
    "research_agent",
    "memory_manager_agent",
    # Current tools
    "writer_agent",
    # Sub-graphs (Phase 4B & 6)
    "topics_manager_subgraph_tool",
    "emotions_manager_subgraph_tool",
    "personality_manager_subgraph_tool",
    # Nested Deep Agents (Phase 5)
    "research_deep_agent",
    "memory_deep_agent",
]
