#!/usr/bin/env python3
import json
with open("data/translations/chapters_es.json") as f:
    data = json.load(f)

if isinstance(data, dict) and "chapters" in data:
    ch = data["chapters"]
    print(f"Spanish: {len(ch)} chapters")
    print(f"Chapter 1 title: {ch[0]['title']}")
elif isinstance(data, list):
    print(f"Spanish: {len(data)} chapters")