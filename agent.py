import subprocess
import json
import logging
import re
from utils import sanitize_json, timeout_subprocess
from logger import setup_logger

logger = setup_logger("PromptPilot-Agent")

def call_phi3(prompt: str, timeout=60):
    system_prompt = """
You are a Windows automation assistant.
Convert this prompt into a JSON list of structured actions.
Each action must be one of:
- {"action": "open", "app": "notepad"}
- {"action": "wait", "seconds": 2}
- {"action": "type", "text": "hello world"}
- {"action": "search", "query": "gmail in Microsoft Edge"}
Only return a valid JSON list. Do not include explanations or code blocks.
"""

    full_prompt = f"{system_prompt.strip()}\n\nPrompt: {prompt.strip()}"

    try:
        logger.info("🧠 Running phi3:mini via Ollama...")
        result = timeout_subprocess(["ollama", "run", "phi3:mini", full_prompt], timeout=timeout)
        logger.info(f"🔧 Raw model output:\n{result.strip()}")
        cleaned = sanitize_json(result)
        return cleaned
    except subprocess.TimeoutExpired:
        logger.error("❌ ERROR: Phi3 model response timed out.")
    except Exception as e:
        logger.error(f"❌ ERROR: Failed to call model: {e}")
    return []
