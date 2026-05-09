#!/usr/bin/env python3
import json
with open("data/translations/chapters_es.json") as f:
    data = json.load(f)

if isinstance(data, dict):
    print("Keys:", list(data.keys()))
    if "cover" in data:
        cov = data["cover"]
        print(f"Cover keys: {list(cov.keys())}")
        for k, v in cov.items():
            print(f"  {k}: {v}")