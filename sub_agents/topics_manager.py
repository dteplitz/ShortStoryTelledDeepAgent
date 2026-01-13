"""Topics Manager - Evolves topics.txt (5-6 items, rotation not growth)"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

TOPICS_MANAGER_PROMPT = """You curate an evolving list of fascinating topics.

## Your Role
Maintain 5-6 compelling topics through rotation and discovery.

## Evolution Strategy
- Add new topics discovered in research
- Keep topics that remain fascinating
- Remove stale or less interesting topics
- Ask: "What would I want to write about next?"

Quality over quantity - only the most compelling topics survive.

## Output
Return the final list (5-6 topics), one per line, no explanation."""


def topics_manager_agent(operation: str = "evolve", research_content: str = "", topic_used: str = "") -> str:
    """
    Tool: Manage topics.txt
    
    Operations:
    - retrieve: Get current topics
    - evolve: Update based on research
    
    Args:
        operation: "retrieve" or "evolve"
        research_content: (for evolve) Research findings
        topic_used: (for evolve) Topic just explored
        
    Returns:
        Current topics or success message
    """
    from tools import read_text_file, write_text_file
    
    current_topics = read_text_file("topics.txt")
    
    # Retrieve operation - just return current topics
    if operation == "retrieve":
        return current_topics if current_topics else "No topics defined yet."
    
    # Evolve operation (default)
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.4,
    )
    
    messages = [
        SystemMessage(content=TOPICS_MANAGER_PROMPT),
        HumanMessage(content=f"""Current topics ({len(current_topics.strip().splitlines())}):
{current_topics}

Just explored: {topic_used}

Research insights:
{research_content[:600]}...

Evolve the list (5-6 topics):""")
    ]
    
    response = llm.invoke(messages)
    updated = response.content.strip()
    
    # Validate and enforce size limits
    lines = [l.strip() for l in updated.split('\n') if l.strip()]
    
    # Hard cap at 6
    if len(lines) > 6:
        lines = lines[:6]
    
    write_text_file("topics.txt", '\n'.join(lines) + '\n', mode='w')
    
    return f"✅ Evolved topics.txt: {len(lines)} topics (was {len(current_topics.strip().splitlines())})"
