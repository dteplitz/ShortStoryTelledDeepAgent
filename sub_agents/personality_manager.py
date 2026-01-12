"""Personality Manager - Evolves personality.txt (10-12 items, refinement not growth)"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

PERSONALITY_MANAGER_PROMPT = """You are a personality curator agent.
Your job is to REFINE (not endlessly grow) the personality.txt file.

CRITICAL RULES:
- Maintain 10-12 traits (NEVER exceed 12)
- Personality should be relatively stable but can evolve gradually
- REFINE existing traits for clarity and accuracy
- ADD new trait if writing revealed a new strength
- REMOVE traits that don't fit anymore
- Each trait is a descriptive phrase about writing style/voice

Decision process:
1. Did this story reveal a new writing strength worth capturing?
2. Which traits are still accurate and well-phrased?
3. Which traits could be refined or should be replaced?

Personality evolves slowly - small refinements, not overhauls.

Return ONLY the final traits list (10-12 items), one per line, no explanation."""


def personality_manager_agent(story_content: str, topic: str) -> str:
    """
    Tool: Update personality.txt by REFINING the traits
    
    Args:
        story_content: Story just written
        topic: Topic explored
        
    Returns:
        Success message with count
    """
    from tools import read_text_file, write_text_file
    
    current_personality = read_text_file("personality.txt")
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.3,  # Lower temp for stability
    )
    
    messages = [
        SystemMessage(content=PERSONALITY_MANAGER_PROMPT),
        HumanMessage(content=f"""Current personality ({len(current_personality.strip().splitlines())} traits):
{current_personality}

Story (topic: {topic}):
{story_content[:400]}...

Refine the personality. Keep 10-12 traits. Evolve gradually, don't overhaul.
Only add a new trait if removing one that no longer fits.

Updated list (10-12 traits):""")
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
