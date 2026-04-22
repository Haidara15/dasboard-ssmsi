# Procedure Admin - Mise a jour des graphiques

## Objectif
Mettre a jour les donnees sans casser la structure des graphiques.

## Perimetre des roles
- Admin: definit la structure, valide la qualite, publie.
- Charge d'etudes: met a jour les valeurs numeriques.

## Etape 1 - Definir la structure de reference (une seule fois)
Dans l'admin, pour chaque thematique:
1. Creer la thematique.
2. Creer chaque graphique avec son type.
3. Creer les series attendues.
4. Fixer les codes stables: thematique_code, graphique_code, serie_code, code_x.

Regle: ces codes ne doivent plus changer apres validation.

## Etape 2 - Construire le gabarit de mise a jour
Utiliser le modele minimal a 6 colonnes:
1. graphique_code
2. thematique_code
3. type_graphique
4. serie_code
5. code_x
6. valeur

## Etape 3 - Envoi au charge d'etudes
Envoyer le gabarit en rappelant 3 regles:
1. Ne pas renommer les codes.
2. Ne pas changer le type_graphique.
3. Renseigner uniquement valeur (et ajouter de nouvelles lignes si necessaire).

## Etape 4 - Controle avant import
Checklist admin:
1. Colonnes obligatoires presentes.
2. Pas de cellule vide sur les colonnes obligatoires.
3. type_graphique valide.
4. valeur numerique.
5. Pas de faute de frappe sur les codes.

## Etape 5 - Import plateforme
1. Ouvrir la page Import.
2. Charger le fichier.
3. Executer l'import.
4. Lire le rapport (crees/mis a jour/ignores).

## Etape 6 - Validation post-import
1. Ouvrir la thematique.
2. Verifier chaque graphique.
3. Verifier ordres et libelles.
4. Corriger les metadonnees editoriales dans l'admin si besoin:
   - thematique: sous_titre, chapeau, texte_methodologique, texte_source.
   - graphique: titre, sous_titre, axes, source, note, legende_visible, ordre.
   - serie: libelle, couleur, ordre, visible.

## Etape 7 - Publication
1. Confirmer actif sur les objets a afficher.
2. Valider le rendu final.
3. Cloturer le cycle de mise a jour.

## Gestion des incidents (rapide)
- Erreur de colonnes: corriger le fichier source puis re-importer.
- Valeurs incorrectes: re-export corrige puis re-import.
- Graphique manquant: verifier graphique_code et thematique_code.
- Duplicat inattendu: verifier combinaison graphique_code + serie_code + code_x.

## Rythme recommande
- Test sur petit echantillon au debut.
- Puis import complet.
- Toujours un controle visuel final avant publication.
