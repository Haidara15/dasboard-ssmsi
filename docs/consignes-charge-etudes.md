# Consignes Charge d'etudes - Fichier de mise a jour

## Votre mission
Mettre a jour les valeurs des graphiques sans modifier la structure des codes.

## Format de fichier obligatoire
Colonnes exactes a conserver dans cet ordre:
1. graphique_code
2. thematique_code
3. type_graphique
4. serie_code
5. code_x
6. valeur

## Ce que vous pouvez modifier
- valeur
- ajout de nouvelles lignes (nouvelle periode ou nouvelle categorie deja prevue)

## Ce que vous ne devez pas modifier
- graphique_code
- thematique_code
- type_graphique
- serie_code
- code_x existants

## Regles de remplissage
1. Une ligne = un point de donnee.
2. valeur doit etre numerique.
3. Pas de cellule vide sur les 6 colonnes.
4. Pas d'espaces inutiles dans les codes.
5. Respect strict de l'orthographe des codes.

## Exemple valide
| graphique_code | thematique_code | type_graphique | serie_code | code_x | valeur |
|---|---|---|---|---|---:|
| violences-homicides | violences | colonnes | nombre | 2023 | 884 |
| violences-homicides | violences | colonnes | nombre | 2024 | 901 |

## Checklist avant envoi
1. Le fichier s'ouvre correctement.
2. Les 6 colonnes sont presentes.
3. Aucune cellule vide sur ces colonnes.
4. Les valeurs sont numeriques.
5. Les codes sont inchanges.

## Nommage conseille du fichier
mise_a_jour_violences_AAAA-MM.xlsx

Exemple:
mise_a_jour_violences_2026-04.xlsx
