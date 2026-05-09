const fs = require('fs');
const path = require('path');

const LANGUAGES = ['de', 'it', 'ja', 'ko', 'pt', 'tr', 'ru', 'pl', 'nl', 'my', 'km', 'bn', 'sv', 'am', 'ar', 'fa', 'id', 'ceb', 'es', 'fr', 'hi', 'tl', 'vi', 'zh', 'da'];
const LANGS_DIR = 'langs';
const OUT_DIR = 'data/translations';

function combineLang(iso) {
    console.log(`Processing ${iso}...`);
    const dirPath = path.join(LANGS_DIR, iso);
    if (!fs.existsSync(dirPath)) {
        console.error(`Directory not found: ${dirPath}`);
        return;
    }

    const files = fs.readdirSync(dirPath)
        .filter(f => f.endsWith('.json'))
        .sort();

    if (files.length === 0) {
        console.error(`No JSON files found for ${iso}`);
        return;
    }

    let allChapters = [];
    for (const f of files) {
    try {
        const content = fs.readFileSync(path.join(dirPath, f), 'utf8').replace(/^\uFEFF/, '');
        const data = JSON.parse(content);
        if (Array.isArray(data)) {
            allChapters = allChapters.concat(data);
        } else {
            allChapters.push(data);
        }
    } catch (e) {
        console.error(`Error reading ${f}: ${e}`);
    }
    }

    allChapters.sort((a, b) => (a.num || 0) - (b.num || 0));
    console.log(`Total chapters for ${iso}: ${allChapters.length}`);

    if (!fs.existsSync(OUT_DIR)) {
        fs.mkdirSync(OUT_DIR, { recursive: true });
    }

    const outFile = path.join(OUT_DIR, `chapters_${iso}.json`);
    fs.writeFileSync(outFile, JSON.stringify(allChapters, null, 2), 'utf8');
    console.log(`Written to ${outFile}`);
}

LANGUAGES.forEach(combineLang);
