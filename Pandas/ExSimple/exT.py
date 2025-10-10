"""
Exercice T: Filtrer les données pour 1986, région 'Western Pacific', pays 'Viet Nam'
"""

import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv('../../Data/world_alcohol.csv')

print("Dataset original:")
print(f"Nombre de lignes: {df.shape[0]}")
print()

# Filtrer avec plusieurs conditions (AND)
df_filtered = df[(df['Year'] == 1986) & 
                  (df['WHO region'] == 'Western Pacific') & 
                  (df['Country'] == 'Viet Nam')]

print("Données pour 1986, Western Pacific, Viet Nam:")
print(df_filtered)