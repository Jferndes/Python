"""
Exercice F: Convertir un array NumPy en Series Pandas
"""

import pandas as pd
import numpy as np

# Création d'un array NumPy
array_numpy = np.array([10, 20, 30, 40, 50, 60])

print("Array NumPy original:")
print(array_numpy)
print(f"Type: {type(array_numpy)}")
print()

# Conversion en Series
serie = pd.Series(array_numpy)

print("Series créée depuis l'array NumPy:")
print(serie)
print(f"Type: {type(serie)}")