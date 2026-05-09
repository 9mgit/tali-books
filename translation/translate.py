#!/usr/bin/env python3
"""
Translation script using LLM Council pattern.
Multiple LLMs translate, then review each other's work, chairman produces final translation.

Usage:
    python translate.py --lang es        # Translate to Spanish
    python translate.py                 # Translate to all languages
"""

import os
import sys
import json
import asyncio
import aiohttp
import argparse
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

LANGUAGES = {
    "es": ("Spanish", "Español"),
    "fr": ("French", "Français"),
    "de": ("German", "Deutsch"),
    "zh-CN": ("Chinese Simplified", "简体中文"),
    "ja": ("Japanese", "日本語"),
    "pt": ("Portuguese", "Português"),
    "ar": ("Arabic", "العربية"),
    "hi": ("Hindi", "हिन्दी"),
    "ru": ("Russian", "Русский"),
    "ko": ("Korean", "한국어"),
    "it": ("Italian", "Italiano"),
    "tl": ("Tagalog", "Tagalog"),
    "ceb": ("Bisaya", "Bisaya"),
    "id": ("Bahasa Indonesia", "Bahasa Indonesia"),
    "vi": ("Vietnamese", "Tiếng Việt"),
    "th": ("Thai", "ไทย"),
    "km": ("Khmer", "ខ្មែរ"),
}

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
SOURCE_FILE = "data/chapters.json"
OUTPUT_DIR = Path("data/translations")

COUNCIL_MODELS = [
    "mistralai/mistral-nemo",
]

# Fallback free models
FREE_MODELS = [
    "cohere/command-r-08-2024",
    "meta-llama/llama-3.1-8b-instruct",
]
    "meta-llama/llama-3.1-8b-instruct",
    "anthropic/claude-3-haiku",
]

TRANSLATION_SYSTEM_PROMPT = """You are a literary translator. Translate the following chapter from English to {target_lang} ({target_name}).

Requirements:
- Preserve the literary, emotional tone of the original
- Keep all *emphasis* markers (asterisks for italic text)
- Keep the --- dividers exactly as they are
- Maintain the question format with *italics*
- Keep the JSON structure identical - only translate text values
- The tone should be: serious, literary, thought-provoking

Translate now:"""

REVIEW_SYSTEM_PROMPT = """You are a literary translation reviewer. Compare the original English text with the translation and evaluate:
1. Accuracy - does it convey the same meaning?
2. Literary quality - is it emotionally compelling?
3. Fluency - does it read naturally in {target_lang}?

Original English:
{original}

Translation:
{translation}

Provide a brief review (2-3 sentences) noting any issues that need correction."""


async def call_openrouter(session, model: str, system_prompt: str, user_prompt: str) -> str:
    """Call a single model via OpenRouter API."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4000,  # Limit to avoid credit issues
    }
    async with session.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    ) as resp:
        if resp.status != 200:
            error = await resp.text()
            raise Exception(f"API error: {resp.status} - {error}")
        data = await resp.json()
        return data["choices"][0]["message"]["content"]


async def translate_chapter_council(session, chapter: dict, lang_code: str, target_lang: str, target_name: str) -> dict:
    """Translate a single chapter using council pattern."""
    chapter_json = json.dumps(chapter, ensure_ascii=False, indent=2)
    
    # Stage 1: Each model translates independently
    translations = []
    for model in COUNCIL_MODELS:
        try:
            translation = await call_openrouter(
                session,
                model,
                TRANSLATION_SYSTEM_PROMPT.format(target_lang=target_lang, target_name=target_name),
                chapter_json
            )
            translations.append((model, translation))
            print(f"  [{model[:20]} translated chapter {chapter['num']}]")
        except Exception as e:
            print(f"  Error with {model}: {e}")
            continue
    
    if not translations:
        raise Exception("No models succeeded")
    
    # Stage 2: Review (simplified - take best translation)
    # In full council, each reviews others. Here we take first valid JSON.
    for model, translation in translations:
        try:
            # Try to parse as JSON
            result = json.loads(translation)
            if "paragraphs" in result:
                print(f"  [Council chose translation from {model[:20]}]")
                return result
        except:
            continue
    
    # Fallback: return first translation stripped of markdown
    import re
    for model, translation in translations:
        cleaned = re.sub(r'^```json\n', '', translation.strip())
        cleaned = re.sub(r'\n```$', '', cleaned)
        try:
            return json.loads(cleaned)
        except:
            continue
    
    raise Exception("Could not parse any translation as JSON")


async def translate_book(target_lang_code: str):
    """Translate all chapters to target language."""
    target_name, target_native = LANGUAGES[target_lang_code]
    
    print(f"\n{'='*60}")
    print(f"Translating to {target_name} ({target_native})")
    print(f"{'='*60}")
    
    # Load source
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        chapters = json.load(f)
    
    translated_chapters = []
    
    # Check for existing work and resume
    output_file = OUTPUT_DIR / f"chapters_{target_lang_code}.json"
    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            translated_chapters = json.load(f)
        print(f"Resuming from {len(translated_chapters)} existing chapters")
        start_idx = len(translated_chapters)
    else:
        start_idx = 0
    
    async with aiohttp.ClientSession() as session:
        for i, ch in enumerate(chapters):
            if i < start_idx:
                continue  # Skip already done
            print(f"\nChapter {ch['num']}: {ch['title']}")
            print(f"  Calling model...")
            try:
                translated = await translate_chapter_council(
                    session, ch, target_lang_code, target_name, target_native
                )
                print(f"  Done! Saving chapter {ch['num']}...")
                translated_chapters.append(translated)
            except Exception as e:
                print(f"  Skipping chapter {ch['num']}: {e}")
                continue
            
            # Save after each chapter (avoid losing progress)
            output_file = OUTPUT_DIR / f"chapters_{target_lang_code}.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(translated_chapters, f, ensure_ascii=False, indent=2)
            print(f"  Saved! ({len(translated_chapters)} chapters)")
    
    print(f"\n✓ Saved to {output_file}")
    return output_file


async def main(args):
    parser = argparse.ArgumentParser(description="Translate book to multiple languages")
    parser.add_argument("--lang", "-l", help="Specific language code (e.g., es, fr)")
    parsed = parser.parse_args(args)
    
    if not OPENROUTER_API_KEY:
        print("ERROR: Set OPENROUTER_API_KEY environment variable")
        print("Get one at https://openrouter.ai/")
        return
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Languages to translate
    if parsed.lang:
        if parsed.lang not in LANGUAGES:
            print(f"Unknown language: {parsed.lang}")
            print(f"Available: {', '.join(LANGUAGES.keys())}")
            return
        targets = [parsed.lang]
    else:
        targets = list(LANGUAGES.keys())
    
    print(f"Translating to {len(targets)} language(s)")
    
    for lang_code in targets:
        print(f"\n{'='*50}")
        print(f"Starting: {LANGUAGES[lang_code][0]}")
        print(f"{'='*50}")
        try:
            await translate_book(lang_code)
        except Exception as e:
            print(f"Error for {lang_code}: {e}")
        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))