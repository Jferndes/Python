"""
Exercice V: Détecter et gérer les valeurs manquantes dans un DataFrame
"""

import pandas as pd
import numpy as np

# Données avec valeurs manquantes
data = {
    'ord_no': [70001.0, np.nan, 70002.0, 70004.0, np.nan, 70005.0, np.nan, 70010.0, 70003.0, 70012.0, np.nan, 70013.0],
    'purch_amt': [150.50, 270.65, 65.26, 110.50, 948.50, 2400.60, 5760.00, 1983.43, 2480.40, 250.45, 75.29, 3045.60],
    'ord_date': ['05/10/2012', '10/09/2012', np.nan, '17/08/2012', '10/09/2012', '2012-07-27', '2012-09-10', '2012-10-10', '2012-10-10', '2012-06-27', '17/08/2012', '2012-04-25'],
    'customer_id': [3002, 3001, 3001, 3003, 3002, 3001, 3001, 3004, 3003, 3002, 3001, 3001],
    'salesman_id': [5002.0, 5003.0, 5001.0, np.nan, 5002.0, 5001.0, 5001.0, np.nan, 5003.0, 5002.0, 5003.0, np.nan]
}

df = pd.DataFrame(data)

print("DataFrame original:")
print(df)
print()

# 1. Détecter les valeurs manquantes (True/False)
print("V.1 - Détecter les valeurs manquantes (True = manquante):")
print(df.isnull())
print()

# 2. Identifier les colonnes avec au moins une valeur manquante
print("V.2 - Colonnes avec au moins une valeur manquante:")
colonnes_avec_nan = df.columns[df.isnull().any()].tolist()
print(colonnes_avec_nan)
print()

# 3. Compter le nombre de valeurs manquantes par colonne
print("V.3 - Nombre de valeurs manquantes par colonne:")
print(df.isnull().sum())
print()

# 4. Remplacer les valeurs manquantes
print("V.4 - Remplacer les valeurs manquantes:")
df_filled = df.fillna({'ord_no': 0, 'ord_date': 'Inconnue', 'salesman_id': 0})
print(df_filled)
print()

# 5. Grouper par customer_id et calculer statistiques sur purch_amt
print("V.5 - Statistiques de purch_amt groupées par customer_id:")
stats = df.groupby('customer_id')['purch_amt'].agg(['mean', 'min', 'max'])
print(stats)