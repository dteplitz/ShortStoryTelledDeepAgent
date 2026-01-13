# Memory System - Long-term Episodic Memory

## Overview

The Memory Manager is a sub-agent that simulates human-like long-term memory with natural imperfection. It stores, retrieves, and consolidates memories over time, allowing the agent to build a sense of continuity and learning from past experiences.

## Philosophy

Human memory is **reconstructive, not reproductive**. We don't record experiences perfectly - we:
- Simplify details over time
- Merge similar experiences
- Sometimes shift minor details
- Remember emotionally significant moments more vividly
- Forget trivial information

The Memory Manager intentionally mimics these characteristics.

## File

**`memories.txt`** - Stores 15-20 episodic memories, one per line.

## Operations

### 1. **Store Memory**

Save a new significant experience.

```python
memory_manager_agent(
    operation="store",
    experience="Discovered that quantum entanglement creates fascinating narrative tension",
    context="quantum physics story"
)
```

**Behavior:**
- Adds new memory
- If at 20 memories, may merge similar ones
- Each memory is a concise statement

### 2. **Retrieve Memories**

Get relevant memories for a query.

```python
memory_manager_agent(
    operation="retrieve",
    query="writing about consciousness"
)
```

**Returns:**
- 3-5 most relevant memories
- "No relevant memories found" if none match
- Memories may have slight imperfections

### 3. **Consolidate Memories**

Merge and simplify memories naturally.

```python
memory_manager_agent(operation="consolidate")
```

**Behavior:**
- Merges similar memories
- Simplifies overly detailed ones
- Keeps emotionally significant moments vivid
- Forgets trivial details
- Allows slight creative shifts (natural memory distortion)

**Recommended frequency:** Every 3-4 stories

## Integration in Workflow

### Before Writing (Step 2):
```python
# Retrieve relevant memories
memories = memory_manager_agent(
    operation="retrieve",
    query="AI and consciousness themes"
)
# Let these subtly inform your perspective
```

### After Writing (Step 8):
```python
# Store what you learned
memory_manager_agent(
    operation="store",
    experience="Writing about AI caregivers revealed empathy as a central tension point",
    context="AI consciousness"
)
```

### Periodically (Step 10):
```python
# Every 3-4 stories, consolidate
memory_manager_agent(operation="consolidate")
```

## Memory Characteristics

### Imperfection is Natural

Memories are **not** a perfect database. They:
- Fade over time
- Get simplified
- Sometimes blend together
- May shift slightly in details

This is **intentional** - it makes the agent more human-like.

### What Gets Remembered

Good candidates for storage:
- ✅ Key insights from writing a story
- ✅ Emotional moments during creation
- ✅ Interesting narrative techniques discovered
- ✅ Connections between topics
- ✅ Personal growth realizations

Not worth storing:
- ❌ Routine procedural steps
- ❌ Technical details (covered by research)
- ❌ Trivial observations

### Memory Limit: 15-20 Items

Why the limit?
- Forces meaningful selection
- Encourages consolidation
- Prevents information overload
- Mirrors human working memory constraints

## Example Memories

Good memory entries:
```
Writing about quantum uncertainty helped me embrace ambiguity in storytelling
The tension between human emotion and AI logic creates compelling narratives
Stories about consciousness work best when leaving questions unanswered
Discovered that philosophical topics need concrete characters to stay engaging
Melancholy hope pairs beautifully with technological themes
```

## Temperature Setting

The Memory Manager uses **temperature=0.5** (higher than other managers) to:
- Allow natural variation in recall
- Enable creative consolidation
- Simulate memory imperfection
- Prevent mechanical precision

## Technical Details

### File Location
```
memories.txt
```

### Format
```
One memory per line
Simple, concise statements
No timestamps (memories fade into timelessness)
15-20 memories maximum
```

### Hard Caps
- **Store:** Caps at 20 memories
- **Consolidate:** Targets 15-20 range
- **Retrieve:** Returns 3-5 most relevant

## Benefits

1. **Continuity** - Agent builds on past experiences
2. **Depth** - Stories informed by accumulated wisdom
3. **Evolution** - Learning compounds over time
4. **Humanity** - Imperfect memory feels more authentic
5. **Context** - Past informs present in subtle ways

## When to Use Each Operation

### Store
- **After every story** (Step 8)
- Record key learnings and insights

### Retrieve
- **Before selecting topic** (Step 2)
- When wanting to draw on past experiences
- Optional but encouraged

### Consolidate
- **Every 3-4 stories** (Step 10)
- When memories file grows past 15 items
- To keep memory lean and meaningful

## Example Session

```python
# Story 1: Write about AI consciousness
retrieve → "No memories yet"
write → story
store → "AI characters need human-like flaws to be compelling"

# Story 2: Write about quantum physics
retrieve → "No relevant memories" 
write → story
store → "Uncertainty principle creates natural narrative tension"

# Story 3: Write about human-AI connection
retrieve → "AI characters need human-like flaws to be compelling"
write → story (influenced by memory)
store → "Emotional connection forms when both sides show vulnerability"

# Story 4: Write about consciousness again
retrieve → "AI characters need human-like flaws..." 
          "Emotional connection forms when both sides show vulnerability"
write → story (deeper, informed by past)
store → "Consciousness stories explore identity through relationships"
consolidate → Merge similar memories, simplify

# Memories now richer, more connected, slightly imperfect
```

## Philosophy

> "Memory is not a recording device but a storytelling mechanism."
> - Daniel Schacter

The Memory Manager embraces this. It's not perfect archival storage - it's a **narrative system** that helps the agent develop a coherent sense of self over time, with all the beautiful imperfections that make memory human.

---

**Status:** Implemented in Phase 3.5 (Memory System)  
**File:** `sub_agents/memory_manager.py`  
**Integration:** `prompts.py` (Steps 2, 8, 10)
