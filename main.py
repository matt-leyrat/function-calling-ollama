from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.messages import HumanMessage

from functions import wiki_search, random_joke, get_current_weather, google_search
from tools import tools

model = OllamaFunctions(
    model="llama3", 
    format="json"
)

model = model.bind_tools(tools=tools)

def handle_tool_calls(tool_calls):
    if tool_calls:
        selected_tool = tool_calls[0]['name']
        tool_input = tool_calls[0]['args']
        
        # Execute the corresponding function based on the selected tool
        if selected_tool == 'wiki_search':
            results = wiki_search(tool_input['query'])
            print(results)
        elif selected_tool == 'random_joke':
            joke = random_joke()
            print(joke)
        elif selected_tool == 'google_search':
            results = google_search(tool_input['query'])
            print(results)
        elif selected_tool == 'get_current_weather':
            weather = get_current_weather(tool_input['location'], tool_input.get('unit', 'celsius'))
            print(weather)
    else:
        print("No tool was selected.")

while True:
    user_input = input("Enter your query (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    # invoke function selection model
    response = model.invoke(user_input)
    
    handle_tool_calls(response.tool_calls)
