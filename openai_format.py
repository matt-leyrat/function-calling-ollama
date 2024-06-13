import requests
import ollama
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain.agents import initialize_agent, Tool
from langchain.requests import RequestsWrapper  # Import RequestsWrapper

# Set up Ollama model and tools
ollama.pull("llama3")  # Download the llama3 model if not already present
model = OllamaFunctions(model="llama3", format="json")

# Define tools for the agent
tools = [
    Tool(
        name="Wikipedia Search",
        func=RequestsWrapper.run,  # Use RequestsWrapper().run
        description="Searches Wikipedia for the given query",
        coroutine="auto"
    ),
    Tool(
        name="Get Weather",
        func=lambda location: requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid=YOUR_API_KEY&units=metric").json(),
        description="Gets the current weather for a given location",
        coroutine="auto"
    ),
    Tool(
        name="Random Joke",
        func=lambda: requests.get("https://official-joke-api.appspot.com/random_joke").json(),
        description="Fetches a random joke",
        coroutine="auto"
    )
]

# Bind tools to the model
model = model.bind_tools(tools)

# Initialize the agent
agent = initialize_agent(tools, model, agent="zero-shot-react-description", verbose=True)

# Example usage
query = "tell me a joke."
result = agent.invoke(query)
print(result)
