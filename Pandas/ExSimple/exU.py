"""
Exercice U: Trouver la consommation moyenne de vin par personne supérieure à 2
"""

import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv('../../Data/world_alcohol.csv')

print("Dataset original:")
print(f"Nombre de lignes: {df.shape[0]}")
print()

# Filtrer pour le type de boisson 'Wine' et convertir la colonne en numérique
df_wine = df[df['Beverage Types'] == 'Wine'].copy()

# Convertir la colonne de consommation en numérique (au cas où c'est du texte)
df_wine['Display Value'] = pd.to_numeric(df_wine['Display Value'], errors='coerce')

# Filtrer pour consommation > 2
df_filtered = df_wine[df_wine['Display Value'] > 2]

print("Pays avec consommation moyenne de vin > 2:")
print(f"Nombre de lignes: {df_filtered.shape[0]}")
print()

print("Aperçu des données:")
print(df_filtered[['Country', 'Year', 'Display Value']].head(10))