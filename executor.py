import time
import subprocess
import pyautogui

def execute_action(action):
    act = action.get("action")

    if act == "open" or act == "open_application":
        subprocess.Popen(action["app"], shell=True)

    elif act == "type":
        pyautogui.write(action["text"], interval=0.05)

    elif act == "press":
        pyautogui.press(action["key"])

    elif act == "wait":
        time.sleep(action["seconds"])

    elif act == "click":
        pyautogui.click()

def execute_all(actions):
    for action in actions:
        try:
            execute_action(action)
        except Exception as e:
            print(f"⚠️ Action failed: {action} -> {e}")
