#!/usr/bin/env python3
"""Save after each chapter"""
import json, subprocess, os, sys

TARGET = sys.argv[1] if len(sys.argv) > 1 else "km"
MODEL = "opencode/hy3-preview-free"
LANG = {"km": "Khmer (ខ្មែរ)", "ceb": "Bisaya"}.get(TARGET, TARGET)

def tr(text):
    cmd = f'echo "Translate to {LANG}: {text}" | /home/tali/.opencode/bin/opencode run --model {MODEL}'
    result = subprocess.run(cmd, shell=True, capture_output=True, timeout=90, cwd="/home/tali/tali-book")
    out = result.stdout.decode()
    if "·" in out:
        out = out.split("·", 1)[1].strip()
    return out if out else text

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
if idx < len(ch):
    c = ch[idx]
    print(f"=== Ch{c['num']} ===")
    
    t = {"num": c["num"], "title": "", "part": "", "part_num": c["part_num"], "paragraphs": [], "word_count": c["word_count"]}
    
    print(" title", end="", flush=True)
    t["title"] = tr(c["title"])
    print(" OK")
    
    print(" part", end="", flush=True)
    t["part"] = tr(c["part"])
    print(" OK")
    
    for j, p in enumerate(c["paragraphs"]):
        print(f" p{j+1}", end="", flush=True)
        t["paragraphs"].append(tr(p))
        print(".", end="", flush=True)
    
    print(" done")
    d.append(t)
    
    with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    
    print(f"Saved ch{c['num']}")
else:
    print("All done")