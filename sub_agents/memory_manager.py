"""Memory Manager - Long-term episodic memory with natural imperfection"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

MEMORY_MANAGER_PROMPT = """You manage long-term memory like a human mind.

## Your Role
Store, retrieve, and consolidate memories with natural imperfection.

## Memory Characteristics
- Memories fade and simplify over time
- Similar memories merge together
- Details can shift slightly (memory is reconstructive)
- Emotional moments are remembered more vividly
- Maintain 15-20 memories total

## Operations

**Store:** Add new significant experiences
**Retrieve:** Find memories related to a query
**Consolidate:** Merge similar memories, simplify old ones, forget trivial details

Memories are imperfect, like human recall."""


STORE_PROMPT = """Add this new experience to your memory.

Current memories ({count}):
{memories}

New experience to store:
{experience}

Context: {context}

Instructions:
- Add this experience as a new memory (one concise line)
- If you already have 20+ memories, merge similar ones or remove the least significant
- Keep total between 15-20 memories
- Return ONLY the complete updated list of memories, one per line
- No explanations, just the memory list"""


RETRIEVE_PROMPT = """Retrieve memories relevant to this query.

Query: {query}

All memories:
{memories}

Return 3-5 most relevant memories, or "No relevant memories found" if none match.
Memories may have slight imperfections - that's natural."""


CONSOLIDATE_PROMPT = """Consolidate memories like a human mind over time.

Current memories ({count}):
{memories}

Tasks:
1. Merge similar memories into one
2. Simplify overly detailed memories
3. Keep emotionally significant moments vivid
4. Forget trivial details
5. Allow slight creative shifts (memory isn't perfect)

Return consolidated list (15-20 memories), one per line."""


def memory_manager_agent(
    operation: str = "retrieve",
    experience: str = "",
    context: str = "",
    query: str = ""
) -> str:
    """
    Tool: Manage long-term episodic memory
    
    Operations:
    - store: Save a new memory (requires experience, optional context)
    - retrieve: Get relevant memories (requires query)
    - consolidate: Merge and simplify memories
    
    Args:
        operation: "store", "retrieve", or "consolidate"
        experience: (for store) What to remember
        context: (for store) Context about the experience
        query: (for retrieve) What to search for
        
    Returns:
        Success message or retrieved memories
    """
    from tools import read_text_file, write_text_file
    
    # Ensure memories file exists
    try:
        memories = read_text_file("memories.txt")
    except:
        memories = ""
        write_text_file("memories.txt", "", mode='w')
    
    memory_lines = [l.strip() for l in memories.split('\n') if l.strip()]
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.5,  # Higher temp for natural imperfection
    )
    
    if operation == "store":
        # Validate experience is provided
        if not experience or not experience.strip():
            return "❌ Error: No experience provided to store"
        
        messages = [
            SystemMessage(content=MEMORY_MANAGER_PROMPT),
            HumanMessage(content=STORE_PROMPT.format(
                count=len(memory_lines),
                memories=memories if memories else "(No memories yet)",
                experience=experience.strip(),
                context=context if context else "General"
            ))
        ]
        
        response = llm.invoke(messages)
        updated = response.content.strip()
        
        # Filter out any explanation text - only keep memory statements
        lines = []
        for line in updated.split('\n'):
            line = line.strip()
            # Skip empty lines, headers, or prompts
            if not line:
                continue
            if line.startswith(('Current', 'New experience', 'Context:', 'Instructions:', 'Return', 'Please', '-', '*')):
                continue
            # Skip lines that look like questions or prompts
            if '?' in line or 'provide' in line.lower():
                continue
            lines.append(line)
        
        # Ensure we have at least the new experience
        if not lines:
            lines = [experience.strip()]
        
        # Cap at 20
        if len(lines) > 20:
            lines = lines[:20]
        
        write_text_file("memories.txt", '\n'.join(lines) + '\n', mode='w')
        return f"✅ Memory stored: {len(lines)} memories total"
    
    elif operation == "retrieve":
        if not memories:
            return "No memories yet."
        
        if not query:
            return "No query provided for retrieval."
        
        messages = [
            SystemMessage(content=MEMORY_MANAGER_PROMPT),
            HumanMessage(content=RETRIEVE_PROMPT.format(
                query=query,
                memories=memories
            ))
        ]
        
        response = llm.invoke(messages)
        return response.content.strip()
    
    elif operation == "consolidate":
        if len(memory_lines) < 10:
            return "Not enough memories to consolidate yet."
        
        messages = [
            SystemMessage(content=MEMORY_MANAGER_PROMPT),
            HumanMessage(content=CONSOLIDATE_PROMPT.format(
                count=len(memory_lines),
                memories=memories
            ))
        ]
        
        response = llm.invoke(messages)
        updated = response.content.strip()
        lines = [l.strip() for l in updated.split('\n') if l.strip()]
        
        # Cap at 20
        if len(lines) > 20:
            lines = lines[:20]
        
        write_text_file("memories.txt", '\n'.join(lines) + '\n', mode='w')
        return f"✅ Memories consolidated: {len(memory_lines)} → {len(lines)} memories"
    
    else:
        return f"Unknown operation: {operation}"


__all__ = ["memory_manager_agent"]
