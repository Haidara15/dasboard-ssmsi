document.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll("[data-graphique]");

    elements.forEach(el => {
        const code = el.dataset.graphique;
        chargerGraphique(code);
    });
});