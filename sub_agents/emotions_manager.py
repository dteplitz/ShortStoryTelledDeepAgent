"""Emotions Manager - Evolves emotions.txt (4-5 items, rotation not growth)"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

EMOTIONS_MANAGER_PROMPT = """You are an emotions curator agent.
Your job is to EVOLVE (not endlessly grow) the emotions.txt file.

CRITICAL RULES:
- Maintain 4-5 emotions total (NEVER exceed 5)
- Always keep these core 3: "Wonder and curiosity", "Melancholy hope", "Quiet intensity"
- For the remaining 1-2 slots: ROTATE - add new emotions OR keep existing OR remove stale ones
- Each emotion is a 2-4 word phrase
- Think of this as ROTATING a playlist, not expanding it

Decision process:
1. What new emotional nuance did this story explore?
2. Which existing emotions (beyond core 3) are still valuable?
3. If adding a new emotion and already at 5, which one should be REPLACED?

Keep it simple - a focused emotional palette is more powerful.

Return ONLY the final emotions list (4-5 items), one per line, no explanation."""


def emotions_manager_agent(story_content: str) -> str:
    """
    Tool: Update emotions.txt by EVOLVING (not growing) the list
    
    Args:
        story_content: The story just written
        
    Returns:
        Success message with count
    """
    # Import here to avoid circular dependency
    from tools import read_text_file, write_text_file
    
    current_emotions = read_text_file("emotions.txt")
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.4,
    )
    
    messages = [
        SystemMessage(content=EMOTIONS_MANAGER_PROMPT),
        HumanMessage(content=f"""Current emotions ({len(current_emotions.strip().splitlines())} items):
{current_emotions}

Story just written:
{story_content[:400]}...

Evolve the emotions list. Keep 4-5 items total. Rotate content, don't just add.
Always keep the core 3, rotate the remaining 1-2 slots.

Updated list (4-5 emotions):""")
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
