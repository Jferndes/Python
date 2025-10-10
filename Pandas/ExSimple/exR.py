"""
Exercice R: Supprimer les doublons de la colonne 'WHO Region' de world_alcohol.csv
"""

import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv('../../Data/world_alcohol.csv')

print("Dataset original:")
print(f"Nombre de lignes: {df.shape[0]}")
print()

print("Régions WHO uniques avant suppression des doublons:")
print(df['WHO region'].unique())
print(f"Nombre de régions uniques: {df['WHO region'].nunique()}")
print()

# Supprimer les doublons basés sur la colonne 'WHO region'
df_unique = df.drop_duplicates(subset=['WHO region'])

print("Dataset après suppression des doublons:")
print(f"Nombre de lignes: {df_unique.shape[0]}")
print()

print("Aperçu du dataset sans doublons:")
print(df_unique[['Country', 'WHO region']].head(10))