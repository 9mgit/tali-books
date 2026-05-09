const fs = require('fs');
const path = require('path');

const TRANSLATIONS_DIR = 'data/translations';
const baselineFile = path.join(TRANSLATIONS_DIR, 'chapters_en.json');

if (!fs.existsSync(baselineFile)) {
    console.error('Baseline file chapters_en.json not found.');
    process.exit(1);
}

const baseline = JSON.parse(fs.readFileSync(baselineFile, 'utf8'));
const baselineStats = baseline.map(ch => ({
    num: ch.num,
    words: ch.word_count || 0,
    paras: ch.paragraphs ? ch.paragraphs.length : 0
}));

const files = fs.readdirSync(TRANSLATIONS_DIR).filter(f => f.startsWith('chapters_') && f.endsWith('.json') && f !== 'chapters_en.json');

const results = [];

files.forEach(file => {
    const iso = file.replace('chapters_', '').replace('.json', '');
    try {
        const data = JSON.parse(fs.readFileSync(path.join(TRANSLATIONS_DIR, file), 'utf8'));
        let totalWords = 0;
        let totalParas = 0;
        let missingChapters = [];
        let anomalies = [];

        baselineStats.forEach(base => {
            const ch = data.find(c => c.num === base.num);
            if (!ch) {
                missingChapters.push(base.num);
            } else {
                totalWords += (ch.word_count || 0);
                totalParas += (ch.paragraphs ? ch.paragraphs.length : 0);
                
                // Check for suspiciously short chapters (e.g., < 50% of baseline words)
                if (ch.word_count && base.words && ch.word_count < base.words * 0.5) {
                    anomalies.push(`Ch ${base.num}: ${ch.word_count}/${base.words} words`);
                }
            }
        });

        const baseTotalWords = baselineStats.reduce((sum, b) => sum + b.words, 0);
        const baseTotalParas = baselineStats.reduce((sum, b) => sum + b.paras, 0);

        results.push({
            iso,
            totalWords,
            baseWords: baseTotalWords,
            ratio: (totalWords / baseTotalWords).toFixed(2),
            totalParas,
            baseParas: baseTotalParas,
            paraRatio: (totalParas / baseTotalParas).toFixed(2),
            missingCount: missingChapters.length,
            anomalies: anomalies.length
        });
    } catch (e) {
        console.error(`Error processing ${file}: ${e}`);
    }
});

console.table(results);
