import json
import os

def fix_word_counts():
    source_path = r'D:\DATASTORE\PROJECTS\BOOK\data\chapters.json'
    zh_combined_path = r'D:\DATASTORE\PROJECTS\BOOK\langs\zh\zh_combined.json'
    
    with open(source_path, 'r', encoding='utf-8') as f:
        source_chapters = json.load(f)
        
    with open(zh_combined_path, 'r', encoding='utf-8') as f:
        zh_chapters = json.load(f)
        
    # Create a map of num -> word_count from source
    word_count_map = {ch['num']: ch['word_count'] for ch in source_chapters}
    
    fixed_count = 0
    for ch in zh_chapters:
        num = ch.get('num')
        if num in word_count_map and 'word_count' not in ch:
            ch['word_count'] = word_count_map[num]
            fixed_count += 1
            
    with open(zh_combined_path, 'w', encoding='utf-8') as f:
        json.dump(zh_chapters, f, ensure_ascii=False, indent=2)
        
    print(f"Fixed {fixed_count} chapters in {zh_combined_path}")

if __name__ == "__main__":
    fix_word_counts()
