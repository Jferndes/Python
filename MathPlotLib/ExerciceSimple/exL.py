"""
Exercice L: Fonction g et fonction récursive f
"""

import numpy as np
import matplotlib.pyplot as plt

# Définir la fonction g sur [0,2[
def g(x):
    return x / (1 - x)

# Tracer g sur [0, 1.99] avec un pas de 0.01
x_g = np.arange(0, 1.99, 0.01)
y_g = g(x_g)

plt.figure(figsize=(10, 6))
plt.plot(x_g, y_g, 'b-', linewidth=2, label='g(x) = x/(1-x)')
plt.xlabel('x')
plt.ylabel('g(x)')
plt.title('Courbe représentative de g(x) sur [0, 2[')
plt.grid(True, alpha=0.3)
plt.legend()
plt.ylim(-5, 50)  # Limiter l'axe Y pour une meilleure visualisation
plt.show()

# Définir la fonction f de manière récursive
def f(x, n_max=1000):
    """
    f est définie récursivement:
    f(0) = 0
    f(x) = 1 + f(g(x)) pour x > 0
    
    On limite la récursion avec n_max pour éviter les débordements
    """
    if x <= 0:
        return 0
    if x >= 1:
        # Pour x >= 1, g(x) serait négatif ou infini, on arrête la récursion
        return 1
    
    # Calculer de manière itérative pour éviter la récursion profonde
    result = 0
    current_x = x
    for _ in range(n_max):
        if current_x >= 1:
            result += 1
            break
        result += 1
        current_x = g(current_x)
        if current_x >= 1 or current_x <= 0:
            break
    
    return result

# Tracer f sur [0, 6]
x_f = np.linspace(0.01, 6, 600)
y_f = [f(xi) for xi in x_f]

plt.figure(figsize=(10, 6))
plt.plot(x_f, y_f, 'r-', linewidth=2, label='f(x)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Courbe représentative de f(x) sur [0, 6]')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()

# Trouver la plus petite valeur a > 0 telle que f(a) > 4
print("\nRecherche de la plus petite valeur a > 0 telle que f(a) > 4:")
tolerance = 0.001
for a in np.arange(0.001, 6, tolerance):
    if f(a) > 4:
        print(f"La plus petite valeur a telle que f(a) > 4 est: a ≈ {a:.4f}")
        print(f"f({a:.4f}) = {f(a)}")
        break