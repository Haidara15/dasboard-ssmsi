import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "import"

# En-têtes
ws.append([
    "graphique_code",
    "thematique_code",
    "type_graphique",
    "serie_code",
    "code_x",
    "valeur"
])

# Exemple de données pour un camembert
ws.append(["camembert-test", "violences", "camembert", "repartition", "femmes", 88])
ws.append(["camembert-test", "violences", "camembert", "repartition", "hommes", 11])
ws.append(["camembert-test", "violences", "camembert", "repartition", "autres", 1])

wb.save("fichier_type_camembert.xlsx")
print("fichier_type_camembert.xlsx généré")
