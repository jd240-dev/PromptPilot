import re

def clean_json(text):
    text = text.strip("` \n")  # remove markdown code block markers
    if text.startswith("json"):
        text = text[4:]
    # Remove trailing commas and comments
    text = re.sub(r",\s*([\]}])", r"\1", text)
    text = re.sub(r"//.*", "", text)
    return text
