"""
Exercice E: Convertir un dictionnaire en Series Pandas
"""

import pandas as pd

# Création d'un dictionnaire
dictionnaire = {
    'a': 100,
    'b': 200,
    'c': 300,
    'd': 400,
    'e': 500
}

print("Dictionnaire original:")
print(dictionnaire)
print()

# Conversion en Series
serie = pd.Series(dictionnaire)

print("Series créée depuis le dictionnaire:")
print(serie)
print()

print(f"Type: {type(serie)}")