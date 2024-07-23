import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import font
import re

class TextEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("Python Text Editor")
        self.file_path = None

        self.setup_widgets()
        self.create_menu()

        self.bind_shortcuts()

    def setup_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.text_area = tk.Text(self.main_frame, wrap=tk.NONE, undo=True, font=("Arial", 12))
        self.text_area.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)

        self.scrollbar_y = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.text_area.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.config(xscrollcommand=self.scrollbar_x.set)

        self.line_numbers = tk.Text(self.main_frame, width=4, padx=3, takefocus=0, border=0, background='lightgrey', state='disabled', wrap='none')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.update_line_numbers()

        self.text_area.bind("<KeyRelease>", self.on_text_change)
        self.text_area.bind("<MouseWheel>", self.on_text_change)
        self.text_area.bind("<Button-1>", self.on_text_change)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        edit_menu.add_command(label="Increase Font Size", command=self.increase_font_size, accelerator="Ctrl++")
        edit_menu.add_command(label="Decrease Font Size", command=self.decrease_font_size, accelerator="Ctrl+-")

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def bind_shortcuts(self):
        self.root.bind('<Control-o>', self.open_file)
        self.root.bind('<Control-s>', self.save_file)
        self.root.bind('<Control-Shift-S>', self.save_as_file)
        self.root.bind('<Control-f>', self.find_text)
        self.root.bind('<Control-F>', self.find_text)
        self.root.bind('<Control-plus>', self.increase_font_size)
        self.root.bind('<Control-minus>', self.decrease_font_size)

    def open_file(self, event=None):
        self.file_path = filedialog.askopenfilename()
        if not self.file_path:
            return
        with open(self.file_path, 'r') as file:
            content = file.read()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, content)
        self.root.title(f"Python Text Editor - {self.file_path}")

    def save_file(self, event=None):
        if not self.file_path:
            self.save_as_file()
        else:
            with open(self.file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
            self.root.title(f"Python Text Editor - {self.file_path}")

    def save_as_file(self, event=None):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                      filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if not self.file_path:
            return
        with open(self.file_path, 'w') as file:
            content = self.text_area.get(1.0, tk.END)
            file.write(content)
        self.root.title(f"Python Text Editor - {self.file_path}")

    def find_text(self, event=None):
        search_term = simpledialog.askstring("Find Text", "Enter text to find:")
        if search_term:
            self.text_area.tag_remove("highlight", "1.0", tk.END)
            start_pos = "1.0"
            while True:
                start_pos = self.text_area.search(search_term, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_term)}c"
                self.text_area.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos
            self.text_area.tag_config("highlight", background="yellow")

    def increase_font_size(self, event=None):
        current_font = font.Font(font=self.text_area['font'])
        size = current_font.actual()['size'] + 1
        self.text_area.configure(font=(current_font.actual()['family'], size))

    def decrease_font_size(self, event=None):
        current_font = font.Font(font=self.text_area['font'])
        size = current_font.actual()['size'] - 1
        self.text_area.configure(font=(current_font.actual()['family'], size))

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        line_count = self.text_area.index('end-1c').split('.')[0]
        for i in range(1, int(line_count) + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")
        self.line_numbers.config(state='disabled')

    def on_text_change(self, event=None):
        self.update_line_numbers()
        self.syntax_highlighting()

    def syntax_highlighting(self):
        keywords = ["def", "class", "import", "from", "return", "if", "else", "elif", "for", "while", "try", "except", "with", "as", "lambda"]
        self.text_area.tag_remove("keyword", "1.0", tk.END)
        for keyword in keywords:
            start_pos = "1.0"
            while True:
                start_pos = self.text_area.search(r'\b' + keyword + r'\b', start_pos, stopindex=tk.END, regexp=True)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(keyword)}c"
                self.text_area.tag_add("keyword", start_pos, end_pos)
                start_pos = end_pos
        self.text_area.tag_config("keyword", foreground="blue", font=('Arial', 12, 'bold'))

    def show_about(self):
        messagebox.showinfo("About", "Python Text Editor\n\nCreated using Tkinter.\n\nFeatures:\n- Syntax Highlighting\n- Line Numbers\n- Text Search\n- File Operations\n- Font Size Adjustment")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
