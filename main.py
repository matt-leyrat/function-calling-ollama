import argparse

from chat_ui import ChatUI
from model import interpret_results, model, handle_tool_calls

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
            print(response)
            result = handle_tool_calls(response.tool_calls)
            interpreted_result_stream = interpret_results(user_input, result)
            for chunk in interpreted_result_stream:
                print(chunk['message']['content'], end='', flush=True)
            print('\n')

