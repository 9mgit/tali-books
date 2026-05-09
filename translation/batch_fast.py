#!/usr/bin/env python3
"""Fast batch"""
import json, subprocess, os, sys

TARGET = sys.argv[1] if len(sys.argv) > 1 else "km"
MODEL = "opencode/nemotron-3-super-free"
LANG = {"km": "Khmer (ខ្មែរ)", "ceb": "Bisaya"}.get(TARGET, TARGET)

def tr(text):
    p = f"Translate to {LANG}: {text}".encode()
    proc = subprocess.Popen(
        ["/home/tali/.opencode/bin/opencode", "run", "--model", MODEL],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd="/home/tali/tali-book"
    )
    try:
        out, _ = proc.communicate(input=p, timeout=60)
        r = out.decode()
        if "·" in r: r = r.split("·", 1)[1].strip()
        return r or text
    except:
        proc.kill()
        return text

os.chdir("/home/tali/tali-book")
ch = json.load(open("data/chapters.json"))

d = []
try:
    d = json.load(open(f"data/translations/chapters_{TARGET}.json"))
except:
    pass

start = len(d)
print(f"Resume ch{start+1}/{len(ch)}")

for i in range(start, len(ch)):
    c = ch[i]
    print(f"Ch{c['num']}", end=" ", flush=True)
    t = {"num": c["num"], "title": tr(c["title"]), "part": tr(c["part"]), "part_num": c["part_num"], "paragraphs": [], "word_count": c["word_count"]}
    for p in c["paragraphs"]:
        t["paragraphs"].append(tr(p))
        print(".", end="", flush=True)
    d.append(t)
    with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f" OK")