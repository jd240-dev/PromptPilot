import atexit
import os

LOG_FILE = "promptpilot.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def delete_logs():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

atexit.register(delete_logs)
