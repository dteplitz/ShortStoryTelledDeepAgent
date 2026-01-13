"""Writer Agent Sub-Graph - Multi-step story generation with refinement"""
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
import operator
import re


# ============================================================================
# STATE DEFINITION
# ============================================================================

class WriterState(TypedDict):
    """State that flows through the writer sub-graph"""
    # Inputs
    topic: str
    research: str
    personality: str
    emotions: str
    memories: str
    timestamp: str
    
    # Internal state
    outline: str
    draft_story: str
    refined_story: str
    filename: str
    
    # Output
    final_story: str
    decision_log: Annotated[Sequence[str], operator.add]  # Accumulate logs


# ============================================================================
# PROMPTS
# ============================================================================

OUTLINE_PROMPT = """Create a brief story outline based on these elements:

Topic: {topic}
Research: {research}
Personality: {personality}
Emotions: {emotions}
Memories: {memories}

Instructions:
Create a 3-5 sentence outline for a 500-token story that:
- Has a clear narrative arc (beginning, development, climax, resolution)
- Focuses on the topic
- Channels 1-2 emotions authentically
- Will subtly weave in research insights

Return ONLY the outline, no explanations."""


DRAFT_PROMPT = """Write a complete story draft based on this outline and context.

Outline:
{outline}

Topic: {topic}
Research Context: {research}
Personality Traits: {personality}
Emotional Palette: {emotions}
Relevant Memories: {memories}

Instructions:
Write a 600-token story draft (we'll refine to 500) that:
1. Follows the outline structure
2. Expresses personality traits through narrative voice
3. Channels 1-2 emotions authentically
4. Subtly references research insights
5. Uses vivid, concrete imagery
6. Shows, don't tell
7. Has a satisfying conclusion

Return ONLY the story text, no meta-commentary."""


REFINE_PROMPT = """Refine this story draft to exactly 500 tokens with perfect formatting.

Draft:
{draft}

Instructions:
1. Edit to EXACTLY 500 tokens (±20 acceptable)
2. Fix any formatting issues:
   - Ensure proper possessives (e.g., "Solace's" not "Solaces")
   - Add em-dashes or commas where needed
   - Fix any concatenated words
   - Ensure proper spacing
3. Tighten prose (remove redundancy, sharpen language)
4. Strengthen opening hook and closing resonance
5. Ensure smooth flow between paragraphs

Return ONLY the refined story text."""


# ============================================================================
# FORMATTING CLEANUP
# ============================================================================

def clean_story_formatting(text: str) -> str:
    """Fix common LLM formatting issues"""
    # Fix possessives (common words)
    possessive_words = [
        "processor", "avatar", "voice", "heart", "mind", "eye", "eyes",
        "face", "hand", "hands", "body", "screen", "companion", "tablet",
        "window", "room", "world", "life", "story", "memory", "thought"
    ]
    
    for word in possessive_words:
        # Fix: "words processor" → "word's processor"
        text = re.sub(rf"(\w+)s\s+{word}", rf"\1's {word}", text)
    
    # Fix missing spaces before articles after punctuation-like endings
    text = re.sub(r'([a-z])a\s+', r'\1—a ', text)
    text = re.sub(r'([a-z])an\s+', r'\1—an ', text)
    
    # Fix missing spaces before common verbs
    text = re.sub(r'([a-z])(was|is|are|were|been|had|have|has)\b', r'\1 \2', text)
    
    # Fix double spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Ensure proper paragraph breaks
    text = text.replace('\n\n\n', '\n\n')
    
    return text.strip()


# ============================================================================
# NODE FUNCTIONS
# ============================================================================

def create_outline(state: WriterState) -> WriterState:
    """Node 1: Create story outline"""
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.6,  # Moderate creativity for planning
    )
    
    messages = [
        SystemMessage(content="You are a story outliner. Create concise, effective story structures."),
        HumanMessage(content=OUTLINE_PROMPT.format(
            topic=state["topic"],
            research=state.get("research", "(None)"),
            personality=state.get("personality", "(None)"),
            emotions=state.get("emotions", "(None)"),
            memories=state.get("memories", "(None)")
        ))
    ]
    
    response = llm.invoke(messages)
    outline = response.content.strip()
    
    state["outline"] = outline
    state["decision_log"] = [f"📝 Created story outline ({len(outline.split())} words)"]
    
    return state


