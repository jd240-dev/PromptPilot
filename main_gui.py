import tkinter as tk
from agent import call_phi3
from executor import execute_actions

def run_prompt():
    prompt = prompt_entry.get()
    actions = call_phi3(prompt)
    if actions:
        execute_actions(actions)
    else:
        output_label.config(text="⚠️ No valid actions returned.")

app = tk.Tk()
app.title("PromptPilot GUI")
app.geometry("400x200")

tk.Label(app, text="Enter Command:").pack(pady=10)
prompt_entry = tk.Entry(app, width=50)
prompt_entry.pack()

tk.Button(app, text="Run", command=run_prompt).pack(pady=20)
output_label = tk.Label(app, text="")
output_label.pack()

app.mainloop()
