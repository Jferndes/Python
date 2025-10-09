"""
Exercice B: Convertir une Series Pandas en liste Python et afficher son type
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("CONVERSION D'UNE SERIES PANDAS EN LISTE PYTHON")
print("=" * 60)
print()

# Création d'une Series Pandas
print("1. Création de la Series Pandas originale")
print("-" * 60)
serie_pandas = pd.Series([10, 20, 30, 40, 50, 60, 70])
print(serie_pandas)
print(f"Type de l'objet: {type(serie_pandas)}")
print()

# Conversion en liste Python - Méthode 1: .tolist()
print("2. Conversion avec la méthode .tolist()")
print("-" * 60)
liste_python1 = serie_pandas.tolist()
print(f"Liste convertie: {liste_python1}")
print(f"Type de l'objet: {type(liste_python1)}")
print()

# Conversion en liste Python - Méthode 2: list()
print("3. Conversion avec la fonction list()")
print("-" * 60)
liste_python2 = list(serie_pandas)
print(f"Liste convertie: {liste_python2}")
print(f"Type de l'objet: {type(liste_python2)}")
print()

# Exemple avec des données de type texte
print("4. Conversion d'une Series de chaînes")
print("-" * 60)
serie_noms = pd.Series(['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'])
print(f"Series originale:\n{serie_noms}")
print()
liste_noms = serie_noms.tolist()
print(f"Liste convertie: {liste_noms}")
print(f"Type de l'objet: {type(liste_noms)}")
print()

# Exemple avec des données mixtes
print("5. Conversion d'une Series avec valeurs manquantes")
print("-" * 60)
serie_avec_nan = pd.Series([10, 20, np.nan, 40, None, 60])
print(f"Series originale:\n{serie_avec_nan}")
print()
liste_avec_nan = serie_avec_nan.tolist()
print(f"Liste convertie: {liste_avec_nan}")
print(f"Type de l'objet: {type(liste_avec_nan)}")
print(f"Type du 3ème élément (NaN): {type(liste_avec_nan[2])}")
print()

# Vérification des types des éléments
print("6. Vérification des types des éléments de la liste")
print("-" * 60)
for i, element in enumerate(liste_python1):
    print(f"Element {i}: {element} - Type: {type(element)}")
print()

# Comparaison Series vs Liste
print("7. Différences entre Series et Liste")
print("-" * 60)
print(f"Series peut faire des opérations vectorielles: {(serie_pandas * 2).tolist()}")
print(f"Liste nécessite une boucle ou list comprehension: {[x * 2 for x in liste_python1]}")
print()

# Conversion de l'index en liste
print("8. Conversion de l'index en liste")
print("-" * 60)
serie_avec_index = pd.Series([100, 200, 300], index=['a', 'b', 'c'])
print(f"Series avec index personnalisé:\n{serie_avec_index}")
print()
valeurs_liste = serie_avec_index.tolist()
index_liste = serie_avec_index.index.tolist()
print(f"Valeurs en liste: {valeurs_liste}")
print(f"Index en liste: {index_liste}")
print(f"Type des valeurs: {type(valeurs_liste)}")
print(f"Type de l'index: {type(index_liste)}")