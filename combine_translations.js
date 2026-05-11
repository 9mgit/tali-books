const fs = require('fs');
const path = require('path');

const LANGS_DIR = 'langs';
const OUT_DIR = 'data/translations/chapters';

const ALL_LANGUAGES = ['am', 'apc', 'apd', 'ar', 'arz', 'bho', 'bn', 'ceb', 'cs', 'da', 'de', 'es', 'fa', 'fi', 'fr', 'gu', 'ha', 'hi', 'id', 'it', 'ja', 'jv', 'km', 'kn', 'ko', 'mai', 'ml', 'mr', 'ms', 'my', 'nl', 'no', 'or', 'pa', 'pl', 'pt', 'ru', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'uz', 'vi', 'wuu', 'yo', 'yue', 'zh'];

const args = process.argv.slice(2);
let LANGUAGES = [];

if (args.length > 0) {
    LANGUAGES = args;
    console.log(`Building only: ${LANGUAGES.join(', ')}`);
} else {
    LANGUAGES = ALL_LANGUAGES;
    console.log(`Building ALL languages (${LANGUAGES.length})`);
}

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
    allChapters = allChapters.filter((c, i, arr) => !i || c.num !== arr[i-1].num);
    console.log(`Total chapters for ${iso}: ${allChapters.length}`);

    if (!fs.existsSync(OUT_DIR)) {
        fs.mkdirSync(OUT_DIR, { recursive: true });
    }

    const outFile = path.join(OUT_DIR, `${iso}.json`);
    fs.writeFileSync(outFile, JSON.stringify(allChapters, null, 2), 'utf8');
    console.log(`Written to ${outFile}`);
}

LANGUAGES.forEach(combineLang);

console.log('\nDone!');