def draft_story(state: WriterState) -> WriterState:
    """Node 2: Write initial story draft"""
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.7,  # Higher temp for creative writing
    )
    
    messages = [
        SystemMessage(content="You are a skilled creative fiction writer. Write vivid, emotionally resonant stories."),
        HumanMessage(content=DRAFT_PROMPT.format(
            outline=state["outline"],
            topic=state["topic"],
            research=state.get("research", "(None)"),
            personality=state.get("personality", "(None)"),
            emotions=state.get("emotions", "(None)"),
            memories=state.get("memories", "(None)")
        ))
    ]
    
    response = llm.invoke(messages)
    draft = response.content.strip()
    
    # Count tokens (rough approximation: 1 token ≈ 0.75 words)
    word_count = len(draft.split())
    token_estimate = int(word_count * 0.75)
    
    state["draft_story"] = draft
    state["decision_log"] = [f"✍️ Drafted story (~{token_estimate} tokens, {word_count} words)"]
    
    return state


def refine_and_format(state: WriterState) -> WriterState:
    """Node 3: Refine to 500 tokens and fix formatting"""
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.5,  # Lower temp for precise editing
    )
    
    messages = [
        SystemMessage(content="You are an expert editor. Refine stories to exact specifications while maintaining voice and impact."),
        HumanMessage(content=REFINE_PROMPT.format(
            draft=state["draft_story"]
        ))
    ]
    
    response = llm.invoke(messages)
    refined = response.content.strip()
    
    # Apply formatting cleanup
    formatted = clean_story_formatting(refined)
    
    # Count final tokens
    word_count = len(formatted.split())
    token_estimate = int(word_count * 0.75)
    
    state["refined_story"] = formatted
    state["decision_log"] = [f"🔧 Refined and formatted (~{token_estimate} tokens, {word_count} words)"]
    
    return state


def save_story(state: WriterState) -> WriterState:
    """Node 4: Save the final story to file"""
    from tools import write_text_file
    
    # Create filename from topic and timestamp
    topic_slug = state["topic"].lower().replace(" ", "_").replace("-", "_")
    topic_slug = re.sub(r'[^a-z0-9_]', '', topic_slug)  # Remove special chars
    topic_slug = topic_slug[:50]  # Limit length
    
    filename = f"stories/{state['timestamp']}_{topic_slug}.txt"
    
    # Write the story
    write_text_file(filename, state["refined_story"], mode='w')
    
    state["filename"] = filename
    state["final_story"] = state["refined_story"]
    state["decision_log"] = [f"💾 Saved to: {filename}"]
    
    return state


# ============================================================================
# BUILD THE GRAPH
# ============================================================================

def build_writer_subgraph():
    """Build and compile the writer sub-graph"""
    
    graph = StateGraph(WriterState)
    
    # Add nodes in sequence
    graph.add_node("outline", create_outline)
    graph.add_node("draft", draft_story)
    graph.add_node("refine", refine_and_format)
    graph.add_node("save", save_story)
    
    # Entry point
    graph.set_entry_point("outline")
    
    # Linear workflow
    graph.add_edge("outline", "draft")
    graph.add_edge("draft", "refine")
    graph.add_edge("refine", "save")
    graph.add_edge("save", END)
    
    return graph.compile()


# ============================================================================
# TOOL INTERFACE
# ============================================================================

# Compile the graph once at module load
writer_subgraph = build_writer_subgraph()


def writer_subgraph_tool(
    topic: str,
    research: str = "",
    personality: str = "",
    emotions: str = "",
    memories: str = "",
    timestamp: str = ""
) -> str:
    """
    Tool: Multi-step story writer using LangGraph sub-graph
    
    Workflow:
    1. Create outline - Plan narrative structure
    2. Draft story - Write 600-token initial draft
    3. Refine - Edit to 500 tokens, fix formatting
    4. Save - Write to stories/ directory
    
    Args:
        topic: The story's central topic
        research: Research summary and key facts
        personality: Writer's personality traits
        emotions: Emotional palette to channel
        memories: Relevant memories (optional)
        timestamp: Current timestamp for filename
        
    Returns:
        Complete story text with decision log
    """
    
    # Invoke the sub-graph
    result = writer_subgraph.invoke({
        "topic": topic,
        "research": research,
        "personality": personality,
        "emotions": emotions,
        "memories": memories,
        "timestamp": timestamp,
        "outline": "",
        "draft_story": "",
        "refined_story": "",
        "filename": "",
        "final_story": "",
        "decision_log": []
    })
    
    # Format response with decision log
    log = "\n".join(result["decision_log"])
    
    return f"{result['final_story']}\n\n---\nGeneration Log:\n{log}"


__all__ = ["writer_subgraph_tool", "writer_subgraph"]
