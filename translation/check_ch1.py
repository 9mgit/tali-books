import json
km = json.load(open("data/translations/chapters_km.json"))
print("Ch1 title:", km[0]["title"][:40])
print("Ch1 p1:", km[0]["paragraphs"][0][:30])
print("Ch1 p2:", km[0]["paragraphs"][1][:30])