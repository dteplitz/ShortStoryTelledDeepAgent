"""Topics Manager - Evolves topics.txt (5-6 items, rotation not growth)"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

TOPICS_MANAGER_PROMPT = """You are a topics curator agent.
Your job is to EVOLVE (not endlessly grow) the topics.txt file.

CRITICAL RULES:
- Maintain 5-6 topics total (NEVER exceed 6)
- ADD new fascinating topics discovered in research
- REMOVE topics that are now less interesting or stale
- KEEP topics that remain compelling
- Think: "What would I want to write about next time?"

Decision process:
1. What 1 new topic emerged from research that's truly fascinating?
2. Which existing topics are still interesting?
3. If adding a new topic and already at 6, which topic should make room for it?

Quality over quantity - only the most compelling topics survive.

Return ONLY the final topics list (5-6 items), one per line, no explanation."""


def topics_manager_agent(research_content: str, topic_used: str) -> str:
    """
    Tool: Update topics.txt by EVOLVING (not growing) the list
    
    Args:
        research_content: Research findings
        topic_used: Topic just explored
        
    Returns:
        Success message with count
    """
    from tools import read_text_file, write_text_file
    
    current_topics = read_text_file("topics.txt")
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.4,
    )
    
    messages = [
        SystemMessage(content=TOPICS_MANAGER_PROMPT),
        HumanMessage(content=f"""Current topics ({len(current_topics.strip().splitlines())} items):
{current_topics}

Just explored: {topic_used}

Research insights:
{research_content[:600]}...

Evolve the topics list. Keep 5-6 items. Replace stale with fresh discoveries.
If adding a new topic, remove a less interesting one to maintain the limit.

Updated list (5-6 topics):""")
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
