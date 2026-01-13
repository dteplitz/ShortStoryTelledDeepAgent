"""Personality Manager - Evolves personality.txt (10-12 items, refinement not growth)"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

PERSONALITY_MANAGER_PROMPT = """You refine a writer's personality through gradual evolution.

## Your Role
Maintain 10-12 stable personality traits that evolve slowly over time.

## Refinement Strategy
- Refine existing traits for clarity
- Add new traits if writing revealed growth
- Remove traits that no longer fit
- Each trait describes writing style or voice

Personality evolves gradually, not through overhauls.

## Output
Return the final list (10-12 traits), one per line, no explanation."""


def personality_manager_agent(operation: str = "refine", story_content: str = "", topic: str = "") -> str:
    """
    Tool: Manage personality.txt
    
    Operations:
    - retrieve: Get current personality
    - refine: Update based on story
    
    Args:
        operation: "retrieve" or "refine"
        story_content: (for refine) Story just written
        topic: (for refine) Topic explored
        
    Returns:
        Current personality or success message
    """
    from tools import read_text_file, write_text_file
    
    current_personality = read_text_file("personality.txt")
    
    # Retrieve operation - just return current personality
    if operation == "retrieve":
        return current_personality if current_personality else "No personality defined yet."
    
    # Refine operation (default)
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.3,  # Lower temp for stability
    )
    
    messages = [
        SystemMessage(content=PERSONALITY_MANAGER_PROMPT),
        HumanMessage(content=f"""Current traits ({len(current_personality.strip().splitlines())}):
{current_personality}

Story (topic: {topic}):
{story_content[:400]}...

Refine the personality (10-12 traits):""")
    ]
    
    response = llm.invoke(messages)
    updated = response.content.strip()
    
    # Validate and enforce size limits
    lines = [l.strip() for l in updated.split('\n') if l.strip()]
    
    # Hard cap at 12
    if len(lines) > 12:
        lines = lines[:12]
    
    write_text_file("personality.txt", '\n'.join(lines) + '\n', mode='w')
    
    return f"✅ Refined personality.txt: {len(lines)} traits (was {len(current_personality.strip().splitlines())})"
