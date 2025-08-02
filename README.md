Tweet Agent - AI-Powered Social Media Automation
An intelligent AI agent designed for Twitter automation using LangGraph, LangChain, and LangSmith. This project leverages cutting-edge AI agent frameworks to create sophisticated social media interactions and content generation.
🚀 Features
	•	AI-Powered Tweet Generation: Automatically generates contextually relevant tweets using advanced language models
	•	Multi-Agent System: Utilizes LangGraph for complex agent orchestration and workflow management
	•	Twitter API Integration: Seamless integration with Twitter API for posting and social media interactions
	•	Research Assistance: Built-in research capabilities for content creation and trend analysis
	•	Comprehensive Logging: Robust logging system for monitoring agent performance and debugging
	•	OAuth Authentication: Secure Twitter authentication with OAuth troubleshooting capabilities
🛠️ Tech Stack
	•	LangChain: Core framework for building AI agents and chain operations
	•	LangGraph: Advanced agent orchestration and multi-agent workflows
	•	LangSmith: Monitoring, debugging, and optimization of language model applications
	•	Twitter API: Social media platform integration
	•	Python: Primary programming language
	•	FastAPI: High-performance web framework for API endpoints
📋 Prerequisites
	•	Python 3.8+
	•	Twitter Developer Account
	•	API keys for Twitter
	•	LangSmith account (optional, for monitoring)
🔧 Installation
	1.	Clone the repository

    git clone https://github.com/yourusername/tweet-agent.git
    cd tweet-agent

    2.	Install dependencies
    uv add pyproject.toml

    3.Environment Configuration
    cp .env.example .env
# Edit .env with your API keys and configuration

⚙️ Configuration
Environment Variables

# Twitter API Configuration
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

# LangSmith Configuration (Optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

🚀 Usage
Basic Tweet Generation

from tweet_agent import TweetAgent

# Initialize the agent
agent = TweetAgent()

# Generate and post a tweet
tweet = agent.generate_tweet(topic="AI technology trends")
agent.post_tweet(tweet)

Advanced Multi-Agent Workflow

from tweet_agent.workflows import TwitterWorkflow

# Create workflow with multiple agents
workflow = TwitterWorkflow()

# Execute research → generate → review → post pipeline
result = workflow.execute({
    "topic": "machine learning",
    "target_audience": "tech professionals"
})




