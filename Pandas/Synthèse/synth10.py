"""
Synthèse 10: Analyse exploratoire complète - Titanic
"""

import pandas as pd

# 1. Charger les données
df = pd.read_csv('../../Data/titanic.csv')
print("1. Données chargées:")
print(df.head())
print()

# 2. Nettoyer les valeurs manquantes
print("2. Valeurs manquantes avant nettoyage:")
print(df.isnull().sum())
print()

# Supprimer les colonnes avec trop de valeurs manquantes
df_clean = df.drop(columns=['deck'], errors='ignore')
# Remplir l'âge par la médiane
df_clean['age'] = df_clean['age'].fillna(df_clean['age'].median())
# Remplir embarked par la valeur la plus fréquente
df_clean['embarked'] = df_clean['embarked'].fillna(df_clean['embarked'].mode()[0])

print("Valeurs manquantes après nettoyage:")
print(df_clean.isnull().sum())
print()

# 3. Statistiques de base
print("3. Statistiques descriptives:")
print(df_clean.describe())
print()

print("Répartition des survivants:")
print(df_clean['survived'].value_counts())
print()

# 4. Grouper par sexe et calculer l'âge moyen et le taux de survie
print("4. Analyse par sexe:")
stats_par_sexe = df_clean.groupby('sex').agg({
    'age': 'mean',
    'survived': 'mean'
})
print(stats_par_sexe)