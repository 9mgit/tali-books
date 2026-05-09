import json
km = json.load(open("data/translations/chapters_km.json"))
eng = 0
for ch in km:
    for p in ch["paragraphs"]:
        if not any(ord(c) > 127 for c in p[:20]):
            eng += 1
print(f"English paragraphs: {eng}")