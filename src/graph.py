from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

import getpass
import os
import logging
import tweepy

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="tweet_agent.log",
)

load_dotenv()

# Initialise LLM 
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
  
# Initialize the chat model with the Google Gemini API key
model = init_chat_model("gemini-2.5-pro", model_provider="google_genai")

# Class for passing state across nodes
class State(TypedDict):
    topic: str  
    description: str
    body: str
    messages: Annotated[list[AnyMessage], add_messages]

## Functions for nodes

# Function to generate a tweet
def generate_tweet(state: State):
    """
    This Function will call llm to generate a tweet.
    """
    logging.debug(f"Generating tweet content using LLM")
    
    topic = state.get("topic", "general topic")
    tweet_generation_prompt = f"Generate a short but creative tweet about{topic}, no options just one tweet with 2 appropriate hashtags."
    
    response = model.invoke(tweet_generation_prompt)
    logging.debug(f"GenerateTweet, LLM response: {response}")
    
    # Return proper state update
    return {
        "messages": [response], 
        "body": response.content if hasattr(response, 'content') else str(response),
        "description": f"This is a tweet about {topic}"
    }

# Function to post a tweet 
def post_tweet(state: State):
    """
    This Function will call twitter api tool to post a tweet.
    """
    tweet_content = state.get("body", "")
    logging.debug(f"postTweet, Posting tweet: {tweet_content}")
    
    try:
        # 1. Get credentials from environment variables
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET") 
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
        
        # Check if all credentials are available
        if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
            raise ValueError("Missing Twitter API credentials in environment variables")
        
        # 2. Use tweepy.Client for v2 API 
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )
        
        # 3. Post the tweet using v2 API
        response = client.create_tweet(text=tweet_content)
        
        logging.debug(f"Tweet posted successfully. Tweet Response: {response}")
        
        return {
            "description": f"Tweet posted successfully with ID: {response.data['id']}",
            "tweet_id": response.data['id']
        }
        
    except Exception as e:
        error_msg = f"Failed to post tweet: {str(e)}"
        logging.error(error_msg)
        
        return {
            "description": f"Failed to post tweet: {str(e)}",
            "error": str(e)
        }

# function to build graph
def create_graph():
    # Topic input from user
    topic = input("Enter the topic for the tweet: ")
    
    # initialize the state graph    
    graph_builder = StateGraph(State)

    # Define the nodes in the graph
    graph_builder.add_node("generate_tweet", generate_tweet)
    graph_builder.add_node("post_tweet", post_tweet)

    # Define the edges in the graph
    graph_builder.add_edge(START, "generate_tweet")
    graph_builder.add_edge("generate_tweet", "post_tweet")
    graph_builder.add_edge("post_tweet", END)

    # Compile the graph
    graph = graph_builder.compile()
    
    # Create initial state instance
    initial_state = {
        "topic": topic,
        "description": "",
        "body": "",
        "messages": []
    }
    
    # Invoke graph with proper state instance
    result = graph.invoke(initial_state)
    return result
