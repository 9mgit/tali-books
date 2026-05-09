import json
d = []
try:
    d = json.load(open("data/translations/chapters_km.json"))
except:
    pass
print(f"Chapters: {len(d)}")