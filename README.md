# Botato 🥔

Botato is an intelligent AI assistant built using LangGraph and LangChain, designed to provide accurate and helpful responses by leveraging web search and Wikipedia knowledge. The agent maintains a conversational flow while ensuring information accuracy and proper source attribution.

## Features ✨

- **Web Search Integration**: Powered by Tavily Search API for real-time web information
- **Wikipedia Knowledge**: Direct access to Wikipedia articles for factual information
- **Conversational Memory**: Maintains context throughout the conversation
- **Error Handling**: Robust error management and logging system
- **Modular Architecture**: Built with LangGraph for flexible and maintainable code structure

## Prerequisites 📋

- Python 3.8+
- OpenAI API key
- Tavily API key

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/ramiyappan/Botato.git
cd Botato
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Usage 💡

```python
from agent import agent_graph

# Initialize the agent
graph = agent_graph()

# Ask a question
question = "What is the capital of France?"
messages = [HumanMessage(content=question)]
response = graph.invoke({"messages": messages})

# Get the response
print(response['messages'][-1].content)
```

## Project Structure 📁

```
.
├── app.py              # Streamlit Frontend app
├── agent.py            # Main agent implementation
├── system_prompt.txt   # System instructions for the agent
├── notebooks/          # Jupyter notebooks for development
├── utils/              # Utility functions
    ├── logger.py       # Setup logging
├── logs/               # Log files
└── venv/               # Virtual environment
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [OpenAI](https://openai.com/)
- [Tavily](https://tavily.com/) 
