import os

def clear_logs():
    if os.path.exists("logs.txt"):
        os.remove("logs.txt")

def log_action(prompt, actions):
    with open("logs.txt", "a") as f:
        f.write(f"\nPROMPT: {prompt}\n")
        f.write(f"ACTIONS: {actions}\n")
