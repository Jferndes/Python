"""
Module de chargement des données CSV
"""
import pandas as pd


def chargerDonneesSport(cheminFichier):
    """
    Charge les données de sport depuis un fichier CSV
    
    Args:
        cheminFichier (str): Chemin vers le fichier sport_raw.csv
    
    Returns:
        pd.DataFrame: DataFrame avec les données de sport
    """
    df = pd.read_csv(cheminFichier)
    print(f"✓ Données sport chargées : {len(df)} lignes")
    return df


def chargerDonneesTravail(cheminFichier):
    """
    Charge les données de travail depuis un fichier CSV
    
    Args:
        cheminFichier (str): Chemin vers le fichier travail_raw.csv
    
    Returns:
        pd.DataFrame: DataFrame avec les données de travail
    """
    df = pd.read_csv(cheminFichier)
    print(f"✓ Données travail chargées : {len(df)} lignes")
    return df


def afficherApercu(df, nom):
    """
    Affiche un aperçu du DataFrame
    
    Args:
        df (pd.DataFrame): DataFrame à afficher
        nom (str): Nom du dataset
    """
    print(f"\n{'='*60}")
    print(f"Aperçu de {nom}")
    print(f"{'='*60}")
    print(f"Dimensions : {df.shape}")
    print(f"\nPremières lignes :")
    print(df.head())
    print(f"\nTypes de données :")
    print(df.dtypes)
    print(f"\nValeurs manquantes :")
    print(df.isnull().sum())
