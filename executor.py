import time
import pyautogui
import subprocess
from logger import log

def execute_actions(actions):
    for action in actions:
        try:
            if action["action"] == "open":
                subprocess.Popen(action["app"])
            elif action["action"] == "wait":
                time.sleep(action["seconds"])
            elif action["action"] == "type":
                pyautogui.write(action["text"])
            elif action["action"] == "hotkey":
                pyautogui.hotkey(*action["keys"])
            elif action["action"] == "click":
                pyautogui.click()
            else:
                log(f"⚠️ Unknown action: {action}")
        except Exception as e:
            log(f"❌ Failed to execute {action}: {e}")
