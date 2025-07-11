import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import time
import os

def load_log():
    if os.path.exists("decrypted_log.txt"):
        with open("decrypted_log.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "No logs found. Run decrypt_logs.py first."

def refresh_log():
    text.delete("1.0", tk.END)
    text.insert(tk.END, load_log())
    window.after(5000, refresh_log)

window = tk.Tk()
window.title("Log Viewer")
text = ScrolledText(window, width=100, height=30, bg="black", fg="white")
text.pack()

refresh_log()
window.mainloop()
