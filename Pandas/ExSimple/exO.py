"""
Exercice O: Ajouter des lignes à un DataFrame existant
"""

import pandas as pd

# DataFrame initial
student_data1 = pd.DataFrame({
    'student_id': ['S1', 'S2', 'S3', 'S4', 'S5'],
    'name': ['Danniella Fenton', 'Ryder Storey', 'Bryce Jensen', 'Ed Bernal', 'Kwame Morin'],
    'marks': [200, 210, 190, 222, 199]
})

print("DataFrame original:")
print(student_data1)
print()

# Nouvelle ligne à ajouter
nouvelle_ligne = pd.DataFrame({
    'student_id': ['S6'],
    'name': ['Scarlette Fisher'],
    'marks': [205]
})

print("Nouvelle ligne:")
print(nouvelle_ligne)
print()

# Ajouter la ligne avec concat
df_combined = pd.concat([student_data1, nouvelle_ligne], ignore_index=True)

print("DataFrame après ajout de la nouvelle ligne:")
print(df_combined)