const letterTranslations = {
    A: ['À', 'Á', 'Â', 'Ã', 'Ä'],
    C: ['Ç'],
    E: ['È', 'É', 'Ê', 'Ë'],
    I: ['Ì', 'Í', 'Î', 'Ï'],
    N: ['Ñ'],
    O: ['Ò', 'Ó', 'Ô', 'Õ', 'Ö'],
    S: ['Š'],
    U: ['Ú', 'Û', 'Ü', 'Ù'],
    Y: ['Ý', 'Ÿ'],
    Z: ['Ž'],
    a: ['à', 'á', 'â', 'ã', 'ä'],
    c: ['ç'],
    e: ['è', 'é', 'ê', 'ë'],
    i: ['ì', 'í', 'î', 'ï'],
    n: ['ñ'],
    o: ['ò', 'ó', 'ô', 'õ', 'ö'],
    s: ['š'],
    u: ['ú', 'û', 'ü', 'ù'],
    y: ['ý', 'ÿ'],
    z: ['ž'],
};

function getSuggestedForInput(str) {
    const letter = str.slice(-1);
    if (letterTranslations[letter] !== undefined) {
        return letterTranslations[letter];
    }

    return null;
}

function applySuggested(str, choice) {
    let newStr = str.slice(0, -1);
    return newStr + choice;
}
