"""
Exercice A: Dessiner une ligne avec étiquettes appropriées sur les axes et un titre
"""

import matplotlib.pyplot as plt

# Données pour la ligne
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Créer le graphique
plt.plot(x, y, color='blue', linewidth=2, marker='x')

# Ajouter les labels et le titre
plt.xlabel('Axe X')
plt.ylabel('Axe Y')
plt.title('Graphique linéaire simple')

# Ajouter une grille pour la lisibilité
plt.grid(True, alpha=0.3)

# Afficher le graphique
plt.show()