#!/usr/bin/env python3
"""Safe sequential batch translate"""
import json
import subprocess
import sys
import time
import os

TARGET = sys.argv[1] if len(sys.argv) > 1 else "km"
MODEL = "opencode/hy3-preview-free"

LANG = {"km": "Khmer (ខ្មែរ)", "ceb": "Bisaya"}.get(TARGET, TARGET)

os.chdir("/home/tali/tali-book")

with open("data/chapters.json") as f:
    chapters = json.load(f)

try:
    with open(f"data/translations/chapters_{TARGET}.json") as f:
        done = json.load(f)
    start = len(done)
except:
    done = []
    start = 0

print(f"Start ch{start+1}/{len(chapters)}")

for idx in range(start, len(chapters)):
    ch = chapters[idx]
    print(f"Ch{ch['num']}", end=" ", flush=True)
    
    t = {"num": ch["num"], "title": "", "part": "", "part_num": ch["part_num"], "paragraphs": [], "word_count": ch["word_count"]}
    
    for i, para in enumerate(ch["paragraphs"]):
        prompt = f"Translate to {LANG}: {para}"
        result = subprocess.run(
            ["echo", prompt, "|", "/home/tali/.opencode/bin/opencode", "run", "--model", MODEL],
            shell=True, capture_output=True, text=True, timeout=60, cwd="/home/tali/tali-book"
        )
        out = result.stdout
        if "·" in out:
            out = out.split("·", 1)[1].strip()
        if out:
            t["paragraphs"].append(out)
        else:
            t["paragraphs"].append(para)
        print(".", end="", flush=True)
        time.sleep(0.5)
    
    title_prompt = f"Translate to {LANG}: {ch['title']}"
    result = subprocess.run(
        ["echo", title_prompt, "|", "/home/tali/.opencode/bin/opencode", "run", "--model", MODEL],
        shell=True, capture_output=True, text=True, timeout=60, cwd="/home/tali/tali-book"
    )
    out = result.stdout
    if "·" in out:
        t["title"] = out.split("·", 1)[1].strip()
    else:
        t["title"] = ch["title"]
    
    part_prompt = f"Translate to {LANG}: {ch['part']}"
    result = subprocess.run(
        ["echo", part_prompt, "|", "/home/tali/.opencode/bin/opencode", "run", "--model", MODEL],
        shell=True, capture_output=True, text=True, timeout=60, cwd="/home/tali/tali-book"
    )
    out = result.stdout
    if "·" in out:
        t["part"] = out.split("·", 1)[1].strip()
    else:
        t["part"] = ch["part"]
    
    done.append(t)
    with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
        json.dump(done, f, ensure_ascii=False, indent=2)
    print(" OK")
    time.sleep(1)

print("Done!")