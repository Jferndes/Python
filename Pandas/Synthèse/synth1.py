"""
Synthèse 1: Création d'un DataFrame simple
"""

import pandas as pd

# Création du DataFrame
data = {
    "Nom": ["Alice", "Bob", "Charlie", "Diane"],
    "Age": [25, 30, 35, 40],
    "Ville": ["Paris", "Lyon", "Marseille", "Toulouse"]
}

df = pd.DataFrame(data)

# 1. Afficher les 2 premières lignes
print("1. Les 2 premières lignes:")
print(df.head(2))
print()

# 2. Afficher les noms des colonnes et les types
print("2. Noms des colonnes:")
print(df.columns.tolist())
print()

print("Types des colonnes:")
print(df.dtypes)
print()

# 3. Changer la colonne "Ville" en index
df_indexed = df.set_index('Ville')

print("3. DataFrame avec 'Ville' comme index:")
print(df_indexed)