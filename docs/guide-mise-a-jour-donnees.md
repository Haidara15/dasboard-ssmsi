# Guide de mise à jour des données graphiques

Ce guide s’adresse à toute personne amenée à mettre à jour les données des graphiques. Il est basé sur l’expérience des cycles précédents : suivez-le à la lettre pour éviter les galères.

---

## 1. Structure attendue pour chaque type de graphique

### A. Camembert (Pie chart)

**Colonnes obligatoires :**
- graphique_code
- thematique_code
- type_graphique (doit être « camembert »)
- serie_code
- code_x (ex : catégorie)
- valeur (numérique)

**Exemple :**
| graphique_code | thematique_code | type_graphique | serie_code | code_x      | valeur |
|----------------|----------------|---------------|------------|-------------|--------|
| G1             | T1             | camembert     | S1         | Hommes      | 1200   |
| G1             | T1             | camembert     | S1         | Femmes      | 800    |

**Règles :**
- Tous les champs sont obligatoires.
- `valeur` doit être un nombre.
- Ne pas modifier les codes existants.

---

### B. Histogramme (Bar chart)

**Colonnes obligatoires :**
- graphique_code
- thematique_code
- type_graphique (doit être « histogramme »)
- serie_code
- code_x (ex : année)
- valeur (numérique)

**Exemple :**
| graphique_code | thematique_code | type_graphique | serie_code | code_x | valeur |
|----------------|----------------|---------------|------------|--------|--------|
| G2             | T1             | histogramme   | S2         | 2022   | 1500   |
| G2             | T1             | histogramme   | S2         | 2023   | 1700   |

**Règles :**
- Même logique que pour le camembert.
- `code_x` doit correspondre à la dimension temporelle ou catégorielle attendue.

---

### C. Courbe (Line chart)

**Colonnes obligatoires :**
- graphique_code
- thematique_code
- type_graphique (doit être « courbe »)
- serie_code
- code_x (ex : année)
- valeur (numérique)

**Exemple :**
| graphique_code | thematique_code | type_graphique | serie_code | code_x | valeur |
|----------------|----------------|---------------|------------|--------|--------|
| G3             | T2             | courbe        | S3         | 2022   | 900    |
| G3             | T2             | courbe        | S3         | 2023   | 1100   |

**Règles :**
- Même logique que pour les autres types.

---

## 2. Points de vigilance
- Ne jamais modifier les codes (graphique, thematique, série, code_x) sans validation admin.
- Toujours vérifier que les colonnes sont bien nommées et présentes.
- Pas de cellule vide dans les colonnes obligatoires.
- `valeur` doit être un nombre (pas de texte, pas de « - », pas de « n/a »).
- Si doute, demander à l’admin avant d’importer.

---

## 3. En cas d’erreur à l’import
- L’import bloque si une règle n’est pas respectée : lisez le message d’erreur, corrigez le fichier, puis recommencez.
- Si besoin, faites un test sur 2-3 lignes avant d’importer tout le fichier.

---

Pour toute question : contactez l’admin ou relisez ce guide !
