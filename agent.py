import subprocess
import json
import logging
import threading
import time
from utils import sanitize_json, run_with_timeout

OLLAMA_MODEL = "phi3:mini"

logger = logging.getLogger("PromptPilot-Agent")

def run_ollama_prompt(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            timeout=45,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        logger.error("❌ ERROR: Phi3 model response timed out.")
        return None
    except Exception as e:
        logger.error(f"❌ ERROR running Phi3: {e}")
        return None

def call_phi3(prompt):
    logger.info(f"🧠 Running {OLLAMA_MODEL} via Ollama...")
    raw_output = run_ollama_prompt(prompt)

    if not raw_output:
        return []

    logger.info(f"🔧 Raw model output:\n{raw_output}")

    # Extract and sanitize JSON
    try:
        cleaned = sanitize_json(raw_output)
        actions = json.loads(cleaned)
        if isinstance(actions, dict):
            actions = [actions]
        return actions
    except json.JSONDecodeError as e:
        logger.error(f"❌ ERROR: JSON parsing failed - {e}")
        return []
