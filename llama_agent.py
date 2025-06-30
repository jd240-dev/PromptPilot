import subprocess

def get_command_from_prompt(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", f"""
Act as a Windows automation assistant.
Your job is to convert user instructions into simple, step-by-step machine-executable commands.
Respond only with a Python-style list of actions in this format:
[
  {{"action": "open", "app": "notepad"}},
  {{"action": "wait", "seconds": 1}},
  {{"action": "type", "text": "Hello World"}}
]

User prompt: {prompt}
"""],
            capture_output=True,
            text=True,
            timeout=20
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[ERROR] {e}"
