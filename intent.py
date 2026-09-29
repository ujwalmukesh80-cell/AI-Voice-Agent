import re

def detect_budget(text):

    text = text.lower()

    numbers = re.findall(r'\d+', text)

    if not numbers:
        return None

    value = int(numbers[0])

    if "crore" in text:
        return value * 10000000

    if "lakh" in text or "lakhs" in text:
        return value * 100000

    return value