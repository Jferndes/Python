"""
Synthèse 5: Statistiques descriptives
"""

import pandas as pd

# Création du DataFrame
data = {
    "Nom": ["Alice", "Bob", "Charlie", "Diane", "Eve"],
    "Age": [25, 30, 35, 40, 28],
    "Ville": ["Paris", "Lyon", "Paris", "Toulouse", "Lyon"]
}

df = pd.DataFrame(data)

print("DataFrame:")
print(df)
print()

# 1. Calculer moyenne, médiane, min et max d'une colonne numérique
print("1. Statistiques sur la colonne 'Age':")
print(f"Moyenne: {df['Age'].mean()}")
print(f"Médiane: {df['Age'].median()}")
print(f"Minimum: {df['Age'].min()}")
print(f"Maximum: {df['Age'].max()}")
print()

# 2. Utiliser df.describe() pour un résumé global
print("2. Résumé global avec describe():")
print(df.describe())
print()

# 3. Calculer la moyenne d'âge par ville (groupby)
print("3. Moyenne d'âge par ville:")
moyenne_par_ville = df.groupby('Ville')['Age'].mean()
print(moyenne_par_ville)