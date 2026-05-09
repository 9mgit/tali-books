#!/usr/bin/env python3
"""Translate chapters using OpenCode CLI on server"""
import json
import subprocess
import sys

TARGET_LANG = sys.argv[1] if len(sys.argv) > 1 else "km"
MODEL = "opencode/minimax-m2.5-free"

LANG_PROMPTS = {
    "km": "Khmer (ខ្មែរ)",
    "ceb": "Bisaya",
}
TARGET = LANG_PROMPTS.get(TARGET_LANG, TARGET_LANG)

def translate_text(text):
    """Translate text to target language"""
    prompt = f"""Translate to {TARGET}. Output ONLY the translation, no explanation.

{text}

Translation:"""
    
    result = subprocess.run(
        ["echo", f"'{prompt}'", "|", "/home/tali/.opencode/bin/opencode", "run", f"--model {MODEL}"],
        shell=True, capture_output=True, text=True, timeout=60, cwd="/home/tali/tali-book"
    )
    
    if result.returncode != 0:
        print(f"Error: {result.stderr[:200]}")
        return None
    
    output = result.stdout
    if "·" in output:
        output = output.split("·", 1)[1].strip()
    return output

def translate_chapter(chapter):
    """Translate a single chapter"""
    trans = {
        "num": chapter["num"],
        "title": translate_text(chapter["title"]),
        "part": translate_text(chapter["part"]),
        "part_num": chapter["part_num"],
        "paragraphs": [],
        "word_count": chapter["word_count"]
    }
    
    for para in chapter["paragraphs"]:
        trans_para = translate_text(para)
        if trans_para:
            trans["paragraphs"].append(trans_para)
        else:
            trans["paragraphs"].append(para)
    
    return trans

def main():
    with open("data/chapters.json") as f:
        chapters = json.load(f)
    
    existing = []
    try:
        with open(f"data/translations/chapters_{TARGET_LANG}.json") as f:
            existing = json.load(f)
    except:
        pass
    
    start = len(existing)
    print(f"Translating chapter {start + 1} onwards to {TARGET}...")
    
    for i, ch in enumerate(chapters[start:], start):
        print(f"Chapter {ch['num']} ({i+1}/{len(chapters)})")
        trans_ch = translate_chapter(ch)
        
        existing.append(trans_ch)
        
        with open(f"data/translations/chapters_{TARGET_LANG}.json", "w") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        
        print(f"Saved chapter {ch['num']}")

if __name__ == "__main__":
    main()