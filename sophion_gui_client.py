
import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import json

def send_theme():
    theme = entry.get()
    if not theme:
        messagebox.showwarning("Missing Theme", "Please enter a symbolic theme.")
        return

    try:
        response = requests.post(
            "http://localhost:8100/sophion/council",
            json={"theme": theme}
        )
        if response.status_code == 200:
            data = response.json()
            output.delete("1.0", tk.END)
            output.insert(tk.END, f"Theme: {data['theme']}\n\n")
            for r in data['responses']:
                output.insert(tk.END, f"{r}\n")
            output.insert(tk.END, f"\nGlyph: {data['glyph']}\n")
            output.insert(tk.END, f"{data['summary']}")
        else:
            messagebox.showerror("Error", f"Server returned status {response.status_code}")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

root = tk.Tk()
root.title("Sophion Theme Sender")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Enter symbolic theme:").pack()
entry = tk.Entry(frame, width=60)
entry.pack(pady=5)

send_btn = tk.Button(frame, text="Send to Sophion", command=send_theme)
send_btn.pack(pady=5)

output = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
output.pack(padx=10, pady=10)

root.mainloop()
