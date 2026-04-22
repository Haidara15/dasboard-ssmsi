// =====================================================
// 1. PALETTE
// =====================================================

const PALETTE_COULEURS = [
    "#1F4E79",
    "#C55A11",
    "#4F81BD",
    "#9BBB59",
    "#8064A2",
    "#4BACC6",
    "#F79646",
    "#92A9CF",
];


// =====================================================
// 2. HELPERS TYPES
// =====================================================

function convertirTypeGraphique(type) {
    switch (type) {
        case "ligne":
            return "line";

        case "colonnes":
        case "colonnes_empilees":
            return "bar";

        case "barres":
        case "barres_empilees":
            return "bar";

        case "aire":
            return "line";

        case "camembert":
            return "pie";

        case "anneau":
            return "doughnut";

        default:
            return "bar";
    }
}

function estGraphiqueCirculaire(type) {
    return ["camembert", "anneau"].includes(type);
}

function estGraphiqueHorizontal(type) {
    return ["barres", "barres_empilees"].includes(type);
}



function estGraphiqueEmpile(data) {
    return data.type_graphique.includes("empile");
}

function estGraphiqueAire(type) {
    return type === "aire";
}

function getCouleur(index) {
    return PALETTE_COULEURS[index % PALETTE_COULEURS.length];
}


// =====================================================
// 3. DATASETS STANDARD
// =====================================================

function construireDatasetsStandard(data) {
    return data.series.map((serie, index) => {
        const couleur = getCouleur(index);

        const typeSerieBrut = data.type_graphique;
        const typeSerie = convertirTypeGraphique(typeSerieBrut);

        const estLigne = typeSerie === "line";
        const estAire = typeSerieBrut === "aire" || estGraphiqueAire(data.type_graphique);

        return {
            label: serie.libelle,
            data: serie.data,
            type: typeSerie,

            borderColor: couleur,
            backgroundColor: estLigne ? couleur : couleur + "CC",

            borderWidth: 2,
            tension: estLigne ? 0.3 : 0,
            fill: estAire,

            // Très important pour les empilés
            stack: estGraphiqueEmpile(data) ? "stack_1" : undefined,
        };
    });
}


// =====================================================
// 4. DATASETS CIRCULAIRES
// =====================================================

function construireDatasetCirculaire(data) {
    if (!data.series || data.series.length === 0) {
        return { labels: [], datasets: [] };
    }

    // Chaque série = une part : on prend la première valeur non-nulle de chaque série
    const labels = data.series.map(s => s.libelle);
    const valeurs = data.series.map(s => {
        const val = (s.data || []).find(v => v !== null && v !== undefined);
        return val ?? null;
    });
    const couleurs = labels.map((_, index) => getCouleur(index));

    return {
        labels: labels,
        datasets: [{
            label: data.titre,
            data: valeurs,
            backgroundColor: couleurs,
            borderColor: "#ffffff",
            borderWidth: 1,
        }]
    };
}


// =====================================================
// 5. DATA PRINCIPALE
// =====================================================

function construireDataChartJS(data) {
    if (estGraphiqueCirculaire(data.type_graphique)) {
        return construireDatasetCirculaire(data);
    }

    return {
        labels: data.labels,
        datasets: construireDatasetsStandard(data),
    };
}


// =====================================================
// 6. OPTIONS CIRCULAIRES
// =====================================================

function construireOptionsCirculaires(data) {
    return {
        responsive: true,
        maintainAspectRatio: false,

        plugins: {
            legend: {
                display: data.legende_visible !== false
            },
            title: {
                display: false
            }
        }
    };
}


// =====================================================
// 7. OPTIONS STANDARD
// =====================================================

function construireOptionsStandard(data) {
    const horizontal = estGraphiqueHorizontal(data.type_graphique);
    const empile = estGraphiqueEmpile(data);

    return {
        responsive: true,
        maintainAspectRatio: false,

        indexAxis: horizontal ? "y" : "x",

        interaction: {
            mode: "index",
            intersect: false
        },

        plugins: {
            legend: {
                display: data.legende_visible !== false
            },
            title: {
                display: false
            }
        },

        scales: {
            x: {
                stacked: empile,
                title: {
                    display: !!data.axe_x,
                    text: data.axe_x
                }
            },

            y: {
                stacked: empile,
                position: "left",
                title: {
                    display: !!data.axe_y,
                    text: data.axe_y
                }
            }
        }
    };
}


// =====================================================
// 8. OPTIONS PRINCIPALES
// =====================================================

function construireOptions(data) {
    if (estGraphiqueCirculaire(data.type_graphique)) {
        return construireOptionsCirculaires(data);
    }

    return construireOptionsStandard(data);
}


// =====================================================
// 9. INSTANCE CHART
// =====================================================

function creerGraphique(ctx, data) {
    const typeGlobal = convertirTypeGraphique(data.type_graphique);

    return new Chart(ctx, {
        type: typeGlobal,
        data: construireDataChartJS(data),
        options: construireOptions(data)
    });
}


// =====================================================
// 10. FONCTION PRINCIPALE
// =====================================================

async function chargerGraphique(codeGraphique) {
    try {
        const response = await fetch(`/api/graphiques/${codeGraphique}/`);

        if (!response.ok) {
            throw new Error(`Erreur API graphique (${response.status})`);
        }

        const data = await response.json();

        console.log("Graphique reçu :", data); // utile pour debug

        const canvas = document.getElementById(`graphique-${codeGraphique}`);
        if (!canvas) return;

        const ctx = canvas.getContext("2d");

        creerGraphique(ctx, data);

    } catch (error) {
        console.error(`Erreur chargement graphique "${codeGraphique}" :`, error);
    }
}