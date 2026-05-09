import json
import os
import glob

def combine_json_files():
    path = r'D:\DATASTORE\PROJECTS\BOOK\langs\hi'
    files = glob.glob(os.path.join(path, 'hindi-*.json'))
    # Sort files numerically: hindi-01, hindi-02...
    files.sort(key=lambda x: int(x.split('-')[-1].split('.')[0]))
    
    combined_data = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                combined_data.extend(data)
            else:
                combined_data.append(data)
                
    output_path = os.path.join(path, 'hindi_combined.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    print(f"Combined {len(files)} files into {output_path}")

if __name__ == "__main__":
    combine_json_files()
