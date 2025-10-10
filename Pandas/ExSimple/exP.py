"""
Exercice P: Afficher les dimensions et les noms des colonnes du fichier world_alcohol.csv
"""

import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv('../../Data/world_alcohol.csv')

print("Dimensions du dataset (lignes, colonnes):")
print(df.shape)
print()

print("Noms des colonnes:")
print(df.columns.tolist())
print()

print("Aperçu des données head:")
print(df.head())

print("Aperçu des données tail:")
print(df.tail())