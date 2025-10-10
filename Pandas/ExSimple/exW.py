"""
Exercice W: Grouper les données scolaires par code d'école
"""

import pandas as pd

# Données scolaires
data = {
    'school': ['S1', 'S2', 'S3', 'S1', 'S2', 'S4'],
    'class': ['s001', 's002', 's003', 's001', 's002', 's004'],
    'name': ['Alberto Franco', 'Gino Mcneill', 'Ryan Parkes', 'Eesha Hinton', 'Gino Mcneill', 'David Parkes'],
    'date_of_birth': ['15/05/2002', '17/05/2002', '16/02/1999', '25/09/1998', '11/05/2002', '15/09/1997'],
    'age': [12, 12, 13, 13, 14, 12],
    'height': [173, 192, 186, 167, 151, 159],
    'weight': [35, 32, 33, 30, 31, 32],
    'address': ['street1', 'street2', 'street3', 'street1', 'street2', 'street4']
}

df = pd.DataFrame(data)

print("DataFrame original:")
print(df)
print()

# W.1 - Diviser en groupes par code d'école
print("W.1 - Groupement par code d'école:")
grouped = df.groupby('school')
print(f"Type de l'objet GroupBy: {type(grouped)}")
print()

print("Groupes créés:")
for name, group in grouped:
    print(f"\nÉcole {name}:")
    print(group)
print()

# W.2 - Statistiques d'âge par école
print("W.2 - Statistiques d'âge par école (mean, min, max):")
age_stats = df.groupby('school')['age'].agg(['mean', 'min', 'max'])
print(age_stats)