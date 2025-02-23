function createCardElement(value) {
    const card = document.createElement('div');

    if (value == null) {
        card.classList.add('facedown-card');
    } else {
        card.classList.add('faceup-card');
        card.textContent = value;
    }

    card.classList.add('card');

    card.addEventListener('click', function () {
        card.classList.toggle('selected');
    });

    return card;
}

export function renderCards(containerId, numCards, facedown) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    for (let i = 0; i < numCards; i++) {
        const card = createCardElement(facedown ? null : `🃏`);
        container.appendChild(card);
    }
}