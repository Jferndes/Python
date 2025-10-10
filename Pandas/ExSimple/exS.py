"""
Exercice S: Découvrir les détails de la consommation d'alcool pour 1987 ou 1989
"""

import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv('../../Data/world_alcohol.csv')

print("Dataset original:")
print(f"Nombre de lignes: {df.shape[0]}")
print()

# Filtrer pour les années 1987 ou 1989
df_filtered = df[(df['Year'] == 1987) | (df['Year'] == 1989)]

print("Données pour l'année 1987 ou 1989:")
print(f"Nombre de lignes: {df_filtered.shape[0]}")
print()

print("Aperçu des données filtrées:")
print(df_filtered.head(10))