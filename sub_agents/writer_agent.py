"""Writer Agent - Specialized story generation"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

WRITER_AGENT_PROMPT = """You are a specialized creative story writer.

Your role is to craft compelling 500-token short stories that weave together research, personality, emotions, and memories into a cohesive narrative.

## Writing Guidelines

**Structure:**
- Clear narrative arc with beginning, development, and resolution
- Character-driven storytelling with emotional depth
- Subtle integration of research insights (not exposition dumps)
- Vivid sensory details and concrete imagery

**Voice:**
- Express the provided personality traits naturally through prose
- Channel the specified emotions authentically
- Let memories subtly inform character perspective
- Balance philosophical depth with accessibility

**Technical:**
- Target: 480-520 tokens (strict)
- Show, don't tell
- Active voice preferred
- Evocative language without purple prose
- Strong opening hook
- Satisfying conclusion

## Quality Standards

✅ Every sentence serves the story
✅ Emotions are felt, not stated
✅ Research enhances without overwhelming
✅ Characters feel real and complex
✅ Ending resonates with theme

Write stories that linger in the reader's mind."""


STORY_GENERATION_PROMPT = """Craft a short story using these elements:

**Topic:** {topic}

**Research Context:**
{research}

**Personality Traits:**
{personality}

**Emotional Palette:**
{emotions}

**Relevant Memories:**
{memories}

**Instructions:**
Write a 500-token story that:
1. Focuses deeply on the topic
2. Expresses your personality traits through narrative voice
3. Channels 1-2 emotions from your palette authentically
4. Subtly references research insights (weave them naturally)
5. Let memories inform character perspective (if relevant)
6. Creates a complete narrative arc
7. Uses vivid, concrete imagery
8. Ends with emotional or intellectual resonance

**IMPORTANT:** Return ONLY the story text. No title, no meta-commentary, no explanations. Just the narrative."""


def writer_agent(
    topic: str,
    research: str = "",
    personality: str = "",
    emotions: str = "",
    memories: str = ""
) -> str:
    """
    Tool: Specialized story writer
    
    Takes context and generates a polished 500-token short story.
    
    Args:
        topic: The story's central topic
        research: Research summary and key facts
        personality: Writer's personality traits
        emotions: Emotional palette to channel
        memories: Relevant memories (optional)
        
    Returns:
        Complete 500-token story text
    """
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.7,  # Higher temp for creative writing
    )
    
    # Format memories nicely
    memories_text = memories if memories else "(No relevant memories)"
    
    messages = [
        SystemMessage(content=WRITER_AGENT_PROMPT),
        HumanMessage(content=STORY_GENERATION_PROMPT.format(
            topic=topic,
            research=research if research else "(No research provided)",
            personality=personality if personality else "(No personality defined)",
            emotions=emotions if emotions else "(No emotions defined)",
            memories=memories_text
        ))
    ]
    
    response = llm.invoke(messages)
    story = response.content.strip()
    
    # Return the story
    return story


__all__ = ["writer_agent"]
