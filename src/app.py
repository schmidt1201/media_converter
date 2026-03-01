import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import os

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
        # remove curly braces and extra spaces
        path = event.data.strip().strip("{}")

        # convert to proper os path
        self.file_path = os.path.normpath(path)

        # show only filename
        filename = os.path.basename(self.file_path) 
        self.drop_label.config(text=f"File: {filename}") # changes drop label text to show file name

    def convert_file(self):
        if not self.file_path:
            self.drop_label.config(text="Please drop a file first.")
            return
        
        # Clean file path
        clean_path = self.file_path.strip("{}")

        output_format = self.selected_format.get()
        base, _ = os.path.splitext(clean_path)
        output_file = f"{base}.{output_format}"

        # Call ffmpeg
        subprocess.run([
            "ffmpeg",
            "-y",                   # Overwrite if exists
            "-i", self.file_path,   # input
            output_file             # output
        ])

        self.drop_label.config(text=f"Converted to {output_file}")
        print(f"successfully converted to {output_file}")

# run app
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = App(root)
    root.mainloop()  