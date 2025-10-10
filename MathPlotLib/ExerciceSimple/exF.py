"""
Exercice F: Diagramme circulaire (pie chart) de la popularité des langages
"""

import matplotlib.pyplot as plt

# Données
langages = ['Java', 'Python', 'PHP', 'JavaScript', 'C#', 'C++']
popularite = [22.2, 17.6, 8.8, 8, 7.7, 6.7]

# Créer le diagramme circulaire
plt.figure(figsize=(8, 8))
plt.pie(popularite, labels=langages, autopct='%1.1f%%', startangle=90)

# Ajouter le titre
plt.title('Popularité des langages de programmation')

# Afficher le graphique
plt.show()