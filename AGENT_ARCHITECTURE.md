# Agent Architecture - All Access Through Agents

## Core Principle

**All file access goes through specialized agents.** The main orchestrator never reads or writes identity files directly.

## Architecture

```
Main Orchestrator (Deep Agent)
├─ Uses tools for:
│  ├─ write_text_file() - ONLY for story files
│  ├─ get_timestamp()
│  └─ list_files()
│
└─ Delegates to Sub-Agents for:
   ├─ research_agent - Web research
   ├─ memory_manager_agent - memories.txt
   ├─ emotions_manager_agent - emotions.txt
   ├─ topics_manager_agent - topics.txt
   └─ personality_manager_agent - personality.txt
```

## File Access Rules

### ✅ Allowed (Main Agent)
- **Write** story files to `stories/` directory
- **List** directories
- **Get** timestamps

### ❌ Not Allowed (Main Agent)
- **Read** identity files directly
- **Write** identity files directly
- **Access** memories.txt

### ✅ Required (Through Agents)
- **All** identity file access
- **All** memory operations

## Sub-Agent Operations

### 1. Research Agent
```python
research_agent(topic)
→ Returns: SUMMARY, KEY_FACTS, DISCOVERED_TOPICS
```

### 2. Memory Manager
```python
# Get memories
memory_manager_agent(operation="retrieve", query="theme")

# Store memory
memory_manager_agent(operation="store", experience="...", context="...")

# Consolidate
memory_manager_agent(operation="consolidate")
```

### 3. Emotions Manager
```python
# Get emotions
emotions_manager_agent(operation="retrieve")

# Evolve emotions
emotions_manager_agent(operation="evolve", story_content="...")
```

### 4. Topics Manager
```python
# Get topics
topics_manager_agent(operation="retrieve")

# Evolve topics
topics_manager_agent(operation="evolve", research_content="...", topic_used="...")
```

### 5. Personality Manager
```python
# Get personality
personality_manager_agent(operation="retrieve")

# Refine personality
personality_manager_agent(operation="refine", story_content="...", topic="...")
```

## Benefits

### 1. **Separation of Concerns**
- Orchestrator focuses on workflow
- Specialists handle domain logic

### 2. **Encapsulation**
- File format changes don't affect orchestrator
- Evolution logic stays in specialized agents

### 3. **Consistency**
- All identity management follows same pattern
- Predictable interface across all managers

### 4. **Safety**
- No accidental direct file writes
- Agents enforce size limits and rotation

### 5. **Observability**
- LangSmith traces show clear agent calls
- Easy to debug which agent did what

## Workflow Example

```python
# 1. Load identity through agents
personality = personality_manager_agent(operation="retrieve")
emotions = emotions_manager_agent(operation="retrieve")
topics = topics_manager_agent(operation="retrieve")

# 2. Retrieve memories through agent
memories = memory_manager_agent(operation="retrieve", query="consciousness")

# 3. Research through agent
research = research_agent("AI consciousness")

# 4. Write story (direct file write to stories/)
timestamp = get_timestamp()
write_text_file(f"stories/{timestamp}_story.txt", story)

# 5. Store memory through agent
memory_manager_agent(operation="store", experience="...", context="...")

# 6. Evolve identity through agents
emotions_manager_agent(operation="evolve", story_content=story)
topics_manager_agent(operation="evolve", research_content=research, topic_used=topic)
personality_manager_agent(operation="refine", story_content=story, topic=topic)
```

## Agent Responsibilities

| Agent | File | Read | Write | Operations |
|-------|------|------|-------|------------|
| **research_agent** | - | - | - | Research only |
| **memory_manager** | memories.txt | ✅ | ✅ | retrieve, store, consolidate |
| **emotions_manager** | emotions.txt | ✅ | ✅ | retrieve, evolve |
| **topics_manager** | topics.txt | ✅ | ✅ | retrieve, evolve |
| **personality_manager** | personality.txt | ✅ | ✅ | retrieve, refine |
| **main_orchestrator** | stories/*.txt | ❌ | ✅ | Write stories only |

## Why This Design?

### Traditional Approach (Rejected)
```python
# Main agent reads files directly
personality = read_text_file("personality.txt")
emotions = read_text_file("emotions.txt")

# Main agent writes files directly  
write_text_file("emotions.txt", updated_emotions)
```

**Problems:**
- ❌ No encapsulation
- ❌ Evolution logic in prompts
- ❌ File format exposed to orchestrator
- ❌ Hard to maintain size limits
- ❌ Difficult to add features (like memory distortion)

### Our Approach (Implemented)
```python
# All access through agents
personality = personality_manager_agent(operation="retrieve")
emotions = emotions_manager_agent(operation="retrieve")

# Evolution through agents
emotions_manager_agent(operation="evolve", story_content=story)
```

**Benefits:**
- ✅ Full encapsulation
- ✅ Evolution logic in agent code
- ✅ File format hidden from orchestrator
- ✅ Agents enforce limits automatically
- ✅ Easy to add features (memory already distorts naturally)

## LangSmith Tracing

With this architecture, traces are clean and hierarchical:

```
Main Agent Run
├─ Tool: personality_manager_agent (operation=retrieve)
│  └─ Returns: [personality traits]
├─ Tool: emotions_manager_agent (operation=retrieve)
│  └─ Returns: [emotions]
├─ Tool: topics_manager_agent (operation=retrieve)
│  └─ Returns: [topics]
├─ Tool: memory_manager_agent (operation=retrieve, query=...)
│  └─ LLM Call: Find relevant memories
├─ Tool: research_agent
│  ├─ LLM Call: Generate queries
│  ├─ Tool: internet_search
│  ├─ Tool: internet_search
│  └─ LLM Call: Synthesize
├─ Tool: get_timestamp
├─ Tool: write_text_file (story)
├─ Tool: memory_manager_agent (operation=store)
│  └─ LLM Call: Store memory
├─ Tool: emotions_manager_agent (operation=evolve)
│  └─ LLM Call: Evolve emotions
├─ Tool: topics_manager_agent (operation=evolve)
│  └─ LLM Call: Evolve topics
└─ Tool: personality_manager_agent (operation=refine)
   └─ LLM Call: Refine personality
```

Clear, hierarchical, and easy to understand!

## Summary

**Golden Rule:** The orchestrator delegates all identity management to specialized agents.

- **Read identity?** → Use agent with operation="retrieve"
- **Write identity?** → Use agent with operation="evolve/refine/store"
- **Write story?** → Direct file write (that's the output)

This architecture keeps concerns separated, code maintainable, and the system extensible.

---

**Status:** Implemented  
**Last Updated:** 2026-01-13
