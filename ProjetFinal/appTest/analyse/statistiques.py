"""
Module pour les calculs statistiques
"""
import numpy as np
import pandas as pd


def calculerStatistiquesDescriptives(data, nomVariable):
    """
    Calcule les statistiques descriptives d'une variable
    
    Args:
        data (array): Données
        nomVariable (str): Nom de la variable
    
    Returns:
        dict: Statistiques descriptives
    """
    stats = {
        'nom': nomVariable,
        'moyenne': np.mean(data),
        'mediane': np.median(data),
        'ecartType': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'q1': np.percentile(data, 25),
        'q3': np.percentile(data, 75)
    }
    
    return stats


def afficherStatistiques(stats):
    """
    Affiche les statistiques descriptives de manière formatée
    
    Args:
        stats (dict): Dictionnaire de statistiques
    """
    print(f"\nStatistiques - {stats['nom']}")
    print(f"  Moyenne : {stats['moyenne']:.2f}")
    print(f"  Médiane : {stats['mediane']:.2f}")
    print(f"  Écart-type : {stats['ecartType']:.2f}")
    print(f"  Min : {stats['min']:.2f}")
    print(f"  Max : {stats['max']:.2f}")
    print(f"  Q1 : {stats['q1']:.2f}")
    print(f"  Q3 : {stats['q3']:.2f}")


def detecterOutliers(data, seuil=3):
    """
    Détecte les outliers avec la méthode des z-scores
    
    Args:
        data (array): Données
        seuil (float): Seuil du z-score (défaut: 3)
    
    Returns:
        array: Masque booléen des outliers
    """
    zScores = np.abs((data - np.mean(data)) / np.std(data))
    return zScores > seuil


def calculerCorrelation(x, y):
    """
    Calcule le coefficient de corrélation de Pearson
    
    Args:
        x (array): Variable 1
        y (array): Variable 2
    
    Returns:
        tuple: (coefficient, p-value)
    """
    from scipy.stats import pearsonr
    
    # Supprimer les NaN
    masque = ~(np.isnan(x) | np.isnan(y))
    x = x[masque]
    y = y[masque]
    
    return pearsonr(x, y)


def creerMatriceCorrelation(df, colonnes):
    """
    Crée une matrice de corrélation pour les colonnes spécifiées
    
    Args:
        df (pd.DataFrame): DataFrame
        colonnes (list): Liste des noms de colonnes
    
    Returns:
        pd.DataFrame: Matrice de corrélation
    """
    return df[colonnes].corr()


def testerSignificativite(pValue, alpha=0.05):
    """
    Teste la significativité statistique
    
    Args:
        pValue (float): P-value
        alpha (float): Seuil de significativité
    
    Returns:
        bool: True si significatif
    """
    return pValue < alpha
