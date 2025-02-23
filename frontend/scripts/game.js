import { renderCards } from './renderGame.js'

document.addEventListener('DOMContentLoaded', () => {
    renderCards('left-player-cards', 4, true);
    renderCards('right-player-cards', 3, true);
    renderCards('my-cards', 7, false);
});
