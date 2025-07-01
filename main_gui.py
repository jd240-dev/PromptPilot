import tkinter as tk
from agent import call_phi3
from executor import execute_all
from logger import init_logger
from utils import log_action

init_logger()

def run_prompt():
    prompt = entry.get()
    actions = call_phi3(prompt)
    log_action(prompt, actions)
    execute_all(actions)

root = tk.Tk()
root.title("PromptPilot Ultimate")

entry = tk.Entry(root, width=60)
entry.pack(padx=10, pady=10)

btn = tk.Button(root, text="Launch Automation", command=run_prompt)
btn.pack(pady=10)

root.mainloop()
