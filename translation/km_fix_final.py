#!/usr/bin/env python3
"""Full re-translate - log to file"""
import json, subprocess, time, os, sys

TARGET = "km"
MODEL = "opencode/big-pickle"
LANG = "Khmer (ខ្មែរ)"

log = open("/tmp/km_fix.log", "w")

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

log.write(f"Found {len(missing)} missing\n")
log.flush()
print(f"Found {len(missing)} missing")

for i, (ch_idx, ch_num, p_idx, src) in enumerate(missing):
    result = subprocess.run(
        ["echo", f"Translate to {LANG}: {src}", "|", "/home/tali/.opencode/bin/opencode", "run", "--model", MODEL],
        shell=True, capture_output=True, text=True, timeout=30, cwd="/home/tali/tali-book"
    )
    out = result.stdout
    if "·" in out:
        out = out.split("·", 1)[1].strip()
    
    if out:
        km[ch_idx]["paragraphs"][p_idx] = out
        log.write(f"{i+1}: OK\n")
    else:
        log.write(f"{i+1}: FAILED\n")
    log.flush()
    
    if (i+1) % 100 == 0:
        log.write(f"Saving at {i+1}\n")
        with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
            json.dump(km, f, ensure_ascii=False, indent=2)
        print(f"{i+1}/{len(missing)}")
    
    time.sleep(0.3)

with open(f"data/translations/chapters_{TARGET}.json", "w") as f:
    json.dump(km, f, ensure_ascii=False, indent=2)

log.write("Done!\n")
print("Done!")

log.close()