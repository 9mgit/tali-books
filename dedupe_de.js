const fs = require('fs');
const filePath = 'data/translations/chapters_de.json';
const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

const unique = {};
data.forEach(ch => {
    unique[ch.num] = ch;
});

const result = Object.values(unique).sort((a, b) => a.num - b.num);
fs.writeFileSync(filePath, JSON.stringify(result, null, 2), 'utf8');
console.log(`Deduplicated. Now ${result.length} chapters.`);
