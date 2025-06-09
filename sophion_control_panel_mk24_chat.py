import tkinter as tk
from tkinter import scrolledtext
import requests
import subprocess
import os

root = tk.Tk()
root.title("SOPHION Control Panel Mk24")
root.geometry("580x600")
root.configure(bg="#f4f4f4")

frame = tk.Frame(root, bg="#f4f4f4")
frame.pack(pady=20)

def launch_all():
    subprocess.Popen(["py", "sophion_router_mk24.py"])
    subprocess.Popen(["py", "creator_api.py"])
    subprocess.Popen(["py", "critic_api.py"])
    subprocess.Popen(["py", "sage_api.py"])
    subprocess.Popen(["py", "trickster_api.py"])
    subprocess.Popen(["py", "hero_api.py"])
    subprocess.Popen(["py", "self_api_mk24_hemispheric.py"])

def launch_persona(filename):
    subprocess.Popen(["py", filename])

def launch_self():
    subprocess.Popen(["py", "self_api_mk24_hemispheric.py"])

def launch_scroll():
    try:
        os.startfile("scroll_memory.json")
    except Exception as e:
        print("Could not open scroll memory:", e)

def submit_theme():
    theme = theme_entry.get("1.0", tk.END).strip()
    if not theme:
        return
    try:
        response = requests.post("http://localhost:8100/route", json={"theme": theme})
        if response.status_code == 200:
            data = response.json()
            result_box.delete("1.0", tk.END)
            result_box.insert(tk.END, f"🧠 Theme: {data.get('theme', '')}\n\n")
            result_box.insert(tk.END, f"🔹 LH: {data.get('lh', '')}\n\n")
            result_box.insert(tk.END, f"🔸 RH: {data.get('rh', '')}\n\n")
            result_box.insert(tk.END, f"🌀 Glyph: {data.get('glyph', '')}\n")
        else:
            result_box.insert(tk.END, f"❌ Error: {response.status_code}\n{response.text}")
    except Exception as e:
        result_box.insert(tk.END, f"❌ Exception: {e}")

# === Buttons ===
tk.Button(frame, text="Launch All Agents", command=launch_all, width=30, bg="#d1e7dd").pack(pady=5)

tk.Label(frame, text="Launch Individual Persona:", bg="#f4f4f4").pack(pady=(15, 5))
tk.Button(frame, text="Creator", command=lambda: launch_persona("creator_api.py"), width=25).pack(pady=2)
tk.Button(frame, text="Critic", command=lambda: launch_persona("critic_api.py"), width=25).pack(pady=2)
tk.Button(frame, text="Sage", command=lambda: launch_persona("sage_api.py"), width=25).pack(pady=2)
tk.Button(frame, text="Trickster", command=lambda: launch_persona("trickster_api.py"), width=25).pack(pady=2)
tk.Button(frame, text="Hero", command=lambda: launch_persona("hero_api.py"), width=25).pack(pady=2)

tk.Button(frame, text="Launch Self Agent (Mk24)", command=launch_self, bg="#fef3c7").pack(pady=(20, 5))
tk.Button(frame, text="Recall Scroll Memory", command=launch_scroll, bg="#e2e3e5").pack(pady=10)

# === Symbolic Chat Interface ===
tk.Label(frame, text="Enter a symbolic theme:", bg="#f4f4f4").pack(pady=(10, 0))
theme_entry = tk.Text(frame, height=2, width=60)
theme_entry.pack(pady=5)
tk.Button(frame, text="Submit Theme to Mk24", command=submit_theme, bg="#cfe2ff").pack(pady=5)

result_box = scrolledtext.ScrolledText(frame, height=15, width=70, wrap=tk.WORD)
result_box.pack(pady=10)

root.mainloop()
