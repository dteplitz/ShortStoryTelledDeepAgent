import os
from datetime import datetime
from typing import List, Literal

from tavily import TavilyClient

from config import DEFAULT_SEARCH_MAX_RESULTS, MAX_SEARCHES

search_counter = 0
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def internet_search(
    query: str,
    max_results: int = DEFAULT_SEARCH_MAX_RESULTS,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
) -> str:
    """Run a web search"""
    global search_counter
    if search_counter >= MAX_SEARCHES:
        return f"Search limit reached ({MAX_SEARCHES}). Summarize with current context."

    search_counter += 1
    result = tavily_client.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=include_raw_content,
    )

    summaries: List[str] = []
    for item in result.get("results", []):
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        summary = item.get("content", "")[:400]
        summaries.append(f"- {title} :: {url}\n  {summary}")

    return "Search results:\n" + "\n".join(summaries)


def read_text_file(path: str) -> str:
    """Read text from a file on the real filesystem."""
    if os.path.isabs(path):
        return "Refusing to read absolute paths."
    if not os.path.exists(path):
        return f"{path} does not exist."

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text_file(path: str, content: str, mode: str = "w") -> str:
    """Write text to a file on the real filesystem. Mode can be 'w' (overwrite) or 'a' (append)."""
    # Convert absolute paths within project to relative
    if os.path.isabs(path):
        project_dir = os.getcwd()
        if path.startswith(project_dir):
            path = os.path.relpath(path, project_dir)
        else:
            return f"Cannot write to paths outside project directory. Use relative paths like 'stories/file.txt'"
    
    if mode not in {"w", "a"}:
        return "Mode must be 'w' or 'a'."

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, mode, encoding="utf-8") as f:
        f.write(content)
    return f"Wrote {len(content)} chars to {path}"


def list_files(directory: str = ".") -> str:
    """List all files in the specified directory on the real filesystem."""
    if os.path.isabs(directory):
        return "Refusing to access absolute paths."
    
    if not os.path.exists(directory):
        return f"Directory {directory} does not exist."
    
    try:
        files = []
        for item in os.listdir(directory):
            path = os.path.join(directory, item)
            if os.path.isfile(path):
                size = os.path.getsize(path)
                files.append(f"{item} ({size} bytes)")
            elif os.path.isdir(path):
                files.append(f"{item}/ (directory)")
        
        if not files:
            return f"No files found in {directory}"
        
        return f"Contents of {directory}:\n" + "\n".join(sorted(files))
    except Exception as e:
        return f"Error listing directory: {str(e)}"


def get_timestamp() -> str:
    """Get current timestamp in YYYY-MM-DD_HH-MM-SS format."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def reset_tool_counters() -> None:
    """Reset per-run counters (e.g., search limits)."""
    global search_counter
    search_counter = 0


# Provide custom tools to access real filesystem files
# StateBackend is for virtual filesystem, but we need real file access
tools = [
    internet_search,
    read_text_file,
    write_text_file,
    list_files,
    get_timestamp
]

