import tkinter as tk
from agent import call_phi3
from executor import execute_actions

def run_task():
    prompt = prompt_entry.get()
    actions = call_phi3(prompt)
    if actions:
        execute_actions(actions)
    else:
        result_label.config(text="⚠️ No valid actions returned.")

root = tk.Tk()
root.title("PromptPilot GUI")

tk.Label(root, text="Enter Task:").pack()
prompt_entry = tk.Entry(root, width=50)
prompt_entry.pack()

tk.Button(root, text="Run", command=run_task).pack()
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
