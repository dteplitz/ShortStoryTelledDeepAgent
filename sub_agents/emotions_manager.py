"""Emotions Manager - Evolves emotions.txt (4-5 items, rotation not growth)"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

EMOTIONS_MANAGER_PROMPT = """You curate an evolving emotional palette.

## Your Role
Maintain a focused 4-5 emotion palette that grows through rotation, not accumulation.

## Rotation Strategy
- You have 1-2 flexible slots
- Assess: What new emotional nuance did this story reveal?
- Keep valuable emotions, rotate stale ones
- Each emotion is a 2-4 word phrase

## Output
Return the final list (4-5 emotions), one per line, no explanation."""


def emotions_manager_agent(operation: str = "evolve", story_content: str = "") -> str:
    """
    Tool: Manage emotions.txt
    
    Operations:
    - retrieve: Get current emotions
    - evolve: Update based on story
    
    Args:
        operation: "retrieve" or "evolve"
        story_content: (for evolve) The story just written
        
    Returns:
        Current emotions or success message
    """
    # Import here to avoid circular dependency
    from tools import read_text_file, write_text_file
    
    current_emotions = read_text_file("emotions.txt")
    
    # Retrieve operation - just return current emotions
    if operation == "retrieve":
        return current_emotions if current_emotions else "No emotions defined yet."
    
    # Evolve operation (default)
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.4,
    )
    
    messages = [
        SystemMessage(content=EMOTIONS_MANAGER_PROMPT),
        HumanMessage(content=f"""Current palette ({len(current_emotions.strip().splitlines())} emotions):
{current_emotions}

Recent story:
{story_content[:400]}...

Evolve the palette (4-5 emotions):""")
    ]
    
    response = llm.invoke(messages)
    updated = response.content.strip()
    
    # Validate and enforce size limits
    lines = [l.strip() for l in updated.split('\n') if l.strip()]
    
    # Hard cap at 5
    if len(lines) > 5:
        lines = lines[:5]
    
    write_text_file("emotions.txt", '\n'.join(lines) + '\n', mode='w')
    
    return f"✅ Evolved emotions.txt: {len(lines)} emotions (was {len(current_emotions.strip().splitlines())})"
