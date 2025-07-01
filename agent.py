import subprocess
import json
import re

def call_phi3(prompt: str) -> list:
    """
    Calls the local Phi-3 model using Ollama and converts the natural language prompt into structured automation steps.
    """
    cmd = [
        "ollama", "run", "phi3",
        f"""
You are a Windows automation assistant.
Convert this prompt into a list of structured actions as JSON, like:
[
  {{ "action": "open", "app": "notepad" }},
  {{ "action": "wait", "seconds": 1 }},
  {{ "action": "type", "text": "hello world" }}
]

Prompt: {prompt}
"""
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=60, text=True, encoding='utf-8', errors='replace')
        raw_output = result.stdout.strip()

        # Optional logging for debug
        print("🔧 Raw model output:\n", raw_output)

        # Remove comments and extract JSON
        cleaned = re.sub(r'//.*?\n', '', raw_output)
        json_text = re.search(r"\[.*\]", cleaned, re.DOTALL).group()

        actions = json.loads(json_text)
        return actions

    except Exception as e:
        print(f"⚠️ Agent Error: {e}")
        return []
