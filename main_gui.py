import tkinter as tk
from tkinter import messagebox
from agent import call_phi3
from executor import execute_actions

def run_prompt():
    prompt = entry.get()
    if not prompt.strip():
        messagebox.showwarning("Empty Prompt", "Please enter a task.")
        return
    actions = call_phi3(prompt)
    if actions:
        execute_actions(actions)
    else:
        messagebox.showinfo("No Actions", "No valid actions returned.")

# GUI setup
window = tk.Tk()
window.title("PromptPilot")
window.geometry("500x180")
window.configure(bg="#f0f0f0")

label = tk.Label(window, text="Enter your task (natural language):", bg="#f0f0f0", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(window, width=60, font=("Arial", 12))
entry.pack(pady=5)

run_button = tk.Button(window, text="Execute Task", command=run_prompt, bg="#4CAF50", fg="white", font=("Arial", 12))
run_button.pack(pady=15)

window.mainloop()
