import tkinter as tk
import os
import shutil
import atexit
from llama_agent import get_command_from_prompt
from automation import run_action
from logger import log_action

LOG_DIR = "logs"

def delete_logs():
    if os.path.exists(LOG_DIR):
        shutil.rmtree(LOG_DIR)

atexit.register(delete_logs)

def on_run():
    prompt = txt.get()
    cmd = get_command_from_prompt(prompt)
    log_action(prompt, cmd)
    run_action(cmd)

if __name__ == "__main__":
    os.makedirs(LOG_DIR, exist_ok=True)
    app = tk.Tk()
    app.title("PromptPilot - AI Assistant")
    txt = tk.Entry(app, width=60)
    txt.pack(padx=10, pady=10)
    btn = tk.Button(app, text="Run Command", command=on_run)
    btn.pack(pady=5)
    app.mainloop()
