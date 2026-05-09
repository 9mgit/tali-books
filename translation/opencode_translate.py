#!/usr/bin/env python3
"""
Translate using OpenCode CLI
"""
import subprocess
import json
import os
import sys

def translate_chapter(chapter, target_lang, model="opencode/minimax-m2.5-free"):
    """Translate single chapter using OpenCode"""
    chapter_json = json.dumps(chapter, ensure_ascii=False)
    
    lang_names = {
        "km": "Khmer (ខ្មែរ)",
        "ceb": "Bisaya",
    }
    target = lang_names.get(target_lang, target_lang)
    
    prompt = f"""Translate this chapter from English to {target}.
Requirements:
- Output ONLY valid JSON
- Preserve JSON structure (num, title, part, part_num, paragraphs, word_count)
- Keep *emphasis* markers
- Keep --- dividers exactly
- word_count unchanged
- Maintain literary tone

{chapter_json}

JSON:"""

    try:
        result = subprocess.run([
            "opencode", "run", 
            f"--model {model}",
            prompt
        ], capture_output=True, text=True, timeout=60, cwd="/home/tali/tali-book")
        
        if result.returncode != 0:
            print(f"Error: {result.stderr[:200]}")
            return None
            
        # Try to extract JSON
        text = result.stdout
        # Find JSON array
        if "[" in text:
            start = text.find("[")
            # Try to find matching end
            try:
                data = json.loads(text[start:])
                return data
            except:
                pass
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "km"
    model = sys.argv[2] if len(sys.argv) > 2 else "opencode/minimax-m2.5-free"
    
    with open("data/chapters.json") as f:
        chapters = json.load(f)
    
    print(f"Translating to {target} using {model}")
    
    # Test with first chapter
    result = translate_chapter(chapters[0], target, model)
    if result:
        print("Translation successful!")
        print(json.dumps(result, ensure_ascii=False, indent=2)[:500])
    else:
        print("Translation failed")