# agent.py

import subprocess
import json
from utils import extract_json, is_valid_json, log

def call_phi3(prompt):
    log("Calling local Phi-3 model...", "INFO")
    raw_prompt = f'''
You are a Windows automation assistant.
Convert this prompt into a list of structured actions in valid JSON format only.

Prompt: {prompt}
    '''

    try:
        result = subprocess.run(
            ["ollama", "run", "phi3", raw_prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        output = result.stdout.strip()
        log(f"🔧 Raw model output:\n{output}", "DEBUG")

        json_data = extract_json(output)
        if json_data and is_valid_json(json_data):
            return json.loads(json_data)

        raise ValueError("❌ Model returned invalid JSON.")

    except subprocess.TimeoutExpired:
        log("⚠️ Phi-3 model timed out.", "ERROR")
    except Exception as e:
        log(f"⚠️ Agent Error: {str(e)}", "ERROR")

    return []
