const fs = require('fs');
const path = require('path');

const LANGS_DIR = 'langs';

function validateJsonFiles() {
    const dirs = fs.readdirSync(LANGS_DIR);
    const errors = [];

    dirs.forEach(dir => {
        const dirPath = path.join(LANGS_DIR, dir);
        if (!fs.statSync(dirPath).isDirectory()) return;

        const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.json'));
        files.forEach(file => {
            const filePath = path.join(dirPath, file);
            try {
                const content = fs.readFileSync(filePath, 'utf8').replace(/^\uFEFF/, '');
                JSON.parse(content);
            } catch (e) {
                errors.push({ file: filePath, error: e.message });
            }
        });
    });

    if (errors.length === 0) {
        console.log('All JSON files are valid.');
    } else {
        console.log('Found errors in the following files:');
        errors.forEach(err => console.log(`${err.file}: ${err.error}`));
    }
}

validateJsonFiles();
