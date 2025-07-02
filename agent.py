import subprocess
import json
import logging
from utils import sanitize_json, run_with_timeout

# Configure logger
logger = logging.getLogger("PromptPilot-Agent")
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

OLLAMA_MODEL = "phi3:mini"

def run_model(prompt: str) -> str:
    try:
        logger.info(f"🧠 Running {OLLAMA_MODEL} via Ollama...")
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            timeout=60  # Add process-level timeout too
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        logger.error("❌ ERROR: Phi3 model response timed out.")
        return None
    except Exception as e:
        logger.error(f"❌ ERROR running Phi3: {e}")
        return None

def call_phi3(prompt: str):
    raw_output = run_with_timeout(run_model, args=(prompt,), timeout_duration=20)

    if not isinstance(raw_output, str):
        logger.error(f"❌ ERROR running Phi3: {raw_output}")
        return None

    logger.info(f"🔧 Raw model output:\n{raw_output}")
    try:
        actions = sanitize_json(raw_output)
        return actions
    except Exception as e:
        logger.error(f"❌ Failed to parse JSON: {e}")
        return None
