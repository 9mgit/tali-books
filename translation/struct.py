import json
ch = json.load(open("data/chapters.json"))
km = json.load(open("data/translations/chapters_km.json"))
print("Chapters:", len(km))
print("Ch1 paras:", len(km[0]["paragraphs"]))
print("Ch2 paras:", len(km[1]["paragraphs"]))
print("Ch3 paras:", len(km[2]["paragraphs"]))