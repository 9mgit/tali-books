#!/usr/bin/env python3
"""
Translate using OpenCode CLI as the backend
"""
import subprocess
import json
import os

def translate_with_opencode(chapters, target_lang):
    """Use opencode to translate chapters"""
    
    lang_prompts = {
        "km": "Khmer (ខ្មែរ)",
        "ceb": "Bisaya",
    }
    
    target = lang_prompts.get(target_lang, target_lang)
    
    # Create a simple prompt to translate
    chapters_json = json.dumps(chapters[:3], ensure_ascii=False, indent=2)  # First 3 for test
    
    prompt = f"""Translate these 3 chapters from English to {target}. 

Return ONLY valid JSON array with translated chapters. Preserve:
- JSON structure (num, title, part, part_num, paragraphs, word_count)
- Keep *emphasis* markers
- Keep --- dividers exactly as-is
- word_count unchanged

{chapters_json}

Output JSON only:"""

    # Run opencode
    result = subprocess.run([
        "ssh", "tali@10.99.99.11",
        f"echo '{prompt}' | /home/tali/.opencode/bin/opencode run"
    ], capture_output=True, text=True, timeout=120)
    
    print("STDOUT:", result.stdout[:500] if result.stdout else "empty")
    print("STDERR:", result.stderr[:500] if result.stderr else "empty")
    return result.stdout

if __name__ == "__main__":
    with open("data/chapters.json") as f:
        chapters = json.load(f)
    
    # Test translate to Khmer
    translate_with_opencode(chapters, "km")