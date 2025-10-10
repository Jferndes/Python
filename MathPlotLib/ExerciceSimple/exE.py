"""
Exercice E: Graphique à barres horizontales de la popularité des langages
"""

import matplotlib.pyplot as plt

# Données
langages = ['Java', 'Python', 'PHP', 'JavaScript', 'C#', 'C++']
popularite = [22.2, 17.6, 8.8, 8, 7.7, 6.7]

# Créer le graphique à barres horizontales
plt.figure(figsize=(10, 6))
plt.barh(langages, popularite, color='coral', edgecolor='black')

# Ajouter les labels et le titre
plt.xlabel('Popularité (%)')
plt.ylabel('Langages de programmation')
plt.title('Popularité des langages de programmation')

# Ajouter une grille verticale
plt.grid(True, axis='x', alpha=0.3)

# Afficher le graphique
plt.show()