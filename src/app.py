import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

class App:
    def __init__(self, root):
        # Creates main window -> root
        self.root = root
        self.root.title("Media Converter") # Sets window title
        self.root.geometry("500x300") # Width x Height
        self.file_path = None

        # Drop area label 
        self.drop_label = tk.Label(self.root, text="Drag & drop desired file here.", width=40, height=5, relief="ridge") # adds text, size and border
        self.drop_label.pack(pady=50)

        # Make drop_label accept dropped files
        self.drop_label.drop_target_register(DND_FILES) # registers label as a place where files can be dropped 
        self.drop_label.dnd_bind("<<Drop>>", self.handle_drop) # when file is dropped, runs handle_drop function

        # Variable to store selected format
        self.selected_format = tk.StringVar(self.root)
        self.selected_format.set("mp3")  # default value

        #create dropdown menu
        self.format_menu = tk.OptionMenu(
            self.root,
            self.selected_format,
            "mp3", "wav", "ogg"
        )
        self.format_menu.pack(pady=10)

        # Add convert button
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_file)        
        self.convert_button.pack(pady=10)

    def handle_drop(self, event):
        self.file_path = event.data # stores file path 
        self.drop_label.config(text=f"File: {self.file_path}") # changes drop label text to show file name

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = App(root)
    root.mainloop()  