"""
Synthèse 4: Gestion des valeurs manquantes
"""

import pandas as pd

# Création du DataFrame avec valeurs manquantes
df = pd.DataFrame({
    "Nom": ["Alice", "Bob", "Charlie", "Diane"],
    "Age": [25, None, 35, None],
    "Ville": ["Paris", "Lyon", None, "Toulouse"]
})

print("DataFrame original:")
print(df)
print()

# 1. Supprimer les lignes avec des valeurs manquantes
df_clean = df.dropna()
print("1. DataFrame sans lignes manquantes:")
print(df_clean)
print()

# 2. Remplacer les valeurs manquantes de Age par la moyenne
df_age_moyenne = df.copy()
moyenne_age = df_age_moyenne['Age'].mean()
df_age_moyenne['Age'] = df_age_moyenne['Age'].fillna(moyenne_age)
print(f"2. Age manquant remplacé par la moyenne ({moyenne_age}):")
print(df_age_moyenne)
print()

# 3. Remplacer les villes manquantes par "Inconnue"
df_ville_remplie = df.copy()
df_ville_remplie['Ville'] = df_ville_remplie['Ville'].fillna("Inconnue")
print("3. Ville manquante remplacée par 'Inconnue':")
print(df_ville_remplie)