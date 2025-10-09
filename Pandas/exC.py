"""
Exercice C: Ajouter, soustraire, multiplier et diviser deux Series Pandas
"""

import pandas as pd
import numpy as np

print("=" * 70)
print("OPÉRATIONS ARITHMÉTIQUES SUR DEUX SERIES PANDAS")
print("=" * 70)
print()

# Création de deux Series
print("1. Création des deux Series")
print("-" * 70)
serie1 = pd.Series([10, 20, 30, 40, 50], name='Serie 1')
serie2 = pd.Series([2, 4, 6, 8, 10], name='Serie 2')

print("Serie 1:")
print(serie1)
print()
print("Serie 2:")
print(serie2)
print()

# Addition
print("2. ADDITION (Serie1 + Serie2)")
print("-" * 70)
addition = serie1 + serie2
print(addition)
print(f"Résultat en liste: {addition.tolist()}")
print()

# Soustraction
print("3. SOUSTRACTION (Serie1 - Serie2)")
print("-" * 70)
soustraction = serie1 - serie2
print(soustraction)
print(f"Résultat en liste: {soustraction.tolist()}")
print()

# Multiplication
print("4. MULTIPLICATION (Serie1 * Serie2)")
print("-" * 70)
multiplication = serie1 * serie2
print(multiplication)
print(f"Résultat en liste: {multiplication.tolist()}")
print()

# Division
print("5. DIVISION (Serie1 / Serie2)")
print("-" * 70)
division = serie1 / serie2
print(division)
print(f"Résultat en liste: {division.tolist()}")
print()

# Division entière
print("6. DIVISION ENTIÈRE (Serie1 // Serie2)")
print("-" * 70)
division_entiere = serie1 // serie2
print(division_entiere)
print(f"Résultat en liste: {division_entiere.tolist()}")
print()

# Modulo
print("7. MODULO (Serie1 % Serie2)")
print("-" * 70)
modulo = serie1 % serie2
print(modulo)
print(f"Résultat en liste: {modulo.tolist()}")
print()

# Puissance
print("8. PUISSANCE (Serie1 ** 2)")
print("-" * 70)
puissance = serie1 ** 2
print(puissance)
print(f"Résultat en liste: {puissance.tolist()}")
print()

# Opérations avec des Series de tailles différentes
print("9. Opérations avec Series de tailles différentes")
print("-" * 70)
serie_a = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
serie_b = pd.Series([5, 10, 15, 20], index=['a', 'b', 'c', 'd'])

print("Serie A:")
print(serie_a)
print()
print("Serie B:")
print(serie_b)
print()
print("Addition (Serie A + Serie B):")
resultat = serie_a + serie_b
print(resultat)
print("Note: L'index 'd' donne NaN car absent de Serie A")
print()

# Méthodes alternatives avec gestion des NaN
print("10. Méthodes avec paramètre fill_value")
print("-" * 70)
addition_fill = serie_a.add(serie_b, fill_value=0)
print("Addition avec fill_value=0:")
print(addition_fill)
print()

# Résumé de toutes les opérations
print("11. RÉSUMÉ - Tableau comparatif")
print("-" * 70)
print(f"{'Opération':<20} {'Symbole':<10} {'Exemple résultat'}")
print(f"{'-'*20} {'-'*10} {'-'*30}")
print(f"{'Addition':<20} {'+':<10} {(serie1 + serie2).iloc[0]}")
print(f"{'Soustraction':<20} {'-':<10} {(serie1 - serie2).iloc[0]}")
print(f"{'Multiplication':<20} {'*':<10} {(serie1 * serie2).iloc[0]}")
print(f"{'Division':<20} {'/':<10} {(serie1 / serie2).iloc[0]}")
print(f"{'Division entière':<20} {'//':<10} {(serie1 // serie2).iloc[0]}")
print(f"{'Modulo':<20} {'%':<10} {(serie1 % serie2).iloc[0]}")
print(f"{'Puissance':<20} {'**':<10} {(serie1 ** 2).iloc[0]}")
print()

# Opérations avec des scalaires
print("12. Opérations avec un scalaire")
print("-" * 70)
print(f"Serie1 + 100:\n{serie1 + 100}\n")
print(f"Serie1 * 3:\n{serie1 * 3}\n")
print(f"Serie1 / 2:\n{serie1 / 2}\n")