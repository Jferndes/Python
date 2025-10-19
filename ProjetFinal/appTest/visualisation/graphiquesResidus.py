"""
Module pour les graphiques des résidus
"""
import matplotlib.pyplot as plt
import numpy as np
from visualisation.utilitairesGraphiques import (
    obtenirCouleur, sauvegarderGraphique, formaterAxes
)


def tracerResidusDuree(resultatsRegression, activite, nomFichier):
    """
    Trace les résidus en fonction de la durée
    
    Args:
        resultatsRegression (dict): Résultats de la régression
        activite (str): Nom de l'activité
        nomFichier (str): Nom du fichier de sauvegarde
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    x = resultatsRegression['x']
    residus = resultatsRegression['residus']
    couleur = obtenirCouleur(activite)
    
    # Graphique 1 : Résidus vs Durée
    ax1.scatter(x, residus, alpha=0.5, s=30, color=couleur)
    ax1.axhline(y=0, color='r', linestyle='--', linewidth=2, label='Résidu = 0')
    
    formaterAxes(ax1, 'Durée (min)', 'Résidus', 
                 f'Résidus vs Durée - {activite.capitalize()}')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Graphique 2 : Distribution des résidus (histogramme)
    ax2.hist(residus, bins=30, color=couleur, alpha=0.7, edgecolor='black')
    ax2.axvline(x=0, color='r', linestyle='--', linewidth=2, label='Résidu = 0')
    
    formaterAxes(ax2, 'Résidus', 'Fréquence', 
                 'Distribution des résidus')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.legend()
    
    plt.tight_layout()
    sauvegarderGraphique(nomFichier)
    plt.close()


def analyserResidus(resultatsRegression, activite):
    """
    Analyse les résidus et génère un rapport textuel
    
    Args:
        resultatsRegression (dict): Résultats de la régression
        activite (str): Nom de l'activité
    
    Returns:
        str: Rapport d'analyse
    """
    residus = resultatsRegression['residus']
    x = resultatsRegression['x']
    
    rapport = f"\n{'='*60}\n"
    rapport += f"ANALYSE DES RÉSIDUS - {activite.upper()}\n"
    rapport += f"{'='*60}\n\n"
    
    # Statistiques des résidus
    rapport += f"Moyenne des résidus : {np.mean(residus):.2f}\n"
    rapport += f"Écart-type des résidus : {np.std(residus):.2f}\n"
    rapport += f"Min : {np.min(residus):.2f} | Max : {np.max(residus):.2f}\n\n"
    
    # Test de linéarité
    rapport += "1. LINÉARITÉ :\n"
    corr_residus_x = np.corrcoef(x, residus)[0, 1]
    if abs(corr_residus_x) < 0.1:
        rapport += "   ✓ Bonne : pas de pattern dans les résidus\n"
    else:
        rapport += "   ⚠ Attention : corrélation entre résidus et x détectée\n"
    
    # Test d'homoscédasticité
    rapport += "\n2. HOMOSCÉDASTICITÉ :\n"
    # Diviser en 3 groupes
    n = len(x)
    idx_sorted = np.argsort(x)
    group_size = n // 3
    
    var1 = np.var(residus[idx_sorted[:group_size]])
    var3 = np.var(residus[idx_sorted[-group_size:]])
    ratio = max(var1, var3) / min(var1, var3)
    
    if ratio < 2:
        rapport += "   ✓ Bonne : variance constante\n"
    else:
        rapport += f"   ⚠ Attention : hétéroscédasticité (ratio variance = {ratio:.2f})\n"
    
    # Détection d'outliers
    rapport += "\n3. OUTLIERS :\n"
    z_scores = np.abs((residus - np.mean(residus)) / np.std(residus))
    outliers = np.sum(z_scores > 3)
    rapport += f"   Nombre d'outliers (|z| > 3) : {outliers} ({outliers/len(residus)*100:.1f}%)\n"
    
    if outliers / len(residus) < 0.05:
        rapport += "   ✓ Peu d'outliers\n"
    else:
        rapport += "   ⚠ Attention : présence significative d'outliers\n"
    
    return rapport


def tracerQQPlot(resultatsRegression, activite, nomFichier):
    """
    Trace un Q-Q plot pour vérifier la normalité des résidus
    
    Args:
        resultatsRegression (dict): Résultats de la régression
        activite (str): Nom de l'activité
        nomFichier (str): Nom du fichier de sauvegarde
    """
    from scipy import stats as sp_stats
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    residus = resultatsRegression['residus']
    couleur = obtenirCouleur(activite)
    
    # Q-Q plot
    sp_stats.probplot(residus, dist="norm", plot=ax)
    ax.get_lines()[0].set_marker('o')
    ax.get_lines()[0].set_markerfacecolor(couleur)
    ax.get_lines()[0].set_markeredgecolor('black')
    ax.get_lines()[0].set_markersize(5)
    ax.get_lines()[0].set_alpha(0.6)
    ax.get_lines()[1].set_color('red')
    ax.get_lines()[1].set_linewidth(2)
    
    formaterAxes(ax, 'Quantiles théoriques', 'Quantiles observés', 
                 f'Q-Q Plot - {activite.capitalize()}')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    sauvegarderGraphique(nomFichier)
    plt.close()
