import re
import threading

def sanitize_json(text):
    # Remove backticks and triple quotes
    text = re.sub(r"```(json)?", "", text.strip())
    # Fix common JSON issues
    text = re.sub(r",\s*([\]}])", r"\1", text)  # Remove trailing commas
    text = re.sub(r"(\w+):", r'"\1":', text)    # Unquoted keys
    return text.strip()

def run_with_timeout(func, args=(), kwargs={}, timeout=30):
    result = [None]
    exception = [None]

    def wrapper():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return None
    if exception[0]:
        raise exception[0]
    return result[0]
