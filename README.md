# Deep Research - AI-Powered Research Assistant

A sophisticated multi-agent AI research system that conducts in-depth research on any topic using intelligent agents and web scraping capabilities.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized AI agents for different research tasks
- **Intelligent Query Generation**: Automatically generates multiple targeted search queries
- **Web Content Extraction**: Advanced web scraping with content filtering
- **Rich Console Interface**: Beautiful terminal UI with progress indicators
- **Comprehensive Reporting**: Structured research summaries and insights

## 🏗️ Architecture

The system uses a **coordinator pattern**  with specialized agents:

### Research Agents

1. **Query Agent** (`research_agents/query_agent.py`)
   - Analyzes research topics
   - Generates multiple targeted search queries
   - Provides strategic research direction

2. **Search Agent** (`research_agents/search_agent.py`)
   - Extracts clean content from web pages
   - Filters out navigation and UI elements
   - Focuses on main content areas
   - Summarizes findings into concise reports

3. **Report Agent** (`research_agents/report_agent.py`)
   - Synthesizes information from multiple sources
   - Creates structured research reports
   - Provides comprehensive analysis

### Core Components

- **ResearchCoordinator** (`coordinator.py`): Orchestrates the research workflow
- **SearchResult** (`models/search_result.py`): Data model for search results
- **Main Interface** (`main.py`): Interactive command-line interface

## 📋 Requirements

- Python 3.12+
- OpenAI API key (for AI agents)
- Internet connection (for web research)

## 🛠️ Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd deep_research
   ```

2. **Install dependencies using uv** (recommended)
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🚀 Usage

### Interactive Mode

Run the main application:
```bash
uv run python main.py
```

The system will prompt you for a research topic and guide you through the process.

### Example Research Flow

1. **Topic Input**: "Climate change impacts on agriculture"
2. **Query Generation**: AI generates focused search queries
3. **Web Research**: Searches and analyzes multiple sources
4. **Content Analysis**: Extracts and summarizes key information
5. **Report Generation**: Compiles comprehensive research report

### Programmatic Usage

```python
import asyncio
from coordinator import ResearchCoordinator

async def research_topic(topic: str):
    coordinator = ResearchCoordinator(topic)
    results = await coordinator.research()
    return results

# Run research
results = asyncio.run(research_topic("artificial intelligence trends"))
```

## 📁 Project Structure

```
deep_research/
├── coordinator.py              # Main research orchestrator
├── main.py                    # CLI interface
├── models/
│   └── search_result.py       # Data models
├── research_agents/
│   ├── query_agent.py         # Query generation agent
│   ├── search_agent.py        # Web scraping agent
│   └── report_agent.py        # Report synthesis agent
├── pyproject.toml             # Project configuration
├── uv.lock                    # Dependency lock file
├── .env                       # Environment variables
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required for AI agent functionality
- `SEARCH_TIMEOUT`: Web request timeout (default: 10 seconds)
- `MAX_RESULTS_PER_QUERY`: Maximum search results per query (default: 3)

### Agent Configuration

Agents can be customized by modifying their instructions and parameters:

```python
# Example: Customize search agent behavior
SEARCH_AGENT_PROMPT = """
Custom instructions for search agent...
"""
```

## 🌟 Key Features Details

### Intelligent Web Content Extraction

The search agent uses advanced techniques to extract clean, relevant content:

- Removes navigation menus, headers, footers
- Filters out advertisements and UI elements
- Focuses on main content areas (articles, main sections)
- Handles various HTML structures intelligently

### Multi-Query Research Strategy

The query agent generates diverse search angles:

- Broad overview queries
- Specific technical queries
- Current trends and developments
- Historical context queries

### Rich Terminal Interface

Beautiful console output with:
- Progress indicators during research
- Colored output for better readability
- Structured panels for different information types
- Real-time status updates

## 🔍 Advanced Usage

### Custom Agent Development

Create specialized agents for specific domains:

```python
from agents import Agent, function_tool

@function_tool
def custom_analysis_tool(data: str) -> str:
    # Custom analysis logic
    return analysis_result

custom_agent = Agent(
    model="gpt-4",
    name="Domain Expert",
    instructions="Specialized domain instructions...",
    tools=[custom_analysis_tool]
)
```

### Batch Research

Process multiple topics:

```python
topics = ["AI ethics", "quantum computing", "sustainable energy"]
results = []

for topic in topics:
    coordinator = ResearchCoordinator(topic)
    result = await coordinator.research()
    results.append(result)
```



### Debug Mode

Enable verbose logging by setting environment variable:
```bash
export DEBUG=1
uv run python main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request



## 🙏 Acknowledgments

- Built with [OpenAI Agents SDK](https://github.com/openai/openai-agents-js)
- Web scraping powered by [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- Search functionality via [DuckDuckGo Search API](https://github.com/deedy5/duckduckgo_search)
- Rich terminal interface using [Rich](https://github.com/Textualize/rich)
-  learned from various open-source projects and special thanks to **Kody Simpson**: https://www.youtube.com/watch?v=gFcAfU3V1Zo


