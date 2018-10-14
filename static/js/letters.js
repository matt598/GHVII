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

class LetterSuggestor {
    constructor(inputSelector) {
        this.helper = document.getElementById('input-helper');
        this.names = Array.from(document.querySelectorAll(inputSelector));
        this.names.forEach(name => {
            name.addEventListener('keyup', this.onKeyUp.bind(this));
        });
        Array.from(document.querySelectorAll('input,textarea')).forEach(input => {
            input.addEventListener('focus', this.onFocus.bind(this));
        });
    }

    onKeyUp(ev) {
        const suggested = getSuggestedForInput(ev.target.value);
        const container = this.helper.querySelector('div');

        if (!suggested) {
            container.innerHTML = 'No suggestions';
            return;
        }

        container.innerHTML = '';
        suggested.map(suggestion => {
            const btn = document.createElement('a');
            btn.href = '#';
            btn.innerHTML = suggestion;
            btn.classList.add('btn', 'btn-sm', 'btn-secondary', 'mr-1');
            btn.addEventListener('click', () => {
                ev.target.value = applySuggested(ev.target.value, suggestion);
                this.onKeyUp(ev);
                ev.target.focus();
            });
            return btn;
        }).forEach(btn => {
            container.appendChild(btn);
        });
    }

    onFocus(ev) {
        let found = false;

        this.names.forEach(name => {
            if (name.id == ev.target.id) {
                found = true;
            }
        });

        this.helper.style.display = (found) ? 'block': 'none';
    }
}
