"""Research Agent - Dedicated web research specialist"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
import json

RESEARCH_AGENT_PROMPT = """You conduct multi-angle research for creative writing.

## Your Capabilities
- Generate focused search queries
- Synthesize findings from multiple sources
- Extract key facts and themes
- Identify fascinating sub-topics

You provide structured, actionable research summaries."""


QUERY_GENERATOR_PROMPT = """Generate 2-3 focused search queries for this topic.

Topic: {topic}

Requirements:
- Explore different angles
- Include "2026" or "latest" for currency
- Cover developments, applications, implications

Return ONLY a JSON array of query strings.
Example: ["query 1", "query 2", "query 3"]"""


SYNTHESIS_PROMPT = """Synthesize research into a creative writing brief.

Topic: {topic}

Search Results:
{results}

Use this format:

SUMMARY:
[2-3 sentences on the most interesting/current aspects]

KEY_FACTS:
- [Fascinating fact 1 for story inspiration]
- [Fascinating fact 2 for story inspiration]
- [Fascinating fact 3 for story inspiration]

DISCOVERED_TOPICS:
- [Fascinating related topic 1]
- [Fascinating related topic 2]

Focus on creative inspiration, not academic completeness."""


def research_agent(topic: str) -> str:
    """
    Tool: Conduct comprehensive research on a topic
    
    This agent:
    1. Generates multiple focused search queries
    2. Executes web searches
    3. Synthesizes findings into a creative writing brief
    4. Identifies new topics to explore
    
    Args:
        topic: The topic to research
        
    Returns:
        Structured research summary with:
        - SUMMARY: Key insights (for story context)
        - KEY_FACTS: Interesting facts (to weave into story)
        - DISCOVERED_TOPICS: New topics found (for topics_manager)
    """
    from tools import internet_search
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.3,  # Lower temp for focused research
    )
    
    # Step 1: Generate focused search queries
    query_gen_messages = [
        SystemMessage(content=RESEARCH_AGENT_PROMPT),
        HumanMessage(content=QUERY_GENERATOR_PROMPT.format(topic=topic))
    ]
    
    query_response = llm.invoke(query_gen_messages)
    
    try:
        # Parse the queries from JSON
        queries = json.loads(query_response.content.strip())
        if not isinstance(queries, list):
            queries = [f"{topic} latest developments 2026"]
    except:
        # Fallback if JSON parsing fails
        queries = [
            f"{topic} latest developments 2026",
            f"{topic} recent breakthroughs"
        ]
    
    # Limit to 2-3 queries to respect search limits
    queries = queries[:2]
    
    # Step 2: Execute searches
    search_results = []
    for query in queries:
        result = internet_search(query)
        search_results.append(f"Query: {query}\n{result}\n")
    
    combined_results = "\n---\n".join(search_results)
    
    # Step 3: Synthesize findings
    synthesis_messages = [
        SystemMessage(content=RESEARCH_AGENT_PROMPT),
        HumanMessage(content=SYNTHESIS_PROMPT.format(
            topic=topic,
            results=combined_results[:2000]  # Limit to avoid token overflow
        ))
    ]
    
    synthesis_response = llm.invoke(synthesis_messages)
    
    # Return the structured synthesis
    return synthesis_response.content


# For backwards compatibility, keep this export
__all__ = ["research_agent"]
