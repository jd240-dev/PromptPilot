import subprocess
import json
import logging
from utils import sanitize_json, timeout_handler

logger = logging.getLogger("PromptPilot-Agent")

OLLAMA_MODEL = "phi3:mini"

def call_phi3(prompt: str, timeout: int = 60):
    logger.info(f"🧠 Running {OLLAMA_MODEL} via Ollama...")

    try:
        completed = timeout_handler(
            lambda: subprocess.run(
                ["ollama", "run", OLLAMA_MODEL, prompt],
                capture_output=True, text=True, check=True
            ),
            timeout_seconds=timeout
        )
        output = completed.stdout.strip()
        logger.info(f"🔧 Raw model output:\n{output}")

        # Attempt to extract valid JSON
        actions = sanitize_json(output)
        return actions
    except subprocess.TimeoutExpired:
        logger.error("❌ ERROR: Phi3 model response timed out.")
    except Exception as e:
        logger.error(f"❌ ERROR running Phi3: {e}")
    return []
