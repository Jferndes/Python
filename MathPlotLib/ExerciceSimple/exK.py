"""
Exercice K: Générer des points avec NumPy et interpoler avec SciPy
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Générer un ensemble de points de données
np.random.seed(42)
x = np.linspace(0, 10, 10)  # 10 points entre 0 et 10
y = np.sin(x) + np.random.randn(10) * 0.3  # Fonction sinusoïdale avec du bruit

# Créer une fonction d'interpolation
f_linear = interpolate.interp1d(x, y, kind='linear')
f_cubic = interpolate.interp1d(x, y, kind='cubic')

# Générer des points plus denses pour l'interpolation
x_dense = np.linspace(0, 10, 100)
y_linear = f_linear(x_dense)
y_cubic = f_cubic(x_dense)

# Créer le graphique
plt.figure(figsize=(10, 6))

# Points originaux
plt.scatter(x, y, color='red', s=100, zorder=5, label='Points originaux', edgecolors='black')

# Interpolation linéaire
plt.plot(x_dense, y_linear, 'b--', linewidth=2, label='Interpolation linéaire')

# Interpolation cubique
plt.plot(x_dense, y_cubic, 'g-', linewidth=2, label='Interpolation cubique')

# Ajouter les labels et le titre
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Interpolation de données avec SciPy')
plt.legend()
plt.grid(True, alpha=0.3)

# Afficher le graphique
plt.show()