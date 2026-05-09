#!/usr/bin/env python3
"""Simple batch translate using shell"""
import json, subprocess, os, sys

TARGET = sys.argv[1] if len(sys.argv) > 1 else "km"
MODEL = "opencode/hy3-preview-free"
LANG = {"km": "Khmer (ខ្មែរ)", "ceb": "Bisaya"}.get(TARGET, TARGET)

def tr(text):
    cmd = f'echo "Translate to {LANG}: {text}" | /home/tali/.opencode/bin/opencode run --model {MODEL}'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, timeout=90, cwd="/home/tali/tali-book")
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
print(f"Resume ch{start+1}/{len(ch)} using {MODEL}")

for i in range(start, len(ch)):
    c = ch[i]
    print(f"Ch{c['num']}", end=" ", flush=True)
    t = {"num": c["num"], "title": "", "part": "", "part_num": c["part_num"], "paragraphs": [], "word_count": c["word_count"]}
    t["title"] = tr(c["title"])
    t["part"] = tr(c["part"])
    for p in c["paragraphs"]:
        t["paragraphs"].append(tr(p))
        print(".", end="", flush=True)
    d.append(t)
    with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(" OK")