import json

# Check current km file
km = json.load(open("/home/tali/tali-book/data/translations/chapters_km.json"))

# Get first paragraph
para1 = km[0]["paragraphs"][0]
print(f"Para1: {repr(para1[:50])}")

# Count translated
translated = 0
for ch in km:
    for p in ch["paragraphs"]:
        if any(ord(c) > 127 for c in p[:20]):
            translated += 1
print(f"Translated: {translated}/{len(km)*len(km[0]['paragraphs'])}")