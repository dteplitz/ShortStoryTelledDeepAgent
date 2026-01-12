"""Sub-agents package - Specialized agents for file management"""

from .emotions_manager import emotions_manager_agent
from .topics_manager import topics_manager_agent
from .personality_manager import personality_manager_agent

__all__ = [
    "emotions_manager_agent",
    "topics_manager_agent",
    "personality_manager_agent",
]
