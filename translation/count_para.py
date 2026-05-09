#!/usr/bin/env python3
import json
ch = json.load(open("data/chapters.json"))
print(f"Chapter 2: {len(ch[1]['paragraphs'])} paragraphs")
for i, p in enumerate(ch[1]['paragraphs'], 1):
    print(f"{i}: {len(p.split())} words")