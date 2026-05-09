import json
import os
import glob

LANGUAGES = ['de', 'it', 'ja', 'ko', 'pt', 'tr']
LANGS_DIR = 'langs'
OUT_DIR = 'data/translations'

def combine_lang(iso):
    print(f"Processing {iso}...")
    path = os.path.join(LANGS_DIR, iso, "*.json")
    files = sorted(glob.glob(path))
    
    if not files:
        print(f"No files found for {iso}")
        return

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

    # Sort by chapter number
    all_chapters.sort(key=lambda x: x.get('num', 0))
    
    print(f"Total chapters for {iso}: {len(all_chapters)}")
    
    out_file = os.path.join(OUT_DIR, f"chapters_{iso}.json")
    with open(out_file, 'w', encoding='utf-8') as fp:
        json.dump(all_chapters, fp, ensure_ascii=False, indent=2)
    print(f"Written to {out_file}")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for iso in LANGUAGES:
        combine_lang(iso)
