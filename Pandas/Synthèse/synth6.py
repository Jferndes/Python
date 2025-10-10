"""
Synthèse 6: Tri et regroupement
"""

import pandas as pd

# Lecture du fichier ventes
df = pd.read_csv("../../Data/ventes.csv")

print("DataFrame ventes:")
print(df.head())
print()

# 1. Trier un DataFrame par une colonne
df_trie_asc = df.sort_values('Prix', ascending=True)
print("1a. Trié par Prix (croissant):")
print(df_trie_asc.head())
print()

df_trie_desc = df.sort_values('Quantité', ascending=False)
print("1b. Trié par Quantité (décroissant):")
print(df_trie_desc.head())
print()

# 2. Regrouper les ventes par produit et calculer la somme totale vendue
ventes_par_produit = df.groupby('Produit')['Quantité'].sum()
print("2. Somme des Quantités vendues par produit:")
print(ventes_par_produit)
print()

# 3. Trouver le produit le plus vendu
produit_max = ventes_par_produit.idxmax()
quantite_max = ventes_par_produit.max()
print(f"3. Produit le plus vendu: {produit_max} avec {quantite_max} unités")