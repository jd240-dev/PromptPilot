import subprocess
import time
import logging
from logger import setup_logger

logger = setup_logger("PromptPilot-Executor")

def execute_actions(actions):
    for action in actions:
        try:
            if action["action"] == "open":
                subprocess.Popen(action["app"])
                logger.info(f"🟢 Opened: {action['app']}")

            elif action["action"] == "wait":
                time.sleep(float(action["seconds"]))
                logger.info(f"⏱️ Waited for {action['seconds']} seconds")

            elif action["action"] == "type":
                import pyautogui
                pyautogui.write(action["text"])
                logger.info(f"⌨️ Typed: {action['text']}")

            elif action["action"] == "search":
                query = action["query"]
                subprocess.Popen(["start", "msedge", f"https://www.google.com/search?q={query}"], shell=True)
                logger.info(f"🔍 Searched for: {query}")

            else:
                logger.warning(f"⚠️ Unknown action: {action}")
        except Exception as e:
            logger.error(f"❌ Execution error: {e}")
