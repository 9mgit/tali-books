#!/usr/bin/env python3
"""Batch translate using stdin file"""
import json, subprocess, os, sys, tempfile

TARGET = sys.argv[1] if len(sys.argv) > 1 else "km"
MODEL = "opencode/nemotron-3-super-free"
LANG = {"km": "Khmer (ខ្មែរ)", "ceb": "Bisaya"}.get(TARGET, TARGET)

def tr(text):
    prompt = f"Translate to {LANG}: {text}"
    # Use temp file for stdin
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(prompt)
        tf = f.name
    
    try:
        result = subprocess.run(
            ["/home/tali/.opencode/bin/opencode", "run", "--model", MODEL],
            stdin=open(tf), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd="/home/tali/tali-book", timeout=60
        )
        os.unlink(tf)
        out = result.stdout.decode()
        if "·" in out:
            out = out.split("·", 1)[1].strip()
        return out if out else text
    except Exception as e:
        try: os.unlink(tf)
        except: pass
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