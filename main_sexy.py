import urwid
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
            return results
        elif selected_tool == 'random_joke':
            joke = random_joke()
            return joke
        elif selected_tool == 'google_search':
            results = google_search(tool_input['query'])
            return results
        elif selected_tool == 'get_current_weather':
            weather = get_current_weather(tool_input['location'], tool_input.get('unit', 'celsius'))
            return weather
    else:
        return "No tool was selected."

class EditWithCursor(urwid.Edit):
    def render(self, size, focus=False):
        canvas = super().render(size, focus)
        if focus:
            canvas = urwid.CompositeCanvas(canvas)
            canvas.cursor = self.get_cursor_coords(size)
        return canvas

class ChatUI:
    def __init__(self):
        self.chat_history = urwid.SimpleFocusListWalker([])
        self.chat_list = urwid.ListBox(self.chat_history)
        self.edit_box = EditWithCursor(caption='> ')
        self.frame = urwid.Frame(self.chat_list, footer=self.edit_box)
        self.frame.focus_position = 'footer'  # Set initial focus on the edit box
        
        palette = [
            ('user_input', 'light green', 'default'),
            ('assistant_response', 'light blue', 'default'),
        ]
        
        self.loop = urwid.MainLoop(self.frame, palette=palette, unhandled_input=self.handle_input)

    def handle_input(self, key):
        if key == 'enter':
            user_input = self.edit_box.edit_text.strip()
            if user_input.lower() == 'exit':
                raise urwid.ExitMainLoop()
            
            self.chat_history.append(urwid.Text(('user_input', f"User: {user_input}")))
            self.edit_box.set_edit_text('')
            
            response = model.invoke(user_input)
            result = handle_tool_calls(response.tool_calls)
            
            # Wrap the assistant response in a urwid.Text widget
            assistant_response = urwid.Text(('assistant_response', f"Assistant: {result}"))
            self.chat_history.append(assistant_response)
            
            self.chat_list.focus_position = len(self.chat_history) - 1
            self.loop.draw_screen()  # Refresh the screen after handling input

    def run(self):
        self.loop.run()

if __name__ == '__main__':
    chat_ui = ChatUI()
    chat_ui.run()