"""
Exercice Q: Rechercher et supprimer les valeurs manquantes de world_alcohol.csv
"""

import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv('../../Data/world_alcohol.csv')

print("Dataset original:")
print(f"Nombre de lignes: {df.shape[0]}")
print()

print("Valeurs manquantes par colonne:")
print(df.isnull().sum())
print()

# Supprimer les lignes avec valeurs manquantes
df_clean = df.dropna()

print("Dataset après suppression des valeurs manquantes:")
print(f"Nombre de lignes: {df_clean.shape[0]}")
print()

print("Vérification - Valeurs manquantes par colonne:")
print(df_clean.isnull().sum())