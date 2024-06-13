from langchain_experimental.llms.ollama_functions import OllamaFunctions
import ollama
from tools import tools
from functions import wiki_search, random_joke, get_current_weather, get_news, google_search

model = OllamaFunctions(
    model="phi3", 
    format="json"
)

model = model.bind_tools(tools=tools)

def handle_tool_calls(tool_calls):
    if tool_calls:
        selected_tool = tool_calls[0]['name']
        tool_input = tool_calls[0]['args']
        
        # Execute the corresponding function based on the selected tool
        if selected_tool == 'wiki_search':
            return wiki_search(tool_input['query'])
        elif selected_tool == 'random_joke':
            return random_joke()
        elif selected_tool == 'get_current_weather':
            return get_current_weather(tool_input['location'], tool_input.get('unit', 'celsius'))
        elif selected_tool == 'get_news':
            return get_news(tool_input['query'])
        elif selected_tool == 'google_search':
            return google_search(tool_input['query'])
    else:
        return("No tool was selected.")

def interpret_results(user_input, result):
    interpreted_result_stream = ollama.chat(
      model='llama3',
      messages=[
          {
              'role': 'system',
              'content': f"""You are an assistant that provides concise 
                and direct responses that summarize the results from function calls. 
                Avoid using polite phrases and unnecessary details. 
                If the results are a joke, just pass the joke along without summarizing.
                The original user input was {user_input}"""
          },
          {
              'role': 'user',
              'content': f"Summarize the following results concisely: {result}"
          }
      ],
      stream=True,
      options={
          'temperature': 0.3,
          'presence_penalty': 0.5
      }
    )
    return interpreted_result_stream
