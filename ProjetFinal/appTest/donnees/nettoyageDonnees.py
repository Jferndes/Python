"""
Module de nettoyage et préparation des données
"""
import pandas as pd
import numpy as np


def nettoyerDonneesSport(df):
    """
    Nettoie les données de sport
    
    Args:
        df (pd.DataFrame): DataFrame brut du sport
    
    Returns:
        pd.DataFrame: DataFrame nettoyé
    """
    dfClean = df.copy()
    
    # Convertir la date en datetime
    dfClean['date'] = pd.to_datetime(dfClean['date'])
    
    # Nettoyer les noms d'activités (minuscules, sans espaces)
    dfClean['activite'] = dfClean['activite'].str.lower().str.strip()
    
    # Supprimer les lignes avec valeurs manquantes critiques
    dfClean = dfClean.dropna(subset=['duree', 'poids_kg', 'calories'])
    
    # Supprimer les valeurs aberrantes (durée ou calories négatives)
    dfClean = dfClean[(dfClean['duree'] > 0) & (dfClean['calories'] > 0) & (dfClean['poids_kg'] > 0)]
    
    print(f"✓ Nettoyage sport : {len(df)} → {len(dfClean)} lignes conservées")
    
    return dfClean


def nettoyerDonneesTravail(df):
    """
    Nettoie les données de travail
    
    Args:
        df (pd.DataFrame): DataFrame brut du travail
    
    Returns:
        pd.DataFrame: DataFrame nettoyé
    """
    dfClean = df.copy()
    
    # Convertir la date en datetime
    dfClean['date'] = pd.to_datetime(dfClean['date'])
    
    # Nettoyer tasses_cafe (peut être string avec des valeurs comme "3.0")
    dfClean['tasses_cafe'] = pd.to_numeric(dfClean['tasses_cafe'], errors='coerce')
    
    # Supprimer les lignes avec valeurs manquantes
    dfClean = dfClean.dropna()
    
    # Supprimer les valeurs aberrantes
    dfClean = dfClean[(dfClean['tasses_cafe'] >= 0) & 
                      (dfClean['heures_travail'] > 0) & 
                      (dfClean['productivite'] > 0)]
    
    print(f"✓ Nettoyage travail : {len(df)} → {len(dfClean)} lignes conservées")
    
    return dfClean


def filtrerParActivite(dfSport, activite):
    """
    Filtre les données pour une activité spécifique
    
    Args:
        dfSport (pd.DataFrame): DataFrame du sport
        activite (str): Nom de l'activité (course, velo, natation)
    
    Returns:
        pd.DataFrame: DataFrame filtré
    """
    dfFiltre = dfSport[dfSport['activite'] == activite].copy()
    print(f"✓ Filtrage {activite} : {len(dfFiltre)} lignes")
    return dfFiltre


def fusionnerDonnees(dfSport, dfTravail):
    """
    Fusionne les données sport et travail par individu et date
    
    Args:
        dfSport (pd.DataFrame): DataFrame du sport
        dfTravail (pd.DataFrame): DataFrame du travail
    
    Returns:
        pd.DataFrame: DataFrame fusionné
    """
    # Agréger les données sport par individu et date
    dfSportAgg = dfSport.groupby(['individu_id', 'date']).agg({
        'duree': 'sum',
        'calories': 'sum',
        'poids_kg': 'first'
    }).reset_index()
    
    dfSportAgg.columns = ['individu_id', 'date', 'duree_sport', 'calories_sport', 'poids_kg']
    
    # Fusionner
    dfFusion = pd.merge(dfTravail, dfSportAgg, on=['individu_id', 'date'], how='left')
    
    # Remplir les NaN (jours sans sport) par 0
    dfFusion['duree_sport'] = dfFusion['duree_sport'].fillna(0)
    dfFusion['calories_sport'] = dfFusion['calories_sport'].fillna(0)
    
    print(f"✓ Fusion des données : {len(dfFusion)} lignes")
    
    return dfFusion


def ajouterJourPrecedent(dfFusion):
    """
    Ajoute les données du jour précédent pour chaque individu
    
    Args:
        dfFusion (pd.DataFrame): DataFrame fusionné
    
    Returns:
        pd.DataFrame: DataFrame avec colonnes du jour précédent
    """
    df = dfFusion.copy()
    df = df.sort_values(['individu_id', 'date'])
    
    # Ajouter colonnes jour précédent
    df['sport_veille'] = df.groupby('individu_id')['duree_sport'].shift(1)
    df['calories_veille'] = df.groupby('individu_id')['calories_sport'].shift(1)
    
    # Remplir les NaN par 0
    df['sport_veille'] = df['sport_veille'].fillna(0)
    df['calories_veille'] = df['calories_veille'].fillna(0)
    
    return df
