"""
Exercice J: Tableaux croisés dynamiques avec Titanic et visualisations
"""

import pandas as pd
import matplotlib.pyplot as plt

# Charger les données Titanic
df = pd.read_csv('../../Data/titanic.csv')

print("Résumé du fichier Titanic:")
print(df.info())
print()
print(df.head())
print()

# Créer un tableau croisé dynamique : survivants par sexe et classe
pivot_survie = df.pivot_table(values='survived', index='sex', columns='pclass', aggfunc='sum')

print("Tableau croisé : Nombre de survivants par sexe et classe")
print(pivot_survie)
print()

# Visualiser avec un graphique à barres groupées
pivot_survie.plot(kind='bar', figsize=(10, 6), edgecolor='black')
plt.xlabel('Sexe')
plt.ylabel('Nombre de survivants')
plt.title('Nombre de survivants par sexe et classe')
plt.legend(title='Classe', labels=['1ère classe', '2ème classe', '3ème classe'])
plt.xticks(rotation=0)
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# Moyenne des survivants par sexe et classe
pivot_moyenne = df.pivot_table(values='survived', index='sex', columns='pclass', aggfunc='mean')

print("\nTableau croisé : Taux de survie moyen par sexe et classe")
print(pivot_moyenne)
print()

# Visualiser avec un heatmap
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(pivot_moyenne, cmap='RdYlGn', aspect='auto')

# Ajouter les valeurs dans les cellules
for i in range(len(pivot_moyenne.index)):
    for j in range(len(pivot_moyenne.columns)):
        text = ax.text(j, i, f'{pivot_moyenne.iloc[i, j]:.2f}',
                      ha="center", va="center", color="black", fontweight='bold')

# Configurer les axes
ax.set_xticks(range(len(pivot_moyenne.columns)))
ax.set_yticks(range(len(pivot_moyenne.index)))
ax.set_xticklabels(pivot_moyenne.columns)
ax.set_yticklabels(pivot_moyenne.index)
ax.set_xlabel('Classe')
ax.set_ylabel('Sexe')
ax.set_title('Taux de survie moyen par sexe et classe')

# Ajouter une barre de couleur
plt.colorbar(im, ax=ax, label='Taux de survie')
plt.tight_layout()
plt.show()