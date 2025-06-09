import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import requests
import os
from datetime import datetime

services = [
    ("Hero", "hero_api.py"),
    ("Critic", "critic_api.py"),
    ("Persona", "persona_api.py"),
    ("Trickster", "trickster_api.py"),
    ("Sage", "sage_api.py"),
    ("Creator", "creator_api.py"),
    ("Self", "self_api.py"),
    ("Sophion Router", "sophion_router.py")
]

launched_processes = []

api_key_var = None

def launch_all():
    for name, script in services:
        try:
            proc = subprocess.Popen(["py", script], creationflags=subprocess.CREATE_NEW_CONSOLE)
            launched_processes.append((name, proc))
        except Exception as e:
            messagebox.showerror("Launch Error", f"Could not launch {script}: {str(e)}")

def close_all():
    global launched_processes
    if not launched_processes:
        messagebox.showinfo("Nothing Running", "No processes are currently being tracked.")
        return

    errors = []
    for name, proc in launched_processes:
        try:
            proc.terminate()
        except Exception as e:
            errors.append(f"{name}: {str(e)}")

    launched_processes.clear()
    if errors:
        messagebox.showerror("Some Errors", "\n".join(errors))
    else:
        messagebox.showinfo("Closed", "All Sophion services were closed successfully.")

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
            output.insert(tk.END, f"{data['summary']}\n")
            if "echo_from" in data and data["echo_from"]:
                output.insert(tk.END, f"\nEcho From: {data['echo_from']['theme']} — {data['echo_from']['glyph']}\n")
                output.insert(tk.END, f"{data['echo_from']['summary']}\n")
        else:
            messagebox.showerror("Error", f"Server returned status {response.status_code}")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

def view_scrolls():
    try:
        response = requests.get("http://localhost:8100/sophion/scrolls")
        if response.status_code == 200:
            scrolls = response.json()
            output.delete("1.0", tk.END)
            for s in scrolls:
                output.insert(tk.END, f"[{s['timestamp']}]\n")
                output.insert(tk.END, f"Theme: {s['theme']}\n")
                output.insert(tk.END, f"Glyph: {s['glyph']}\n")
                output.insert(tk.END, f"{s['summary']}\n\n")
        else:
            messagebox.showerror("Error", f"Server returned status {response.status_code}")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))


def launch_self():
    try:
        proc = subprocess.Popen(["py", "self_api_mk23_with_llm_test_rebuilt.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        launched_processes.append(("Self", proc))
        messagebox.showinfo("Self Agent", "Mk23 Self Agent launched successfully.")
    except Exception as e:
        messagebox.showerror("Launch Error", f"Could not launch Self Agent: {str(e)}")

def test_llm_key():
    key = api_key_var.get()
    if not key:
        messagebox.showwarning("Missing Key", "Please paste your OpenAI API key.")
        return
    try:
        response = requests.post("http://localhost:8107/self/test_llm", json={"api_key": key})
        if response.status_code == 200:
            msg = response.json().get("message", "LLM is active.")
            messagebox.showinfo("LLM Status", f"✅ {msg}")
        else:
            msg = response.json().get("message", "Unknown error.")
            messagebox.showwarning("LLM Error", f"⚠️ {msg}")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

root = tk.Tk()
root.title("Sophion Control Panel")

top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Button(top_frame, text="Launch All Services", command=launch_all, bg="#d0ffd0").pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="Close All Services", command=close_all, bg="#ffd0d0").pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="Recall All Scrolls", command=view_scrolls, bg="#f0e0ff").pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="Launch Self Agent Only", command=launch_self, bg="#e0f0ff").pack(side=tk.LEFT, padx=5)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Enter symbolic theme:").pack()
entry = tk.Entry(input_frame, width=60)
entry.pack(pady=5)

send_btn = tk.Button(input_frame, text="Send to Sophion", command=send_theme, bg="#d0e0ff")
send_btn.pack(pady=5)

api_frame = tk.Frame(root)
api_frame.pack(pady=10)

tk.Label(api_frame, text="Paste OpenAI API Key:").pack()
api_key_var = tk.StringVar()
api_entry = tk.Entry(api_frame, textvariable=api_key_var, width=60, show="*")
api_entry.pack(pady=5)

tk.Button(api_frame, text="Verify LLM Activation", command=test_llm_key, bg="#ffe0a0").pack(pady=5)

output = scrolledtext.ScrolledText(root, width=90, height=25, wrap=tk.WORD)
output.pack(padx=10, pady=10)

root.mainloop()
