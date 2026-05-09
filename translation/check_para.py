import json
km = json.load(open("data/translations/chapters_km.json"))
print("KM Ch1 paragraphs:")
for i, p in enumerate(km[0]["paragraphs"][:5]):
    print(f"  {i+1}:", p[:50])
print("\nKM Ch1 last para:", km[0]["paragraphs"][-1][:50])