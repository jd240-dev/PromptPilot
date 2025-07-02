import subprocess
import logging
from utils import sanitize_json, run_with_timeout

# Set up logger
logger = logging.getLogger("PromptPilot-Agent")
logging.basicConfig(level=logging.INFO)

OLLAMA_MODEL = "phi3:mini"

def call_phi3(prompt: str, timeout: int = 60):
    """
    Calls the Phi-3 Mini model via Ollama and returns a list of parsed actions.
    Includes timeout handling and JSON sanitization.
    """
    logger.info(f"🧠 Running {OLLAMA_MODEL} via Ollama...")

    try:
        # Run the Ollama model with timeout handling
        completed = run_with_timeout(
            lambda: subprocess.run(
                ["ollama", "run", OLLAMA_MODEL, prompt],
                capture_output=True,
                text=True,
                check=True
            ),
            timeout_seconds=timeout
        )

        output = completed.stdout.strip()
        logger.info(f"🔧 Raw model output:\n{output}")

        # Sanitize and parse output
        actions = sanitize_json(output)
        return actions

    except subprocess.TimeoutExpired:
        logger.error("❌ ERROR: Phi3 model response timed out.")
    except Exception as e:
        logger.error(f"❌ ERROR running Phi3: {e}")

    return []
