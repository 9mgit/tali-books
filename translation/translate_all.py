#!/usr/bin/env python3
"""Translate with timeout and save on each para"""
import json, subprocess, os, sys, time

TARGET = sys.argv[1] if len(sys.argv) > 1 else "km"
MODEL = "opencode/hy3-preview-free"
LANG = {"km": "Khmer (ខ្មែរ)", "ceb": "Bisaya"}.get(TARGET, TARGET)

def tr(text, timeout=30):
    cmd = f'echo "Translate to {LANG}: {text}" | /home/tali/.opencode/bin/opencode run --model {MODEL}'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout, cwd="/home/tali/tali-book")
        out = result.stdout.decode()
        if "·" in out:
            out = out.split("·", 1)[1].strip()
        return out if out else text
    except:
        return text

os.chdir("/home/tali/tali-book")
ch = json.load(open("data/chapters.json"))

d = []
try:
    d = json.load(open(f"data/translations/chapters_{TARGET}.json"))
except:
    pass

start = len(d)
print(f"Start ch{start+1}/{len(ch)}")

idx = start
while idx < len(ch):
    c = ch[idx]
    print(f"Ch{c['num']}", end=" ", flush=True)
    
    t = {"num": c["num"], "title": tr(c["title"]), "part": tr(c["part"]), "part_num": c["part_num"], "paragraphs": [], "word_count": c["word_count"]}
    
    for j, p in enumerate(c["paragraphs"]):
        tp = tr(p, timeout=30)
        t["paragraphs"].append(tp)
        print(".", end="", flush=True)
        time.sleep(0.5)
    
    d.append(t)
    with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f" OK")
    idx += 1
    time.sleep(1)

print("Done")