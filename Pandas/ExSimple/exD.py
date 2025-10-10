"""
Exercice D: Comparer deux Series Pandas
ds1 = pd.Series([2, 4, 6, 8, 10])
ds2 = pd.Series([1, 3, 5, 7, 10])
"""

import pandas as pd
import numpy as np

print("=" * 70)
print("COMPARAISON DE DEUX SERIES PANDAS")
print("=" * 70)
print()

# Création des deux Series données
print("1. Création des Series à comparer")
print("-" * 70)
ds1 = pd.Series([2, 4, 6, 8, 10], name='ds1')
ds2 = pd.Series([1, 3, 5, 7, 10], name='ds2')

print("ds1:")
print(ds1)
print()
print("ds2:")
print(ds2)
print()

# Comparaison d'égalité (==)
print("2. ÉGALITÉ (ds1 == ds2)")
print("-" * 70)
egalite = ds1 == ds2
print(egalite)
print(f"Résultat: {egalite.tolist()}")
print(f"Nombre de valeurs égales: {egalite.sum()}")
print()

# Comparaison de différence (!=)
print("3. DIFFÉRENCE (ds1 != ds2)")
print("-" * 70)
difference = ds1 != ds2
print(difference)
print(f"Résultat: {difference.tolist()}")
print(f"Nombre de valeurs différentes: {difference.sum()}")
print()

# Supériorité (>)
print("4. SUPÉRIORITÉ (ds1 > ds2)")
print("-" * 70)
superieur = ds1 > ds2
print(superieur)
print(f"Résultat: {superieur.tolist()}")
print(f"Nombre de cas où ds1 > ds2: {superieur.sum()}")
print()

# Supériorité ou égalité (>=)
print("5. SUPÉRIORITÉ OU ÉGALITÉ (ds1 >= ds2)")
print("-" * 70)
superieur_egal = ds1 >= ds2
print(superieur_egal)
print(f"Résultat: {superieur_egal.tolist()}")
print(f"Nombre de cas où ds1 >= ds2: {superieur_egal.sum()}")
print()

# Infériorité (<)
print("6. INFÉRIORITÉ (ds1 < ds2)")
print("-" * 70)
inferieur = ds1 < ds2
print(inferieur)
print(f"Résultat: {inferieur.tolist()}")
print(f"Nombre de cas où ds1 < ds2: {inferieur.sum()}")
print()

# Infériorité ou égalité (<=)
print("7. INFÉRIORITÉ OU ÉGALITÉ (ds1 <= ds2)")
print("-" * 70)
inferieur_egal = ds1 <= ds2
print(inferieur_egal)
print(f"Résultat: {inferieur_egal.tolist()}")
print(f"Nombre de cas où ds1 <= ds2: {inferieur_egal.sum()}")
print()

# Comparaison globale avec .equals()
print("8. COMPARAISON GLOBALE (.equals())")
print("-" * 70)
sont_identiques = ds1.equals(ds2)
print(f"ds1.equals(ds2): {sont_identiques}")
print("Note: .equals() retourne True seulement si TOUTES les valeurs sont identiques")
print()

# Test avec deux Series identiques
ds3 = pd.Series([2, 4, 6, 8, 10])
print(f"ds1.equals(ds3): {ds1.equals(ds3)}")
print()

# Tableau récapitulatif
print("9. TABLEAU RÉCAPITULATIF DES COMPARAISONS")
print("-" * 70)
print(f"{'Index':<10} {'ds1':<10} {'ds2':<10} {'==':<10} {'!=':<10} {'>':<10} {'>=':<10} {'<':<10} {'<=':<10}")
print("-" * 70)
for i in range(len(ds1)):
    print(f"{i:<10} {ds1.iloc[i]:<10} {ds2.iloc[i]:<10} {str(ds1.iloc[i] == ds2.iloc[i]):<10} "
          f"{str(ds1.iloc[i] != ds2.iloc[i]):<10} {str(ds1.iloc[i] > ds2.iloc[i]):<10} "
          f"{str(ds1.iloc[i] >= ds2.iloc[i]):<10} {str(ds1.iloc[i] < ds2.iloc[i]):<10} "
          f"{str(ds1.iloc[i] <= ds2.iloc[i]):<10}")
print()

# Filtrage avec comparaison
print("10. UTILISATION DES COMPARAISONS POUR FILTRER")
print("-" * 70)
print("Valeurs de ds1 où ds1 > ds2:")
filtree = ds1[ds1 > ds2]
print(filtree)
print()

print("Valeurs de ds1 où ds1 == ds2:")
egales = ds1[ds1 == ds2]
print(egales)
print()

# Opérations logiques combinées
print("11. OPÉRATIONS LOGIQUES COMBINÉES")
print("-" * 70)
print("ds1 supérieur à 5 ET ds2 inférieur à 8:")
condition_combinee = (ds1 > 5) & (ds2 < 8)
print(condition_combinee)
print(f"Résultat: {condition_combinee.tolist()}")
print()

print("ds1 égal à 2 OU ds2 égal à 10:")
condition_ou = (ds1 == 2) | (ds2 == 10)
print(condition_ou)
print(f"Résultat: {condition_ou.tolist()}")
print()

# Statistiques de comparaison
print("12. STATISTIQUES DE COMPARAISON")
print("-" * 70)
print(f"Pourcentage de valeurs égales: {(ds1 == ds2).sum() / len(ds1) * 100:.1f}%")
print(f"Pourcentage où ds1 > ds2: {(ds1 > ds2).sum() / len(ds1) * 100:.1f}%")
print(f"Pourcentage où ds1 < ds2: {(ds1 < ds2).sum() / len(ds1) * 100:.1f}%")
print()

# Différence absolue entre les deux Series
print("13. DIFFÉRENCE ABSOLUE ENTRE LES DEUX SERIES")
print("-" * 70)
diff_absolue = (ds1 - ds2).abs()
print("Différence absolue (|ds1 - ds2|):")
print(diff_absolue)
print(f"Différence moyenne: {diff_absolue.mean():.2f}")
print(f"Différence maximale: {diff_absolue.max()}")