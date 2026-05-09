import json
import sys

files = [
    "bisaya-01.json",
    "bisaya-02.json", 
    "bisaya-03.json",
    "bisaya-04.json",
    "bisaya-05.json",
    "bisaya-06.json",
    "bisaya-07.json",
    "bisaya-08.json",
    "bisaya-09.json",
    "bisaya-10.json",
    "bisaya-11.json",
    "bisaya-12.json",
    "bisaya-13.json",
    "bisaya-14.json",
    "bisaya-15.json",
]

all_chapters = []

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            if isinstance(data, list):
                all_chapters.extend(data)
            else:
                all_chapters.append(data)
    except Exception as e:
        print(f"Error reading {f}: {e}")

all_chapters.sort(key=lambda x: x.get('num', 0))

print(f"Total chapters: {len(all_chapters)}")

with open('chapters_ceb.json', 'w', encoding='utf-8') as fp:
    json.dump(all_chapters, fp, ensure_ascii=False, indent=2)

print("Written to chapters_ceb.json")
