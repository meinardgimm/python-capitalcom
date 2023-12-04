import tkinter as tk
from tkinter import scrolledtext
import subprocess
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        # Matplotlib figure and canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def run_note_script(self):
        try:
            # Run the "note.py" script using subprocess
            result = subprocess.run(["python", "capitalcom/note.py"],
                                    capture_output=True, text=True, check=True)
            output = result.stdout

            # Parse the JSON data
            data = json.loads(output)

            # Clear the current text in the scrolled text widget
            self.output_text.delete(1.0, tk.END)

            # Insert the output of the script into the scrolled text widget
            self.output_text.insert(tk.END, output)

            # Plot the data
            self.plot_data(data)

        except subprocess.CalledProcessError as e:
            # If there is an error running the script, display the error message
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {e.stderr}")

    def plot_data(self, data):
        # Extract data for plotting
        snapshot_times = [entry['snapshotTime'] for entry in data['prices']]
        bid_prices = [entry['openPrice']['bid'] for entry in data['prices']]
        ask_prices = [entry['openPrice']['ask'] for entry in data['prices']]

        # Plotting
        self.ax.clear()
        self.ax.plot(snapshot_times, bid_prices, label='Bid Price', marker='o')
        self.ax.plot(snapshot_times, ask_prices, label='Ask Price', marker='o')
        self.ax.set_xlabel('Snapshot Time')
        self.ax.set_ylabel('Price')
        self.ax.set_title('Bid and Ask Prices Over Time')
        self.ax.legend()

        # Update the canvas
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
