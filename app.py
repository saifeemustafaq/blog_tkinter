import tkinter as tk
from tkinter import filedialog, messagebox

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Text Editor")

        # Menu Bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", command=self.undo_text)
        self.edit_menu.add_command(label="Redo", command=self.redo_text)

        # View Menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        # Font submenu
        self.font_var = tk.StringVar(value="Times")
        self.fonts = ["Times", "Arial", "Helvetica"]
        self.font_menu = tk.Menu(self.view_menu, tearoff=0)
        for font in self.fonts:
            self.font_menu.add_radiobutton(label=font, variable=self.font_var, command=self.change_font)
        self.view_menu.add_cascade(label="Font", menu=self.font_menu)

        # Theme submenu
        self.theme_var = tk.StringVar(value="Light")
        self.themes = {
            "Light": {"bg": "white", "fg": "black"},
            "Dark": {"bg": "black", "fg": "white"}
        }
        self.theme_menu = tk.Menu(self.view_menu, tearoff=0)
        for theme, _ in self.themes.items():
            self.theme_menu.add_radiobutton(label=theme, variable=self.theme_var, command=self.change_theme)
        self.view_menu.add_cascade(label="Theme", menu=self.theme_menu)

        # Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        # Text Area and Scrollbar
        self.text_scroll = tk.Scrollbar(root)
        self.text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_area = tk.Text(root, yscrollcommand=self.text_scroll.set, wrap=tk.WORD, undo=True, font=(self.font_var.get(), 12))
        self.text_area.pack(fill=tk.BOTH, expand=1)

        self.text_scroll.config(command=self.text_area.yview)
        self.text_area.bind('<KeyRelease>', self.update_status)

        # Status Bar
        self.status = tk.Label(root, text='Line: 1 | Column: 1', anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, event=None):
        row, col = self.text_area.index(tk.INSERT).split('.')
        self.status.config(text=f'Line: {row} | Column: {col}')

    def change_font(self):
        self.text_area.config(font=(self.font_var.get(), 12))

    def change_theme(self):
        theme = self.theme_var.get()
        bg_color, fg_color = self.themes[theme]["bg"], self.themes[theme]["fg"]
        self.text_area.config(bg=bg_color, fg=fg_color)

    def show_about(self):
        messagebox.showinfo("About", "This is a simple Text Editor application using tkinter!")

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.INSERT, file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def undo_text(self):
        self.text_area.edit_undo()

    def redo_text(self):
        self.text_area.edit_redo()

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
