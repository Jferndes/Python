"""
Exercice G: Traduire un dictionnaire Python en DataFrame Pandas
"""

import pandas as pd

# Dictionnaire avec les données
data = {
    'X': [78, 85, 96, 80, 86],
    'Y': [84, 94, 89, 83, 86],
    'Z': [86, 97, 96, 72, 83]
}

print("Dictionnaire original:")
print(data)
print()

# Conversion en DataFrame
df = pd.DataFrame(data)

print("DataFrame créé:")
print(df)