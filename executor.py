import time
import subprocess
import logging
import webbrowser
import pyautogui

logger = logging.getLogger("PromptPilot-Executor")

def execute_action(action):
    try:
        act = action.get("action")

        if act == "open_app":
            app_name = action.get("name")
            subprocess.Popen(["start", "", app_name], shell=True)

        elif act == "wait":
            time.sleep(float(action.get("seconds", 1)))

        elif act == "type":
            pyautogui.write(action.get("text", ""), interval=0.05)

        elif act == "hotkey":
            keys = action.get("keys", [])
            pyautogui.hotkey(*keys)

        elif act == "click":
            if "x" in action and "y" in action:
                pyautogui.click(action["x"], action["y"])
            else:
                pyautogui.click()

        elif act == "open_url":
            url = action.get("url")
            if url:
                webbrowser.open(url)

        else:
            logger.warning(f"⚠️ Unknown action: {action}")

    except Exception as e:
        logger.error(f"❌ Error executing action {action}: {e}")
