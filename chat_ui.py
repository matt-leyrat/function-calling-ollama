import urwid
from model import model, handle_tool_calls

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
