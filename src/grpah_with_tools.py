from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os

load_dotenv()

# Simple state class
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Global variables
mcp_client = None
model_with_tools = None
tools = None

# Function to setup MCP client and bind model with tools.
async def setup_mcp_client():
    """Initialize MCP client and model with tools."""
    global mcp_client, model_with_tools, tools
    # Initialize model
    model = init_chat_model("gemini-2.5-pro", model_provider="google_genai")
    
    # Setup MCP client
    mcp_client = MultiServerMCPClient({
        "twitter_server": {
            "command": "python",
            "args": ["/Users/surya/Developer/python/mcp-servers/servers/twitter_server.py"],
            "transport": "stdio",
            "env": {
            "API_KEY": "GrH6k5zAVpWAAwd3Am7Bxrpjm",
            "API_SECRET": "CvGIrzr3a8bE5kxbmWAChqi9TbsFlVmy3CPm5uscXGhZCuxMln",
            "ACCESS_TOKEN": "1951276371625517056-8H4wQE5bEPrE7xOWowSf7x09rNNy5N",
            "ACCESS_TOKEN_SECRET": "6OWCXhM4MPuIvJPzhVQvCf01t6BqibC4AjJLiscbr2Kr6",
            "TWITTER_BEARER_TOKEN": "AAAAAAAAAAAAAAAAAAAAAKJ03QEAAAAAflVKFBqvMUTy6QOpnjuYAo4%2Bub0%3DAhHbuszLoqpPVphbW6C2jwWWLo5xaWxxGoX4w0DiEMjnyhptHR"
                }
        }
    })
    
    # Get tools and bind to model
    tools = await mcp_client.get_tools()
    model_with_tools = model.bind_tools(tools)
    
# Function for node logic
async def llm_node(state: State):
    """LLM node that can call tools."""
    response = await model_with_tools.ainvoke(state["messages"])
    return {"messages": [response]}

async def run_agent():
    """Main function to run the Twitter agent."""
    
    # Setup MCP
    await setup_mcp_client()
    
    # Build graph - Use async nodes directly
    builder = StateGraph(State)
    builder.add_node("llm", llm_node)  # Remove sync_wrapper
    builder.add_node("tools", ToolNode(tools))  # Remove sync_wrapper
    
    # Add edges
    builder.add_edge(START, "llm")
    builder.add_conditional_edges(
        "llm",
        tools_condition
    )
    builder.add_edge("tools", "llm")
    
    # Compile graph
    graph = builder.compile()
    
    # Get user input
    user_input = input("What would you like me to do? : ")
    
    # Run the graph - Use ainvoke for async
    result = await graph.ainvoke({
        "messages": [HumanMessage(content=f"""You are a Twitter agent. 
        User request: {user_input}
        
        If this involves posting a tweet, use the post_tweet tool immediately with appropriate content.""")]
    })
    
    # Print result
    if result["messages"]:
        final_message = result["messages"][-1]
        print("\n🐦 Response:", final_message.content)

def main():
    """Entry point."""
    
    # Use asyncio.run() only at the top level
    asyncio.run(run_agent())
    
if __name__ == "__main__":
    main()
