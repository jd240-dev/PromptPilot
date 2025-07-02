import subprocess
import json
import logging
from utils import sanitize_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PromptPilot-Agent")

MODEL_NAME = "phi3:mini"
TIMEOUT_SECONDS = 30


def call_phi3(prompt: str) -> list:
    """
    Invokes the local phi3:mini model via Ollama and returns a list of actions from model output.
    """
    system_prompt = """You are a Windows automation AI.
Your job is to convert a user's request into a list of step-by-step JSON actions.

Each action should follow this format:
{ "action": "open_app", "name": "notepad" }
{ "action": "type", "text": "hello world" }
{ "action": "wait", "seconds": 1 }
{ "action": "press", "keys": ["ctrl", "s"] }

Respond ONLY with a pure JSON array of such actions. Do NOT include explanations or comments.
"""

    full_prompt = f"{system_prompt}\nUser prompt: {prompt.strip()}\n"

    try:
        logger.info("🧠 Running phi3:mini via Ollama...")
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, full_prompt],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            encoding="utf-8",
            errors="ignore"  # Ignore unicode decoding errors
        )
        raw_output = result.stdout.strip()
        logger.info("🔧 Raw model output:\n%s", raw_output)

        # Try direct JSON parsing
        try:
            parsed = json.loads(raw_output)
            return parsed if isinstance(parsed, list) else [parsed]

        except json.JSONDecodeError:
            logger.warning("⚠️ JSON parsing failed. Attempting to sanitize...")
            cleaned = sanitize_json(raw_output)
            logger.debug("🧼 Cleaned JSON:\n%s", cleaned)

            parsed = json.loads(cleaned)
            return parsed if isinstance(parsed, list) else [parsed]

    except subprocess.TimeoutExpired:
        logger.error("❌ ERROR: Phi3:mini model response timed out after %d seconds.", TIMEOUT_SECONDS)
    except json.JSONDecodeError as e:
        logger.error("❌ JSON parsing failed after sanitization: %s", str(e))
    except Exception as e:
        logger.exception("❌ Unexpected error in phi3 agent:")

    return []
