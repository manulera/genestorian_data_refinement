// A js script to get the data from https://yeast.nig.ac.jp/yeast/fy/StrainAllItemsList.xhtml
// To get the publication info, you should wait until all requests are made
function savefile(filename, data) {
    var blob = new Blob([data], { type: 'text' });
    if (window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveBlob(blob, filename);
    }
    else {
        var elem = window.document.createElement('a');
        elem.href = window.URL.createObjectURL(blob);
        elem.download = filename;
        document.body.appendChild(elem);
        elem.click();
        document.body.removeChild(elem);
    }
}

const table = document.getElementById('form_list:resouceList')
let rows = table.getElementsByTagName('TR')
const csvContent = [];
for (const tr of rows) {
    // Skip header
    if (tr.getElementsByTagName('TH').length)
        continue

    let lineContent = []
    // Add csv content
    for (const td of tr.getElementsByTagName('TD')) {
        lineContent.push(td.textContent.replaceAll('\n', '').replace(/\s\s+/g, ' ').trim())

    }
    csvContent.push(lineContent.join('\t'))
}

savefile('strains.tsv', csvContent.join('\n'))

