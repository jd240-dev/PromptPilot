import tkinter as tk
from agent import call_phi3
from executor import execute_actions

def run_prompt():
    prompt = entry.get()
    actions = call_phi3(prompt)
    if actions:
        execute_actions(actions)
    else:
        result_label.config(text="⚠️ No valid actions.")

root = tk.Tk()
root.title("PromptPilot GUI")

entry = tk.Entry(root, width=60)
entry.pack(pady=10)

button = tk.Button(root, text="Run", command=run_prompt)
button.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
