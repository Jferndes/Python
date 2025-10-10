"""
Synthèse 2: Lecture et écriture de données
"""

import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv("../../Data/ventes.csv")

# 1. Afficher les 5 premières lignes
print("1. Les 5 premières lignes:")
print(df.head(5))
print()

# 2. Sélectionner les colonnes ["Produit", "Quantité", "Prix"]
df_selection = df[["Produit", "Quantité", "Prix"]]
print("2. Colonnes sélectionnées:")
print(df_selection.head())
print()

# 3. Calculer une colonne Total = Quantité * Prix
df['Total'] = df['Quantité'] * df['Prix']
print("3. DataFrame avec colonne 'Total':")
print(df.head())
print()

# 4. Sauvegarder le résultat
df.to_csv("../../Data/ventes_total.csv", index=False)
print("4. Fichier sauvegardé: ventes_total.csv")