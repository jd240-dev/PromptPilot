import logging
import time
import webbrowser
import pyautogui

logger = logging.getLogger("PromptPilot-Executor")

def execute_actions(actions):
    for action in actions:
        try:
            act = action.get("action")

            if act == "open_app":
                subprocess.Popen(action.get("name"))
            elif act == "open_url":
                webbrowser.open(action.get("site") or action.get("url"))
            elif act == "wait":
                time.sleep(action.get("seconds", 1))
            elif act == "type":
                pyautogui.write(action.get("text", ""), interval=0.05)
            elif act == "click":
                pyautogui.click()
            elif act == "keypress":
                pyautogui.press(action.get("key"))
            else:
                logger.warning(f"⚠️ Unknown action: {action}")
        except Exception as e:
            logger.error(f"❌ Failed action {action}: {e}")
