import json
km = json.load(open("data/translations/chapters_km.json"))
print("Ch1 para1:", km[0]["paragraphs"][0][:30])
print("Ch1 para2:", km[0]["paragraphs"][1][:30])

# Count Khmer
kh = 0
for ch in km:
    for p in ch["paragraphs"]:
        if any(ord(c) > 127 for c in p[:20]):
            kh += 1
print(f"Khmer paragraphs: {kh}")