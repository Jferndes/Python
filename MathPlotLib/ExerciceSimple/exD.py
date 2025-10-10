"""
Exercice D: Graphique à barres de la popularité des langages de programmation
"""

import matplotlib.pyplot as plt

# Données
langages = ['Java', 'Python', 'PHP', 'JavaScript', 'C#', 'C++']
popularite = [22.2, 17.6, 8.8, 8, 7.7, 6.7]

# Créer le graphique à barres
plt.figure(figsize=(10, 6))
plt.bar(langages, popularite, color='steelblue', edgecolor='black')

# Ajouter les labels et le titre
plt.xlabel('Langages de programmation')
plt.ylabel('Popularité (%)')
plt.title('Popularité des langages de programmation')

# Ajouter une grille horizontale
plt.grid(True, axis='y', alpha=0.3)

# Afficher le graphique
plt.show()