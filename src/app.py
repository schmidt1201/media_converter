import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import os

BG_COLOR = "#0f0f0f"
PANEL_COLOR = "#1a1a1a"
ACCENT = "#4f46e5"
TEXT_COLOR = "#ffffff"
MUTED = "#aaaaaa"

SUPPORTED_FORMATS = ["mp3", "wav", "ogg", "flac", "aac"]

class App:
    def __init__(self, root):
        # Creates main window -> root
        self.root = root
        self.root.title("Media Converter")
        self.root.geometry("500x300")
        self.root.configure(bg=BG_COLOR)
        self.file_path = None

        # Drop area label 
        self.drop_label = tk.Label(
            self.root, 
            text="Drag & drop desired file here.", 
            width=40, 
            height=5, 
            relief="ridge", 
            bg=PANEL_COLOR, 
            fg=MUTED, 
            font=("Segoe UI", 11), 
            highlightbackground="#2a2a2a", 
            highlightthickness=1
        )
        self.drop_label.pack(pady=50)

        # Make drop_label accept dropped files
        self.drop_label.drop_target_register(DND_FILES) # registers label as a place where files can be dropped 
        self.drop_label.dnd_bind("<<Drop>>", self.handle_drop) # when file is dropped, runs handle_drop function

        # Variable to store selected format
        self.selected_format = tk.StringVar(self.root)
        self.selected_format.set(SUPPORTED_FORMATS[0])  # default value

        #create dropdown menu
        self.format_menu = tk.OptionMenu(
            self.root,
            self.selected_format,
            *SUPPORTED_FORMATS
        )

        self.format_menu.config(             
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            activebackground=PANEL_COLOR,
            activeforeground=TEXT_COLOR,
            highlightthickness=0,
            font=("Segoe UI", 10)
        )

        self.format_menu["menu"].config(     
            bg=PANEL_COLOR,
            fg=TEXT_COLOR
        )

        self.format_menu.pack(pady=10)

        # Add convert button
        self.convert_button = tk.Button(
            self.root,
            text="Convert", 
            command=self.convert_file, 
            bg=ACCENT, 
            fg="white", 
            activebackground="#4338ca", 
            activeforeground="white", 
            relief="flat", 
            font=("Segoe UI", 10, "bold"), 
            padx=20, 
            pady=6
        )        
        self.convert_button.pack(pady=10)

    def handle_drop(self, event):
        # Remove curly braces added by tkinterdnd2 on Windows paths
        path = event.data.strip().strip("{}")

        # convert to proper os path
        self.file_path = os.path.normpath(path)

        # show only filename
        filename = os.path.basename(self.file_path) 
        self.drop_label.config(text=f"File: {filename}", fg=TEXT_COLOR) # changes drop label text to show file name

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