"""
Synthèse 7: Fusion de DataFrames
"""

import pandas as pd

# Création des DataFrames
clients = pd.DataFrame({
    "id_client": [1, 2, 3],
    "nom": ["Alice", "Bob", "Charlie"]
})

commandes = pd.DataFrame({
    "id_commande": [100, 101, 102],
    "id_client": [1, 1, 3],
    "montant": [250, 120, 90]
})

print("DataFrame clients:")
print(clients)
print()

print("DataFrame commandes:")
print(commandes)
print()

# 1. Réaliser une jointure entre clients et commandes sur id_client
df_merged = pd.merge(clients, commandes, on='id_client')
print("1. Jointure clients-commandes:")
print(df_merged)
print()

# 2. Calculer le montant total dépensé par chaque client
montant_par_client = df_merged.groupby('nom')['montant'].sum()
print("2. Montant total dépensé par client:")
print(montant_par_client)