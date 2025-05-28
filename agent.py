from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image, display
from langchain_openai import ChatOpenAI
import uuid
from utils.logger import setup_logger
from dotenv import load_dotenv
load_dotenv()

# --- Logger ---
logger = setup_logger("agent")

# --- Tools ---
class ToolManager:
    def __init__(self):
        self.tools = [self.wiki_search, self.web_search]

    @tool
    def wiki_search(input: str) -> str:
        """Search Wikipedia for a query and return maximum 2 results.
        
        Args:
            input: The search query."""
        try:
            search_docs = WikipediaLoader(query=input, load_max_docs=2).load()
            formatted_search_docs = "\n\n---\n\n".join(
                [
                f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
                for doc in search_docs
            ])
            return formatted_search_docs
        except Exception as e:
            logger.exception(f"Error in wiki_search: {e}")
            return "Error occurred while searching Wikipedia. Please try again."

    @tool
    def web_search(input: str) -> str:
        """Search the web using Tavily for a query and return maximum 3 results.
        
        Args:
            input: The search query."""
        try:
            search_docs = TavilySearchResults(max_results=3).invoke(input)
            formatted_search_docs = "\n\n---\n\n".join(
                [
                    f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
                    for doc in search_docs
                ]
            )
            return formatted_search_docs
        except Exception as e:
            logger.exception(f"Error in web_search: {e}")
            return "Error occurred while searching the web. Please try again."
    
# --- Assistant Node ---
class AssistantAgent:
    def __init__(self, tools):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.llm_with_tools = self.llm.bind_tools(tools)
        self.system_message = self._load_system_prompt()
        logger.info(f"Initialized {self.llm.model_name} Assistant with tools.")

    def _load_system_prompt(self) -> SystemMessage:
        with open("system_prompt.txt", "r") as file:
            return SystemMessage(content=file.read())

    def run(self, state: MessagesState):
        logger.info(f"Invoking assistant with {len(state['messages'])} messages.")
        return {"messages": [self.llm_with_tools.invoke([self.system_message] + state["messages"])]}
    
# --- Graph ---
class AgentGraphBuilder:
    def __init__(self, assistant_fn, tools):
        self.assistant_fn = assistant_fn
        self.tools = tools
        self.memory = MemorySaver()

    def build(self):
        builder = StateGraph(MessagesState)

        # Define nodes
        builder.add_node("assistant", self.assistant_fn)
        builder.add_node("tools", ToolNode(self.tools))

        # Define flow
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant", tools_condition)
        builder.add_edge("tools", "assistant")

        graph = builder.compile(checkpointer=self.memory)
        logger.info(f"Graph Build Successfull! {len(self.tools)} tools added.")
        return graph
    
# --- Main ---
def agent_graph():
    # Initialize tools
    tool_manager = ToolManager()
    tools = tool_manager.tools

    # Initialize assistant LLM
    assistant_agent = AssistantAgent(tools)

    # Build graph
    graph_builder = AgentGraphBuilder(assistant_agent.run, tools)
    graph = graph_builder.build()
    return graph

# --- Test ---
if __name__ == "__main__":
    graph = agent_graph()

    question = "Hi!"
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    logger.info(f"[Thread ID: {thread_id}] Received question: {question}")

    messages = [HumanMessage(content=question)]
    response = graph.invoke({"messages": messages}, config)

    logger.info(f"[Thread ID: {thread_id}] Received response from assistant: {response['messages'][-1].content}")

    for m in response['messages']:
        m.pretty_print()