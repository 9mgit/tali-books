import json
km = json.load(open("data/translations/chapters_km.json"))
print("KM Ch1 title:", km[0]["title"][:60])
print("KM Ch1 para 1:", km[0]["paragraphs"][0][:60])

es = json.load(open("data/translations/chapters_es.json"))
if "chapters" in es:
    es = es["chapters"]
print("ES Ch1 title:", es[0]["title"][:60])