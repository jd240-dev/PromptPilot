import subprocess
import json
import re

def call_phi3(prompt: str) -> list:
    """
    Calls Phi-3 or LLaMA via Ollama and parses structured JSON actions.
    """
    cmd = [
        "ollama", "run", "phi3",  # or "llama3"
        f"""
You are a Windows automation assistant.
Respond ONLY with a JSON array like:
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
        print("🔧 Raw model output:\n", raw_output)

        # Remove comments (e.g., //...) and trailing junk
        cleaned_output = re.sub(r'//.*?\n', '', raw_output)

        # Find first valid JSON array
        match = re.search(r'\[\s*{.*?}\s*\]', cleaned_output, re.DOTALL)
        if not match:
            raise ValueError("❌ No valid JSON array found.")

        json_text = match.group(0)

        # Convert string to Python list
        actions = json.loads(json_text)
        return actions

    except Exception as e:
        print(f"⚠️ Agent Error: {e}")
        return []
