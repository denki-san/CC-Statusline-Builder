
import os
import re
import json

THEMES_DIR = "themes"
PREVIEW_FILE = "preview.html"

def ansi256_to_hex(code):
    """Convert ANSI 256-color code to hex color string."""
    code = int(code)
    # Standard colors 0-15 (approximate)
    standard_colors = [
        "#000000", "#800000", "#008000", "#808000", "#000080", "#800080", "#008080", "#c0c0c0",
        "#808080", "#ff0000", "#00ff00", "#ffff00", "#0000ff", "#ff00ff", "#00ffff", "#ffffff"
    ]
    if code < 16:
        return standard_colors[code]
    
    # 216-color cube (16-231)
    if code < 232:
        idx = code - 16
        b = idx % 6
        g = (idx // 6) % 6
        r = idx // 36
        def c(v): return 0 if v == 0 else 55 + v * 40
        return f"#{c(r):02x}{c(g):02x}{c(b):02x}"
    
    # Grayscale (232-255)
    gray = (code - 232) * 10 + 8
    return f"#{gray:02x}{gray:02x}{gray:02x}"


def extract_ansi256_color(content, var_name):
    """Extract an ANSI 256-color from a shell script variable."""
    # Matches: VAR_NAME="\033[38;5;NNNm"  or  VAR="\033[38;5;NNNm"
    match = re.search(rf'{var_name}=".*?38;5;(\d+)m"', content)
    if match:
        return ansi256_to_hex(match.group(1))
    return None


def parse_theme(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    theme_id = filename.replace(".sh", "")
    
    # Name from comments or filename
    name_match = re.search(r'^# (.+?)(?:\s+主题|$)', content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else theme_id
    # Prefer the theme_id as the display name (already formatted nicely)
    # e.g. "01-tokyo-night" -> "01-Tokyo-Night"
    name = "-".join(part.capitalize() for part in theme_id.split("-"))
    
    # Category heuristic
    category = "classic"
    for kw, cat in [("cyber", "special"), ("hacker", "special"), ("neon", "special"),
                    ("pastel", "soft"), ("dream", "soft"), ("soft", "soft"),
                    ("candy", "special"), ("matrix", "special"), ("galaxy", "special")]:
        if kw in theme_id.lower():
            category = cat
            break
    
    # Extract actual colors from the script
    model_color = extract_ansi256_color(content, "MODEL_COLOR") or "#c0caf5"
    progress_low = extract_ansi256_color(content, "PROGRESS_LOW") or model_color
    progress_mid = extract_ansi256_color(content, "PROGRESS_MID") or model_color
    progress_high = extract_ansi256_color(content, "PROGRESS_HIGH") or "#f7768e"

    # Extract progress fill characters
    filled_match = re.search(r'PROGRESS_FILLED="(.+?)"', content)
    empty_match = re.search(r'PROGRESS_EMPTY="(.+?)"', content)
    filled_char = filled_match.group(1) if filled_match else "█"
    empty_char = empty_match.group(1) if empty_match else "░"
    
    # 5 chars: 3 filled, 2 empty simulates 32% context
    progress_chars = [filled_char, filled_char, filled_char, empty_char, empty_char]
    
    return {
        "id": theme_id,
        "name": name,
        "category": category,
        "lang": "BASH",
        "modelColor": model_color,
        "progressLow": progress_low,
        "progressMid": progress_mid,
        "progressHigh": progress_high,
        "progressChars": progress_chars,
        "tokenText": "Total: input 216k / output 15k",
        "code": content
    }

def main():
    themes = []
    for filename in os.listdir(THEMES_DIR):
        if filename.endswith(".sh"):
            themes.append(parse_theme(os.path.join(THEMES_DIR, filename)))
    
    # Sort themes by name
    themes.sort(key=lambda x: x["name"])
    
    # Read preview.html
    with open(PREVIEW_FILE, "r") as f:
        html = f.read()
    
    # Inject themes JSON
    themes_json = json.dumps(themes, indent=4)
    
    themes_json = json.dumps(themes, indent=4)
    
    start_marker = "// THEMES_DEFINITION_START"
    end_marker = "// THEMES_DEFINITION_END"
    
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        # Construct new content
        # We want to keep the start_marker, insert the new themes, and keep the end_marker
        # The content between them will be replaced.
        # So we slice up to start_marker + len(start_marker)
        # And we slice from end_idx
        
        prefix = html[:start_idx + len(start_marker)]
        suffix = html[end_idx:]
        
        new_html = prefix + "\n    const themes = " + themes_json + ";\n    " + suffix
        
        with open(PREVIEW_FILE, "w") as f:
            f.write(new_html)
        print(f"Injected {len(themes)} themes into {PREVIEW_FILE} using MARKERS")
    else:
        print("Could not find delimiters for injection.")
        # Fallback logic only if markers are missing
        # ... logic removed to avoid dangerous replacements ...
        print("Error: Markers not found. Please ensure preview.html has // THEMES_DEFINITION_START and // THEMES_DEFINITION_END")

if __name__ == "__main__":
    main()
