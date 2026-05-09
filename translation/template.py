import json
import re

# Source chapters
with open('data/chapters.json') as f:
    chapters = json.load(f)

# You are translating these chapters to {lang}
# Preserve:
# - JSON structure exactly  
# - *emphasis* markers
# - --- dividers
# - Literary tone

# Output wrapped JSON with chapters + basic cover (no cover translation needed)

output = {"chapters": chapters}

with open('data/translations/chapters_{lang}.json', 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Output to data/translations/chapters_{{lang}}.json - {len(chapters)} chapters")