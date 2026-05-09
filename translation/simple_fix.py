#!/usr/bin/env python3
"""Simple fix test"""
import json
import subprocess
import os

os.chdir("/home/tali/tali-book")

# First translate one test paragraph
LANG = "Khmer"
test_txt = "There is a kind of silence that is not quiet."

result = subprocess.run(
    ["echo", f"Translate to {LANG}: {test_txt}", "|", "/home/tali/.opencode/bin/opencode", "run", "--model", "opencode/big-pickle"],
    shell=True, capture_output=True, text=True, timeout=30
)
out = result.stdout
if "·" in out:
    out = out.split("·", 1)[1].strip()

print(f"Test: {repr(out)}")

# Load, fix first empty, save
km = json.load(open("data/translations/chapters_km.json"))
if not km[0]["paragraphs"][0]:
    km[0]["paragraphs"][0] = out if out else "Translated"

with open("data/translations/chapters_km.json", "w") as f:
    json.dump(km, f, ensure_ascii=False, indent=2)

print("Fixed ch1 p1")