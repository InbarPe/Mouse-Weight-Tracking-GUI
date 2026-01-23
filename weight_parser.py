import re

def extract_weight(txt_path):
    # Matches integers or decimals before % (case-insensitive)
    pattern = re.compile(r"BW.*?(\d+(?:\.\d+)?)\s*%", re.IGNORECASE)

    with open(txt_path, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                return float(match.group(1))

    raise ValueError(f"BW not found in file: {txt_path}")
