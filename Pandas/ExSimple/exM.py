"""
Exercice M: Joindre deux DataFrames le long des lignes
"""

import pandas as pd

# Premier DataFrame
student_data1 = pd.DataFrame({
    'student_id': ['S1', 'S2', 'S3', 'S4', 'S5'],
    'name': ['Danniella Fenton', 'Ryder Storey', 'Bryce Jensen', 'Ed Bernal', 'Kwame Morin'],
    'marks': [200, 210, 190, 222, 199]
})

# Second DataFrame
student_data2 = pd.DataFrame({
    'student_id': ['S4', 'S5', 'S6', 'S7', 'S8'],
    'name': ['Scarlette Fisher', 'Carla Williamson', 'Dante Morse', 'Kaiser William', 'Madeeha Preston'],
    'marks': [201, 200, 198, 219, 201]
})

print("DataFrame 1:")
print(student_data1)
print()

print("DataFrame 2:")
print(student_data2)
print()

# Concaténation le long des lignes (axis=0)
df_combined = pd.concat([student_data1, student_data2], axis=0, ignore_index=True)

print("DataFrames joints le long des lignes:")
print(df_combined)