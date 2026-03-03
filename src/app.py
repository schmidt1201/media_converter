import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
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
            self.drop_label.config(text="Please drop a file first.") # if clicks button without dropping a file
            return
        
        # Disable button while converting to prevent double-clicks
        self.convert_button.config(state="disabled", text="Converting...")
        self.drop_label.config(text="Converting...", fg=MUTED)

        thread = threading.Thread(target=self._run_conversion, daemon=True)
        thread.start()

    def _run_conversion(self):
        output_format = self.selected_format.get()
        base, _ = os.path.splitext(self.file_path)
        output_file = f"{base}.{output_format}"

        try:
            result = subprocess.run(
                ["ffmpeg", "-y", "-i", self.file_path, output_file],
                capture_output=True, # supresses terminal noise
                text=True # stderr/stdout returned as strings
            )
            if result.returncode != 0:
                self.root.after(0, lambda: self._on_failure("Conversion failed"))
            else:
                filename = os.path.basename(output_file)
                self.root.after(0, lambda: self._on_success(filename))
        except FileNotFoundError:
            # ffmpeg is not installed or not on path
            self.root.after(0, lambda: self._on_failure("ffmpeg not found. is it installed/on PATH?"))
    
    def _on_success(self, filename):
        self.drop_label.config(text=f"✅ Saved: {filename}", fg=TEXT_COLOR)
        self.convert_button.config(state="normal", text="Convert")

    def _on_failure(self, message):
        self.drop_label.config(text=f"❌ {message}", fg="#f87171")
        self.convert_button.config(state="normal", text="Convert")

# run app
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = App(root)
    root.mainloop()  