#!/usr/bin/env python3
"""Re-translate missing paragraphs"""
import json
import subprocess
import sys
import time
import os

TARGET = "km"  # Khmer
MODEL = "opencode/hy3-preview-free"
LANG = "Khmer (ខ្មែរ)"

os.chdir("/home/tali/tali-book")

# Load source and translation
with open("data/chapters.json") as f:
    chapters = json.load(f)

with open(f"data/translations/chapters_{TARGET}.json") as f:
    km = json.load(f)

# Check each paragraph
missing = []
for ch_idx, ch in enumerate(chapters):
    km_ch = km[ch_idx]
    for p_idx, (src_para, km_para) in enumerate(zip(ch["paragraphs"], km_ch["paragraphs"])):
        # Check if it's English (not translated)
        if not any(ord(c) > 127 for c in km_para[:20]):  # No non-ASCII chars
            missing.append((ch_idx, ch["num"], p_idx, src_para[:50]))

print(f"Found {len(missing)} missing paragraphs")
print(f"Re-translating...")

# Re-translate missing
for ch_idx, ch_num, p_idx, src in missing[:50]:  # Limit to avoid overload
    prompt = f"Translate to {LANG}: {src}"
    result = subprocess.run(
        ["echo", prompt, "|", "/home/tali/.opencode/bin/opencode", "run", "--model", MODEL],
        shell=True, capture_output=True, text=True, timeout=60, cwd="/home/tali/tali-book"
    )
    out = result.stdout
    if "·" in out:
        out = out.split("·", 1)[1].strip()
    
    if out and any(ord(c) > 127 for c in out[:10]):  # Has Khmer chars
        km[ch_idx]["paragraphs"][p_idx] = out
        print(f"Ch{ch_num} p{p_idx+1}: OK")
    else:
        print(f"Ch{ch_num} p{p_idx+1}: FAILED")
    
    time.sleep(0.5)

# Save
with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
    json.dump(km, f, ensure_ascii=False, indent=2)

print("Done!")