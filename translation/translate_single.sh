#!/bin/bash
# Simple translation script - translate one chapter at a time using single model
# Usage: ./translate_single.sh <lang_code>
# Example: ./translate_single.sh es

LANG=$1
if [ -z "$LANG" ]; then
    echo "Usage: $0 <lang_code>"
    echo "Languages: es, fr, de, zh-CN, ja, pt, ar, hi, ru, ko, it, tl, ceb, id, vi, th, km"
    exit 1
fi

API_KEY=${OPENROUTER_API_KEY:-$(cat .api_key 2>/dev/null)}
if [ -z "$API_KEY" ]; then
    echo "ERROR: Set OPENROUTER_API_KEY or create .api_key file"
    exit 1
fi

# Language config
declare -A LANG_NAME
LANG_NAME[es]="Spanish"
LANG_NAME[fr]="French"
LANG_NAME[de]="German"
LANG_NAME[zh-CN]="Chinese Simplified"
LANG_NAME[ja]="Japanese"
LANG_NAME[pt]="Portuguese"
LANG_NAME[ar]="Arabic"
LANG_NAME[hi]="Hindi"
LANG_NAME[ru]="Russian"
LANG_NAME[ko]="Korean"
LANG_NAME[it]="Italian"
LANG_NAME[tl]="Tagalog"
LANG_NAME[ceb]="Bisaya"
LANG_NAME[id]="Bahasa Indonesia"
LANG_NAME[vi]="Vietnamese"
LANG_NAME[th]="Thai"
LANG_NAME[km]="Khmer"

TARGET="${LANG_NAME[$LANG]}"
OUTPUT_DIR="data/translations"

echo "Translating to $TARGET..."

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Read chapter file and translate
# This is a simplified single-model version
# For full council, use translate.py

echo "Using: translate.py --lang $LANG"
python3 translate.py --lang "$LANG" --key "$API_KEY"