# Creative Story Writer Agent 📚✨

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deep Agents](https://img.shields.io/badge/DeepAgents-0.0.8-green.svg)](https://docs.langchain.com/oss/python/deepagents/quickstart)

> An autonomous AI agent that researches current topics, writes creative short stories, and **continuously evolves** its personality, emotions, and interests based on what it learns.

## ✨ Features

- 🤖 **Fully Autonomous** - No prompts needed, just run it!
- 🔍 **Research-Driven** - Searches the web for current information
- ✍️ **Creative Writing** - Generates 500-token stories with personality
- 🌱 **Self-Evolving** - Updates its own identity files based on discoveries
- 📚 **Story Archive** - Saves all stories with timestamps
- 🎭 **Dynamic Identity** - Personality, emotions, and interests grow organically

## 🎯 What It Does

This agent autonomously:
1. **Reads its identity** from `personality.txt`, `emotions.txt`, and `topics.txt`
2. **Chooses a topic** that interests it
3. **Researches** the topic using web search
4. **Writes** a creative 500-token short story
5. **Saves** the story with a timestamp
6. **Evolves** its personality, emotions, and topics based on research insights

Every time you run it, the agent grows and changes based on what it discovers!

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Configuration](#️-configuration)
- [Example Output](#-example-output)
- [Technical Details](#️-technical-details)

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd FirstDeepAgent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your keys:
- 🔑 Get OpenAI API key from: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- 🔑 Get Tavily API key from: [tavily.com](https://tavily.com/)

### 4. Run the agent

```bash
python main.py
```

That's it! The agent will automatically create a story and save it to the `stories/` folder.

> **💡 Tip**: Run it multiple times and watch your agent evolve!

---

## 📁 Project Structure

```
FirstDeepAgent/
├── agent.py           # Agent configuration and setup
├── main.py            # Entry point - run this!
├── prompts.py         # System prompt defining agent behavior
├── tools.py           # Custom tools (search, file operations)
├── config.py          # Configuration and environment loading
├── topics.txt         # Topics the agent can write about (evolves!)
├── personality.txt    # Agent's writing personality (evolves!)
├── emotions.txt       # Emotional range for stories (evolves!)
├── stories/           # Generated stories saved here
├── requirements.txt   # Python dependencies
└── .env              # Your API keys (not in git)
```

## 🧠 How It Works

### The Agent's Identity

The agent has three core files that define its creative identity:

- **`topics.txt`** - 5-15 topics it finds interesting
- **`personality.txt`** - 10 traits that define its writing voice
- **`emotions.txt`** - 3-7 emotions it channels in stories

### The Creative Loop

Every time you run `python main.py`:

1. Agent reads its current identity files
2. Picks an interesting topic
3. Researches it via Tavily web search
4. Writes a 500-token story incorporating:
   - Its personality traits
   - Appropriate emotions
   - Subtle references to research
5. Saves story to `stories/YYYY-MM-DD_HH-MM-SS_topic.txt`
6. **Updates all three identity files** based on:
   - New topics discovered in research
   - New emotions the story explored
   - Refined personality traits

### Self-Evolution

The agent is designed to **grow and change**:
- Discovers "neural correlates of consciousness" → adds to topics
- Story explores "philosophical wonder" → adds to emotions
- Research inspires analytical style → refines personality

Over time, the agent develops its own unique voice and interests!

---

## ⚙️ Configuration

### Environment Variables

Edit `.env` to customize:

```env
# Required
OPENAI_API_KEY=sk-...          # Your OpenAI API key
TAVILY_API_KEY=tvly-...        # Your Tavily API key

# Optional (defaults shown)
OPENAI_MODEL=gpt-4o-mini       # Model to use
MAX_OUTPUT_TOKENS=512          # Max tokens per response
MAX_SEARCHES=3                 # Max web searches per run
DEFAULT_SEARCH_MAX_RESULTS=5   # Results per search
```

### Customizing the Agent

Edit the identity files to change the agent:

**`topics.txt`** - Add topics you want it to explore:
```
AI consciousness and ethics
Human-machine relationships
Quantum computing frontiers
```

**`personality.txt`** - Define its writing voice:
```
Direct and curious
Questions everything, seeks deeper meaning
Balances emotion with clarity
```

**`emotions.txt`** - Set its emotional palette:
```
Wonder and curiosity
Melancholy hope
Quiet intensity
```

---

## 📖 Example Output

The agent creates stories like:

**`stories/2025-12-17_17-38-26_AI_Consciousness.txt`**
```
In a dimly lit lab humming with the quiet pulse of servers, 
Mira stared at the screen. The AI before her wasn't just 
spitting out answers—it was reflecting, hesitating, almost... 
aware...
```

Each story:
- ✅ Max 500 tokens
- ✅ Incorporates personality traits
- ✅ Channels specific emotions
- ✅ References current research
- ✅ Has a clear narrative arc

---

## 🛠️ Technical Details

### Built With

- **Deep Agents** - LangChain's agentic framework with planning & file tools
- **OpenAI GPT-4** - Language model for story generation
- **Tavily** - AI-optimized web search API
- **LangGraph** - Agent workflow orchestration

### Architecture

- **StateBackend** - Manages agent's file system state
- **Custom Tools** - Internet search, file operations, timestamps
- **System Prompt** - Defines autonomous behavior and evolution logic

---

## 🤝 Contributing

This is a personal project, but feel free to fork and experiment! Ideas:
- Add more tool integrations
- Implement different evolution strategies
- Create visualization of agent's growth over time
- Add story quality metrics

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🙏 Acknowledgments

Built with:
- 🦜 [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/quickstart)
- 🤖 [OpenAI](https://openai.com)
- 🔍 [Tavily](https://tavily.com)

---

<div align="center">

**⭐ Star this repo if you find it interesting!**

*This agent evolves autonomously. Run it regularly and watch it develop its own unique creative voice!* 🌱

</div>

