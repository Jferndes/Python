"""
Module pour les graphiques de régression
"""
import matplotlib.pyplot as plt
import numpy as np
from visualisation.utilitairesGraphiques import (
    obtenirCouleur, sauvegarderGraphique, ajouterGridEtLegende, formaterAxes
)


def tracerScatterAvecRegression(resultatsRegression, activite, nomFichier, 
                                  titreX='Durée (min)', titreY='Calories'):
    """
    Trace un scatter plot avec la droite de régression
    
    Args:
        resultatsRegression (dict): Résultats de la régression
        activite (str): Nom de l'activité
        nomFichier (str): Nom du fichier de sauvegarde
        titreX (str): Titre axe X
        titreY (str): Titre axe Y
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = resultatsRegression['x']
    y = resultatsRegression['y']
    predictions = resultatsRegression['predictions']
    pente = resultatsRegression['pente']
    intercept = resultatsRegression['intercept']
    r2 = resultatsRegression['r2']
    
    couleur = obtenirCouleur(activite)
    
    # Scatter plot
    ax.scatter(x, y, alpha=0.5, s=30, color=couleur, label='Données observées')
    
    # Droite de régression
    ax.plot(x, predictions, 'r-', linewidth=2, label='Régression linéaire')
    
    # Équation et R²
    equation = f'y = {pente:.2f}x + {intercept:.2f}'
    r2_text = f'R² = {r2:.3f}'
    
    ax.text(0.05, 0.95, equation, transform=ax.transAxes, 
            fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax.text(0.05, 0.88, r2_text, transform=ax.transAxes, 
            fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    # Formatage
    titre = f'Régression linéaire - {activite.capitalize()}'
    formaterAxes(ax, titreX, titreY, titre)
    ajouterGridEtLegende()
    
    plt.tight_layout()
    sauvegarderGraphique(nomFichier)
    plt.close()


def tracerRegressionMultivariee(resultatsRegression, activite, nomFichier):
    """
    Trace les résultats d'une régression multivariée
    
    Args:
        resultatsRegression (dict): Résultats de la régression
        activite (str): Nom de l'activité
        nomFichier (str): Nom du fichier de sauvegarde
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    X = resultatsRegression['X']
    y = resultatsRegression['y']
    predictions = resultatsRegression['predictions']
    r2 = resultatsRegression['r2']
    coefs = resultatsRegression['coefficients']
    intercept = resultatsRegression['intercept']
    
    couleur = obtenirCouleur(activite)
    
    # Graphique 1 : Prédictions vs Observations
    ax1.scatter(y, predictions, alpha=0.5, s=30, color=couleur)
    
    # Droite y=x (prédiction parfaite)
    min_val = min(y.min(), predictions.min())
    max_val = max(y.max(), predictions.max())
    ax1.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Prédiction parfaite')
    
    formaterAxes(ax1, 'Calories observées', 'Calories prédites', 
                 f'Régression multivariée - {activite.capitalize()}')
    ax1.text(0.05, 0.95, f'R² = {r2:.3f}', transform=ax1.transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Graphique 2 : Influence de chaque variable
    ax2.scatter(X[:, 0], y, alpha=0.5, s=30, color=couleur, label='Durée (min)')
    ax2.scatter(X[:, 1], y, alpha=0.5, s=30, color='orange', label='Poids (kg)', marker='s')
    
    formaterAxes(ax2, 'Valeur de la variable', 'Calories', 
                 'Influence des variables')
    
    # Afficher coefficients
    equation = f'Calories = {coefs[0]:.2f}×durée + {coefs[1]:.2f}×poids + {intercept:.2f}'
    ax2.text(0.05, 0.95, equation, transform=ax2.transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    sauvegarderGraphique(nomFichier)
    plt.close()


def tracerRegressionCafeProductivite(resultatsRegression, nomFichier):
    """
    Trace la régression café → productivité
    
    Args:
        resultatsRegression (dict): Résultats de la régression
        nomFichier (str): Nom du fichier de sauvegarde
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = resultatsRegression['x']
    y = resultatsRegression['y']
    predictions = resultatsRegression['predictions']
    pente = resultatsRegression['pente']
    intercept = resultatsRegression['intercept']
    r2 = resultatsRegression['r2']
    
    # Scatter plot
    ax.scatter(x, y, alpha=0.4, s=40, color='#8B4513', label='Données observées')
    
    # Droite de régression
    ax.plot(x, predictions, 'r-', linewidth=2.5, label='Régression linéaire')
    
    # Équation et R²
    equation = f'Productivité = {pente:.2f} × café + {intercept:.2f}'
    r2_text = f'R² = {r2:.3f}'
    
    ax.text(0.05, 0.95, equation, transform=ax.transAxes, 
            fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax.text(0.05, 0.88, r2_text, transform=ax.transAxes, 
            fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    # Zone d'effet décroissant
    ax.axvspan(6, x.max(), alpha=0.2, color='red', label='Zone rendement décroissant')
    
    # Formatage
    formaterAxes(ax, 'Tasses de café', 'Productivité', 
                 'Effet du café sur la productivité (0-6 tasses)')
    ajouterGridEtLegende()
    
    plt.tight_layout()
    sauvegarderGraphique(nomFichier)
    plt.close()


def tracerComparaisonActivites(resultatsDict, nomFichier):
    """
    Compare les pentes de régression entre activités
    
    Args:
        resultatsDict (dict): Dictionnaire {activite: resultatsRegression}
        nomFichier (str): Nom du fichier de sauvegarde
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    activites = []
    pentes = []
    
    for activite, resultats in resultatsDict.items():
        activites.append(activite.capitalize())
        pentes.append(resultats['pente'])
    
    couleurs = [obtenirCouleur(act.lower()) for act in activites]
    
    bars = ax.bar(activites, pentes, color=couleurs, alpha=0.7, edgecolor='black')
    
    # Ajouter valeurs sur les barres
    for bar, pente in zip(bars, pentes):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{pente:.1f}',
                ha='center', va='bottom', fontweight='bold')
    
    formaterAxes(ax, 'Activité', 'Calories brûlées par minute', 
                 'Comparaison des intensités énergétiques')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    sauvegarderGraphique(nomFichier)
    plt.close()
