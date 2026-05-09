const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/translations/chapters_de.json', 'utf8'));
const counts = {};
data.forEach(ch => {
    counts[ch.num] = (counts[ch.num] || 0) + 1;
});
const duplicates = Object.keys(counts).filter(num => counts[num] > 1);
console.log('Duplicates:', duplicates);
console.log('Total length:', data.length);
