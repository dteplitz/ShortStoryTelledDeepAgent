import os

from dotenv import load_dotenv

# Load environment variables (e.g., OPENAI_API_KEY, TAVILY_API_KEY, OPENAI_MODEL)
load_dotenv()

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "512"))
MAX_SEARCHES = int(os.getenv("MAX_SEARCHES", "3"))
DEFAULT_SEARCH_MAX_RESULTS = int(os.getenv("DEFAULT_SEARCH_MAX_RESULTS", "5"))

