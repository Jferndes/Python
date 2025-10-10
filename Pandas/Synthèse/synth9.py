"""
Synthèse 9: Dates et séries temporelles
"""

import pandas as pd

# Création du DataFrame
dates = pd.date_range("2024-01-01", periods=10)
df = pd.DataFrame({
    "Date": dates,
    "Ventes": [100, 110, 120, 115, 130, 140, 150, 160, 155, 170]
})

print("DataFrame original:")
print(df)
print()

# 1. Convertir Date en index
df_indexed = df.set_index('Date')
print("1. Date comme index:")
print(df_indexed)
print()

# 2. Calculer la moyenne mobile sur 3 jours
df_indexed['Moyenne_mobile_3j'] = df_indexed['Ventes'].rolling(3).mean()
print("2. Moyenne mobile sur 3 jours:")
print(df_indexed)
print()

# 3. Calculer le pourcentage d'évolution jour après jour
df_indexed['Pct_change'] = df_indexed['Ventes'].pct_change() * 100
print("3. Pourcentage d'évolution jour après jour:")
print(df_indexed)