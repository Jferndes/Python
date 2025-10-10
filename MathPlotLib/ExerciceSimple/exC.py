"""
Exercice C: Graphiques linéaires des données financières d'Alphabet Inc.
"""

import matplotlib.pyplot as plt
import pandas as pd

# Lecture du fichier CSV sans headers
# Ajuster le chemin selon votre structure de dossiers
df = pd.read_csv('C:\\Users\\joelf\\OneDrive\\Bureau\\ESIEA\\S7\\Python\\Python\\Data\\fdata.csv', header=None, names=['Date', 'Open', 'High', 'Low', 'Close'])

print("Données financières:")
print(df)
print()

# Créer le graphique avec plusieurs lignes
plt.figure(figsize=(10, 6))

plt.plot(df['Date'], df['Open'], marker='o', label='Ouverture', linewidth=2)
plt.plot(df['Date'], df['High'], marker='s', label='Haut', linewidth=2)
plt.plot(df['Date'], df['Low'], marker='^', label='Bas', linewidth=2)
plt.plot(df['Date'], df['Close'], marker='d', label='Clôture', linewidth=2)

# Ajouter les labels et le titre
plt.xlabel('Date')
plt.ylabel('Prix ($)')
plt.title('Données financières Alphabet Inc. (3-7 octobre 2016)')

# Ajouter la légende
plt.legend()

# Rotation des labels de dates pour la lisibilité
plt.xticks(rotation=45)

# Ajouter une grille
plt.grid(True, alpha=0.3)

# Ajuster l'espacement
plt.tight_layout()

# Afficher le graphique
plt.show()