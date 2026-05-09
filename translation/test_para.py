#!/usr/bin/env python3
"""Single paragraph test"""
import json, subprocess, os

MODEL = "opencode/hy3-preview-free"
LANG = "Khmer (ខ្មែរ)"

os.chdir("/home/tali/tali-book")
ch = json.load(open("data/chapters.json"))

# Test translate first paragraph of ch2
c = ch[1]
p = c["paragraphs"][0]
print(f"Original: {p[:50]}...")

cmd = f'echo "Translate to {LANG}: {p}" | /home/tali/.opencode/bin/opencode run --model {MODEL}'
result = subprocess.run(cmd, shell=True, capture_output=True, timeout=90)
out = result.stdout.decode()
if "·" in out:
    out = out.split("·", 1)[1].strip()
print(f"Translated: {out[:50]}...")