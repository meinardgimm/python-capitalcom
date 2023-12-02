import os
import tkinter as tk
from tkinter import scrolledtext
import subprocess

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Viewer")

        # Create a scrolled text widget to display the output
        self.output_text = scrolledtext.ScrolledText(self.root, width=40, height=10)
        self.output_text.pack(padx=10, pady=10)

        # Create a button to run the "note.py" script
        self.run_button = tk.Button(self.root, text="Run note.py", command=self.run_note_script)
        self.run_button.pack(pady=10)

    def run_note_script(self):
        try:
            # Run the "note.py" script using subprocess
            os.listdir()
            result = subprocess.run(["python3", "capitalcom/note.py"], capture_output=True, text=True, check=True)
            output = result.stdout

            # Clear the current text in the scrolled text widget
            self.output_text.delete(1.0, tk.END)

            # Insert the output of the script into the scrolled text widget
            self.output_text.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            # If there is an error running the script, display the error message
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {e.stderr}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
