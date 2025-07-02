import subprocess
import time
import logging
import pyautogui
import webbrowser

logger = logging.getLogger("PromptPilot-Executor")
logger.setLevel(logging.INFO)

def execute_actions(actions):
    for action in actions:
        try:
            act = action.get("action", "").lower()

            if act == "open_app":
                app = action.get("name")
                subprocess.Popen(app)
                logger.info(f"🟢 Opened app: {app}")

            elif act == "switch_tab":
                pyautogui.hotkey("ctrl", "t")
                logger.info("🟢 Opened new browser tab.")

            elif act == "wait":
                seconds = float(action.get("seconds", 1))
                time.sleep(seconds)
                logger.info(f"⏱️ Waited for {seconds} seconds.")

            elif act == "open_url":
                site = action.get("site") or action.get("url")
                if site:
                    webbrowser.open(site)
                    logger.info(f"🌐 Opened URL: {site}")

            elif act == "type":
                text = action.get("text") or action.get("value", "")
                pyautogui.write(text, interval=0.05)
                logger.info(f"⌨️ Typed: {text}")

            elif act == "hotkey":
                keys = action.get("keys", [])
                pyautogui.hotkey(*keys)
                logger.info(f"⌨️ Pressed hotkeys: {' + '.join(keys)}")

            else:
                logger.warning(f"⚠️ Unknown action: {action}")

        except Exception as e:
            logger.error(f"❌ Error executing action {action}: {e}")
