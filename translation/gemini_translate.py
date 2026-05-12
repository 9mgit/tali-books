#!/usr/bin/env python3
"""
Gemini translation script
"""
import os
import json
import asyncio
import aiohttp
from pathlib import Path

LANGUAGES = {
    "km": ("Khmer", "ខ្មែរ"),
    "ceb": ("Bisaya", "Bisaya"),
}

SOURCE_FILE = "data/chapters.json"
OUTPUT_DIR = Path("data/translations")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"


async def translate_chapter(chapter, target_lang, target_name):
    """Translate single chapter using Gemini"""
    chapter_json = json.dumps(chapter, ensure_ascii=False)
    
    prompt = f"""Translate the following chapter from English to {target_lang} ({target_name}).
Requirements:
- Keep JSON structure exactly as-is
- Preserve all *emphasis* markers and --- dividers  
- Maintain literary, emotional tone
- Only translate the text content, not the structure keys

Chapter:
{chapter_json}

Output ONLY the JSON array with translated content:"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4000,
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(GEMINI_URL, json=payload) as resp:
            if resp.status != 200:
                error = await resp.text()
                print(f"Error: {resp.status} - {error}")
                return None
            data = await resp.json()
            try:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                # Extract JSON from response
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                return json.loads(text)
            except Exception as e:
                print(f"Parse error: {e}")
                return None


async def translate_book(lang_code):
    """Translate all chapters"""
    target_name, target_native = LANGUAGES[lang_code]
    print(f"\nTranslating to {target_name} ({target_native})")
    
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        chapters = json.load(f)
    
    translated = []
    for ch in chapters[:3]:  # Test first 3
        print(f"Chapter {ch['num']}...", end=" ")
        result = await translate_chapter(ch, target_name, target_native)
        if result:
            translated.append(result)
            print("OK")
        else:
            print("FAILED")
            break
    
    # Save
    output_file = OUTPUT_DIR / f"chapters_{lang_code}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(translated)} chapters to {output_file}")


async def main():
    # Test with Khmer first
    await translate_book("km")


if __name__ == "__main__":
    asyncio.run(main())