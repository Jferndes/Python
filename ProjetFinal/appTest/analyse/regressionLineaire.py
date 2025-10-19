"""
Module pour les régressions linéaires
"""
import numpy as np
from scipy import stats


def regressionLineaireSimple(x, y):
    """
    Calcule une régression linéaire simple y = a*x + b
    
    Args:
        x (array): Variable indépendante
        y (array): Variable dépendante
    
    Returns:
        dict: Dictionnaire avec pente, intercept, r2, residus, predictions
    """
    # Supprimer les NaN
    masque = ~(np.isnan(x) | np.isnan(y))
    x = x[masque]
    y = y[masque]
    
    # Régression
    pente, intercept, rValue, pValue, stdErr = stats.linregress(x, y)
    
    # Prédictions et résidus
    predictions = pente * x + intercept
    residus = y - predictions
    
    # R²
    r2 = rValue ** 2
    
    return {
        'pente': pente,
        'intercept': intercept,
        'r2': r2,
        'pValue': pValue,
        'stdErr': stdErr,
        'predictions': predictions,
        'residus': residus,
        'x': x,
        'y': y
    }


def regressionLineaireMultiple(X, y):
    """
    Calcule une régression linéaire multiple y = a1*x1 + a2*x2 + ... + b
    
    Args:
        X (np.array): Matrice des variables indépendantes (n_samples, n_features)
        y (np.array): Variable dépendante
    
    Returns:
        dict: Dictionnaire avec coefficients, intercept, r2, residus, predictions
    """
    # Supprimer les lignes avec NaN
    masque = ~(np.isnan(X).any(axis=1) | np.isnan(y))
    X = X[masque]
    y = y[masque]
    
    # Ajouter colonne de 1 pour l'intercept
    XAvecIntercept = np.column_stack([X, np.ones(len(X))])
    
    # Calcul des coefficients par moindres carrés
    coefficients = np.linalg.lstsq(XAvecIntercept, y, rcond=None)[0]
    
    # Séparer coefficients et intercept
    coefs = coefficients[:-1]
    intercept = coefficients[-1]
    
    # Prédictions et résidus
    predictions = X @ coefs + intercept
    residus = y - predictions
    
    # R²
    ssTot = np.sum((y - np.mean(y)) ** 2)
    ssRes = np.sum(residus ** 2)
    r2 = 1 - (ssRes / ssTot)
    
    return {
        'coefficients': coefs,
        'intercept': intercept,
        'r2': r2,
        'predictions': predictions,
        'residus': residus,
        'X': X,
        'y': y
    }


def calculerMetriques(residus):
    """
    Calcule les métriques d'évaluation
    
    Args:
        residus (array): Résidus du modèle
    
    Returns:
        dict: Métriques (RMSE, MAE, etc.)
    """
    rmse = np.sqrt(np.mean(residus ** 2))
    mae = np.mean(np.abs(residus))
    
    return {
        'rmse': rmse,
        'mae': mae,
        'residusMoyen': np.mean(residus),
        'residusStd': np.std(residus)
    }


def interpreterPenteCalories(pente, activite):
    """
    Interprète la pente de la régression calories ~ durée
    
    Args:
        pente (float): Pente de la régression (calories/minute)
        activite (str): Nom de l'activité
    
    Returns:
        str: Interprétation textuelle
    """
    interpretation = f"\n{'='*60}\n"
    interpretation += f"INTERPRÉTATION - {activite.upper()}\n"
    interpretation += f"{'='*60}\n"
    interpretation += f"Pente : {pente:.2f} calories/minute\n"
    interpretation += f"Cela signifie qu'en moyenne, chaque minute supplémentaire\n"
    interpretation += f"de {activite} brûle {pente:.2f} calories.\n"
    
    # Calculer l'équivalent horaire
    caloriesHeure = pente * 60
    interpretation += f"\nÉquivalent : {caloriesHeure:.0f} calories/heure\n"
    
    return interpretation
