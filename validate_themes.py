
import json
import re

PREVIEW_FILE = "preview.html"

def validate_json():
    with open(PREVIEW_FILE, "r") as f:
        content = f.read()
    
    # Extract the themes array
    # It starts with "const themes = [" and ends with "];"
    match = re.search(r'const themes = (\[.*?\]);', content, re.DOTALL)
    if not match:
        print("Could not find themes array")
        return
    
    json_str = match.group(1)
    
    try:
        json.loads(json_str)
        print("JSON is valid!")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        # Print context
        lines = json_str.splitlines()
        err_line = e.lineno - 1
        print(f"Line {err_line}: {lines[err_line]}")
        if err_line > 0:
            print(f"Prev: {lines[err_line-1]}")
        if err_line < len(lines) - 1:
            print(f"Next: {lines[err_line+1]}")

if __name__ == "__main__":
    validate_json()
