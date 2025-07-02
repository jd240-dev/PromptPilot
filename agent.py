import subprocess
import json
from logger import log
from utils import clean_json

def call_phi3(prompt: str, timeout: int = 20):
    system_prompt = (
        "You are a Windows automation assistant.\n"
        "Convert this prompt into a JSON list of actions.\n"
        "Example:\n"
        "[{\"action\": \"open\", \"app\": \"notepad\"}, {\"action\": \"wait\", \"seconds\": 1}, {\"action\": \"type\", \"text\": \"hello\"}]\n\n"
        f"Prompt: {prompt}"
    )
    try:
        result = subprocess.run(
            ["ollama", "run", "phi3", system_prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout
        )
        raw_output = result.stdout.decode("utf-8", errors="ignore").strip()
        log("🔧 Raw model output:\n" + raw_output)
        cleaned = clean_json(raw_output)
        return json.loads(cleaned)
    except subprocess.TimeoutExpired:
        log("❌ ERROR: Phi3 model response timed out.")
        return []
    except json.JSONDecodeError as e:
        log(f"❌ ERROR: JSON parsing failed - {e}")
        return []
