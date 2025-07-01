import subprocess
import json

def get_command_from_prompt(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", f"""
You are a Windows automation assistant.
Convert this prompt into a list of structured actions as JSON:
[
  {{"action": "open", "app": "notepad"}},
  {{"action": "wait", "seconds": 1}},
  {{"action": "type", "text": "hello"}}
]

Prompt: {prompt}
"""],
            capture_output=True,
            text=True,
            timeout=20,
            encoding="utf-8",
            errors="ignore"
        )

        output = result.stdout.strip()

        # Try parsing the JSON response
        try:
            json.loads(output)
            return output
        except json.JSONDecodeError:
            print("❌ Invalid JSON from LLaMA:")
            print(output)
            return "[]"

    except Exception as e:
        print(f"[ERROR llama_agent.py] {e}")
        return "[]"
