"""
Module pour les fonctions utilitaires de visualisation
"""
import matplotlib.pyplot as plt
from config.constantes import FIGSIZE_DEFAULT, DPI_SAUVEGARDE, COULEURS_ACTIVITES


def configurerStyle():
    """
    Configure le style général des graphiques
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.figsize'] = FIGSIZE_DEFAULT
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 13
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9


def obtenirCouleur(activite):
    """
    Retourne la couleur associée à une activité
    
    Args:
        activite (str): Nom de l'activité
    
    Returns:
        str: Code couleur hexadécimal
    """
    return COULEURS_ACTIVITES.get(activite, '#95A5A6')


def sauvegarderGraphique(nomFichier, dossier='resultats'):
    """
    Sauvegarde le graphique actuel
    
    Args:
        nomFichier (str): Nom du fichier (avec .png)
        dossier (str): Dossier de destination
    """
    import os
    
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(dossier):
        os.makedirs(dossier)
    
    chemin = os.path.join(dossier, nomFichier)
    plt.savefig(chemin, dpi=DPI_SAUVEGARDE, bbox_inches='tight')
    print(f"✓ Graphique sauvegardé : {chemin}")


def ajouterGridEtLegende():
    """
    Ajoute une grille et optimise la légende
    """
    plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    plt.legend(framealpha=0.9, loc='best')


def formaterAxes(ax, titreX, titreY, titre):
    """
    Formate les axes d'un graphique
    
    Args:
        ax: Axe matplotlib
        titreX (str): Titre de l'axe X
        titreY (str): Titre de l'axe Y
        titre (str): Titre du graphique
    """
    ax.set_xlabel(titreX, fontweight='bold')
    ax.set_ylabel(titreY, fontweight='bold')
    ax.set_title(titre, fontweight='bold', pad=15)