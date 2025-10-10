"""
Exercice I: Graphique de dispersion avec distribution aléatoire en X et Y
"""

import matplotlib.pyplot as plt
import numpy as np

# Générer des distributions aléatoires
np.random.seed(42)  # Pour la reproductibilité
n_points = 100

x = np.random.randn(n_points)  # Distribution normale
y = np.random.randn(n_points)  # Distribution normale

# Créer le graphique de dispersion
plt.figure(figsize=(8, 6))
plt.scatter(x, y, alpha=0.6, edgecolors='black', s=50)

# Ajouter les labels et le titre
plt.xlabel('Distribution X')
plt.ylabel('Distribution Y')
plt.title('Graphique de dispersion - Distribution aléatoire')

# Ajouter une grille
plt.grid(True, alpha=0.3)

# Afficher le graphique
plt.show()