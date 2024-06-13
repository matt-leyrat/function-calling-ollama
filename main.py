import argparse
import ollama
from langchain_experimental.llms.ollama_functions import OllamaFunctions

from chat_ui import ChatUI
from model import model, handle_tool_calls

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chat UI')
    parser.add_argument('--sexy', action='store_true', help='Run the sexy UI version')
    args = parser.parse_args()

    if args.sexy:
        chat_ui = ChatUI()
        chat_ui.run()
    else:
        while True:
            user_input = input("Enter your query (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break

            # Invoke function selection model
            response = model.invoke(user_input)
            result = handle_tool_calls(response.tool_calls)
            interpreted_result_stream = ollama.chat(
              model='llama3',
              messages=[
                  {
                      'role': 'user',
                      'content': f"Your role is to interpret the results of a function call from another LLM.the user query was this: {user_input} interpret these results: {result} if it's a joke just pass the joke along."
                  }
              ],
              stream=True,
            )
            for chunk in interpreted_result_stream:
                print(chunk['message']['content'], end='', flush=True)
            print('\n')

