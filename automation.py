import subprocess
import pyautogui
import time
import json

def run_action(command_str):
    try:
        actions = json.loads(command_str)
        for act in actions:
            action = act.get("action")
            if action == "open":
                subprocess.Popen(act["app"])
                time.sleep(1)
            elif action == "type":
                pyautogui.write(act["text"], interval=0.05)
            elif action == "press":
                pyautogui.press(act["key"])
            elif action == "wait":
                time.sleep(act["seconds"])
            elif action == "screenshot":
                pyautogui.screenshot("screenshot.png")
    except Exception as e:
        print(f"Execution Error: {e}")
