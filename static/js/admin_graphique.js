(function () {
  "use strict";

  const TYPES_SERIE_UNIQUE = ["camembert", "anneau", "valeur_cle"];

  function updateSerieInline() {
    const select = document.getElementById("id_type_graphique");
    if (!select) return;

    const type = select.value;
    const isUnique = TYPES_SERIE_UNIQUE.includes(type);

    // Bouton "Ajouter une série" (lien en bas de l'inline)
    const addLinks = document.querySelectorAll(".serie-graphique-inline .add-row, [data-inline-formset] .add-row");
    // Fallback : chercher par texte si les sélecteurs ne matchent pas
    const allAddLinks = document.querySelectorAll(".add-row a, a.add-row");

    allAddLinks.forEach(function (link) {
      const row = link.closest("tr, .add-row");
      if (row) {
        row.style.display = isUnique ? "none" : "";
      } else {
        link.style.display = isUnique ? "none" : "";
      }
    });

    // En mode unique : compter les lignes existantes et masquer les lignes vides en excès
    if (isUnique) {
      const inlineRows = document.querySelectorAll(
        "#seriegraphique_set-group .dynamic-seriegraphique_set, " +
        "[id$='seriegraphique_set'] .form-row.dynamic-seriegraphique_set"
      );
      let visibleCount = 0;
      inlineRows.forEach(function (row) {
        if (row.style.display === "none") return; // déjà masqué
        visibleCount++;
        if (visibleCount > 1) {
          row.style.display = "none";
        }
      });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const select = document.getElementById("id_type_graphique");
    if (!select) return;

    // Appliquer au chargement
    updateSerieInline();

    // Écouter les changements
    select.addEventListener("change", updateSerieInline);
  });
})();
