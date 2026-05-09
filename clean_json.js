const fs = require('fs');
const path = require('path');

function cleanJson(filePath) {
    console.log(`Cleaning ${filePath}...`);
    let content = fs.readFileSync(filePath, 'utf8').replace(/^\uFEFF/, '');
    
    // Remove trailing commas in arrays/objects
    content = content.replace(/,\s*([\]}])/g, '$1');
    
    // Replace bad control characters (newlines, tabs) inside strings
    // This is a naive approach, but often works for simple fixes
    content = content.replace(/[\u0000-\u001F]+/g, ' ');

    try {
        JSON.parse(content);
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Successfully cleaned ${filePath}`);
    } catch (e) {
        console.error(`Could not clean ${filePath}: ${e.message}`);
        // Try to force close it if it's truncated
        if (content.trim().slice(-1) !== ']') {
            console.log(`Attempting to force close ${filePath}...`);
            // This is risky but we are desperate
            content += '}]}]'; 
            // try again... (omitted for brevity)
        }
    }
}

cleanJson('D:/DATASTORE/PROJECTS/BOOK/langs/tr/Turkish-03.json');
cleanJson('D:/DATASTORE/PROJECTS/BOOK/langs/de/German-03.json');
