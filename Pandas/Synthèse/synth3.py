"""
Synthèse 3: Sélection et filtrage
"""

import pandas as pd

# Création du DataFrame
data = {
    "Nom": ["Alice", "Bob", "Charlie", "Diane"],
    "Age": [25, 30, 35, 40],
    "Ville": ["Paris", "Lyon", "Marseille", "Toulouse"]
}

df = pd.DataFrame(data)

print("DataFrame original:")
print(df)
print()

# 1. Sélectionner uniquement les clients dont l'âge est > 30
df_age_filtre = df[df['Age'] > 30]
print("1. Clients avec âge > 30:")
print(df_age_filtre)
print()

# 2. Sélectionner les colonnes "Nom" et "Ville"
df_selection = df[['Nom', 'Ville']]
print("2. Colonnes 'Nom' et 'Ville':")
print(df_selection)
print()

# 3. Trier les résultats par âge décroissant
df_trie = df.sort_values('Age', ascending=False)
print("3. DataFrame trié par âge décroissant:")
print(df_trie)