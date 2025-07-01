import subprocess
import json
import re

def call_phi3(prompt: str) -> list:
    cmd = [
        "ollama", "run", "phi3",
        f"""
You are a Windows automation assistant.
Convert this prompt into a list of structured actions as JSON:

Prompt: {prompt}
"""
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=30, text=True)
        raw_output = result.stdout.strip()
        cleaned = re.sub(r'//.*?\n', '', raw_output)
        json_text = re.search(r"\[.*\]", cleaned, re.DOTALL).group()
        return json.loads(json_text)
    except Exception as e:
        print(f"⚠️ Agent Error: {e}")
        return []
