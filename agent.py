import subprocess
import json
import logging
import platform

from utils import sanitize_json, timeout_handler, run_with_timeout

# Configure logger
logger = logging.getLogger("PromptPilot-Agent")
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

OLLAMA_MODEL = "phi3:mini"

def call_phi3(prompt, timeout=15):
    logger.info(f"🧠 Running {OLLAMA_MODEL} via Ollama...")

    def run_model():
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout
        )
        return result.stdout.decode(errors="replace")

    try:
        raw_output = run_with_timeout(run_model, timeout)
        logger.info(f"🔧 Raw model output:\n{raw_output}")

        parsed_json = sanitize_json(raw_output)
        return parsed_json

    except subprocess.TimeoutExpired:
        logger.error("❌ ERROR: Phi3 model response timed out.")
    except Exception as e:
        logger.error(f"❌ ERROR running Phi3: {e}")
    return []
