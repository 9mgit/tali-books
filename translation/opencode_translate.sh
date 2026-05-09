#!/bin/bash
# Translate using OpenCode CLI
# Usage: ./opencode_translate.sh <lang_code>

LANG=$1
OUTPUT_FILE="data/translations/chapters_${LANG}.json"
CHAPTERS=""
if [ -n "$2" ]; then
    CHAPTERS="--chapters $2"
fi

echo "Translating to $LANG using OpenCode..."

# Use opencode run to translate
/home/tali/opencode-bin/opencode run "Translate the chapters from data/chapters.json to language code $LANG. 
Output the complete translated JSON to $OUTPUT_FILE with structure:
{\"chapters\": [...translated chapters...]}

Requirements:
- Use model opencode/minimax-m2.5-free
- Translate all 59 chapters
- Preserve JSON structure
- Keep *emphasis* markers  
- Keep --- dividers
- Maintain literary tone
- Keep word_count unchanged

Execute: python3 translation/translate.py --lang $LANG"

echo "Translation initiated. Check $OUTPUT_FILE for results."