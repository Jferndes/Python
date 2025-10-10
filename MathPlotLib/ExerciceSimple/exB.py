"""
Exercice B: Dessiner une ligne en utilisant des valeurs d'axes données
"""

import matplotlib.pyplot as plt

# Valeurs d'axes données
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [2, 4, 5, 7, 6, 8, 9, 11, 12, 12]

# Créer le graphique
plt.plot(x, y, color='red', linewidth=2, marker='o', markersize=6)

# Ajouter les labels et le titre
plt.xlabel('Valeurs X')
plt.ylabel('Valeurs Y')
plt.title('Tracé de ligne avec valeurs d\'axes données')

# Ajouter une grille
plt.grid(True, alpha=0.3)

# Afficher le graphique
plt.show()