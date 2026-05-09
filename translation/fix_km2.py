#!/usr/bin/env python3
"""Re-translate missing paragraphs using big-pickle"""
import json
import subprocess
import sys
import time
import os

TARGET = "km"
MODEL = "opencode/big-pickle"  # Use this instead
LANG = "Khmer (ខ្មែរ)"

os.chdir("/home/tali/tali-book")

with open("data/chapters.json") as f:
    chapters = json.load(f)

with open(f"data/translations/chapters_{TARGET}.json") as f:
    km = json.load(f)

missing = []
for ch_idx, ch in enumerate(chapters):
    km_ch = km[ch_idx]
    for p_idx, (src_para, km_para) in enumerate(zip(ch["paragraphs"], km_ch["paragraphs"])):
        if not any(ord(c) > 127 for c in km_para[:20]):
            missing.append((ch_idx, ch["num"], p_idx, src_para))

print(f"Found {len(missing)} missing paragraphs")
print(f"Using model: {MODEL}")

for i, (ch_idx, ch_num, p_idx, src) in enumerate(missing):
    prompt = f"Translate to {LANG}: {src}"
    result = subprocess.run(
        ["echo", prompt, "|", "/home/tali/.opencode/bin/opencode", "run", "--model", MODEL],
        shell=True, capture_output=True, text=True, timeout=90, cwd="/home/tali/tali-book"
    )
    out = result.stdout
    if "·" in out:
        out = out.split("·", 1)[1].strip()
    
    if out and any(ord(c) > 127 for c in out[:10]):
        km[ch_idx]["paragraphs"][p_idx] = out
        print(f"{i+1}/{len(missing)} Ch{ch_num}p{p_idx+1}: OK")
    else:
        print(f"{i+1}/{len(missing)} Ch{ch_num}p{p_idx+1}: FAILED")
    
    time.sleep(0.5)
    
    if (i+1) % 50 == 0:
        with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
            json.dump(km, f, ensure_ascii=False, indent=2)
        print("Saved progress")

with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
    json.dump(km, f, ensure_ascii=False, indent=2)

print("Done!")