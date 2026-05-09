import json
ch = json.load(open("/home/tali/tali-book/data/chapters.json"))
print("Ch1:", len(ch[0]["paragraphs"]))
print("Total:", sum(len(c["paragraphs"]) for c in ch))