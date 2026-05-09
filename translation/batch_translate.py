#!/usr/bin/env python3
"""Simple batch translate"""
import json, subprocess, time, os, sys

TARGET = sys.argv[1] if len(sys.argv) > 1 else "km"
MODEL = "opencode/nemotron-3-super-free"
LANG = {"km": "Khmer (ខ្មែរ)", "ceb": "Bisaya"}.get(TARGET, TARGET)

def tr(text):
    proc = subprocess.Popen(
        ["/home/tali/.opencode/bin/opencode", "run", "--model", MODEL],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd="/home/tali/tali-book"
    )
    try:
        out, _ = proc.communicate(input=f"Translate to {LANG}: {text}".encode(), timeout=90)
        result = out.decode()
        if "·" in result:
            result = result.split("·", 1)[1].strip()
        return result
    except:
        proc.kill()
        return text

os.chdir("/home/tali/tali-book")
chapters = json.load(open("data/chapters.json"))

# Check progress
done = []
try:
    done = json.load(open(f"data/translations/chapters_{TARGET}.json"))
except:
    pass

start = len(done)
print(f"Start ch{start+1}/{len(chapters)}")

# Translate chapter 1
if start < 1:
    ch = chapters[0]
    print(f"Ch{ch['num']} title...", end=" ", flush=True)
    title = tr(ch["title"])
    print("done")
    print(f"Ch{ch['num']} part...", end=" ", flush=True)
    part = tr(ch["part"])
    print("done")
    print(f"Ch{ch['num']} paras...", end=" ", flush=True)
    paragraphs = []
    for i, p in enumerate(ch["paragraphs"]):
        tp = tr(p)
        paragraphs.append(tp if tp else p)
        if (i+1) % 10 == 0:
            print(i+1, end=" ", flush=True)
    print("done")
    
    t = {"num": ch["num"], "title": title, "part": part, "part_num": ch["part_num"], "paragraphs": paragraphs, "word_count": ch["word_count"]}
    done.append(t)
    with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
        json.dump(done, f, ensure_ascii=False, indent=2)
    print(f"SAVED ch{ch['num']}")

# Continue
for idx in range(start, len(chapters)):
    ch = chapters[idx]
    print(f"Ch{ch['num']}")
    title = tr(ch["title"])
    part = tr(ch["part"])
    paragraphs = []
    for p in ch["paragraphs"]:
        tp = tr(p)
        paragraphs.append(tp if tp else p)
    t = {"num": ch["num"], "title": title, "part": part, "part_num": ch["part_num"], "paragraphs": paragraphs, "word_count": ch["word_count"]}
    done.append(t)
    with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
        json.dump(done, f, ensure_ascii=False, indent=2)
    print(f"SAVED ch{ch['num']}")
    time.sleep(1)