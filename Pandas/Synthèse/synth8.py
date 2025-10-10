"""
Synthèse 8: Agrégation multiple
"""

import pandas as pd

# Création du DataFrame
df = pd.DataFrame({
    "Ville": ["Paris", "Paris", "Lyon", "Lyon", "Marseille"],
    "Ventes": [100, 150, 200, 250, 300],
    "Employés": [10, 12, 8, 9, 11]
})

print("DataFrame:")
print(df)
print()

# 1. Calculer la moyenne et le total des ventes par ville
ventes_par_ville = df.groupby('Ville')['Ventes'].agg(['mean', 'sum'])
print("1. Moyenne et total des ventes par ville:")
print(ventes_par_ville)
print()

# 2. Ajouter une colonne productivité moyenne par employé
df['Productivité'] = df['Ventes'] / df['Employés']
print("2. DataFrame avec colonne 'Productivité':")
print(df)