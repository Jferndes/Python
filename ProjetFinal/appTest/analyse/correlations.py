"""
Module pour les analyses de corrélations et questions spécifiques
"""
import numpy as np
import pandas as pd
from analyse.statistiques import calculerCorrelation


def analyserSportIntenseCafe(dfFusion, seuilIntense=60):
    """
    Analyse si les jours de sport intense sont suivis de plus de café
    
    Args:
        dfFusion (pd.DataFrame): DataFrame fusionné avec données veille
        seuilIntense (float): Durée minimale pour sport intense (minutes)
    
    Returns:
        dict: Résultats de l'analyse
    """
    # Identifier les jours avec sport intense la veille
    dfFusion['sportIntenseVeille'] = dfFusion['sport_veille'] >= seuilIntense
    
    # Comparer consommation de café
    cafeApresSportIntense = dfFusion[dfFusion['sportIntenseVeille'] == True]['tasses_cafe'].mean()
    cafeSansSportIntense = dfFusion[dfFusion['sportIntenseVeille'] == False]['tasses_cafe'].mean()
    
    # Test statistique
    from scipy.stats import ttest_ind
    groupe1 = dfFusion[dfFusion['sportIntenseVeille'] == True]['tasses_cafe'].dropna()
    groupe2 = dfFusion[dfFusion['sportIntenseVeille'] == False]['tasses_cafe'].dropna()
    tStat, pValue = ttest_ind(groupe1, groupe2)
    
    return {
        'cafeApresSportIntense': cafeApresSportIntense,
        'cafeSansSportIntense': cafeSansSportIntense,
        'difference': cafeApresSportIntense - cafeSansSportIntense,
        'pValue': pValue,
        'significatif': pValue < 0.05
    }


def analyserActifProductif(dfFusion, seuilActif=30):
    """
    Analyse si les individus actifs sont plus productifs
    
    Args:
        dfFusion (pd.DataFrame): DataFrame fusionné
        seuilActif (float): Durée moyenne minimale pour être considéré actif
    
    Returns:
        dict: Résultats de l'analyse
    """
    # Calculer durée moyenne de sport par individu
    sportMoyenParIndividu = dfFusion.groupby('individu_id')['duree_sport'].mean()
    
    # Classifier actifs vs sédentaires
    dfFusion['estActif'] = dfFusion['individu_id'].map(
        lambda x: sportMoyenParIndividu[x] >= seuilActif
    )
    
    # Comparer productivité
    prodActifs = dfFusion[dfFusion['estActif'] == True]['productivite'].mean()
    prodSedentaires = dfFusion[dfFusion['estActif'] == False]['productivite'].mean()
    
    # Corrélation durée sport vs productivité
    corr, pValue = calculerCorrelation(
        dfFusion['duree_sport'].values,
        dfFusion['productivite'].values
    )
    
    return {
        'productiviteActifs': prodActifs,
        'productiviteSedentaires': prodSedentaires,
        'difference': prodActifs - prodSedentaires,
        'correlation': corr,
        'pValue': pValue,
        'significatif': pValue < 0.05
    }


def analyserExcesCafeSport(dfFusion, seuilCafe=6, seuilSport=90):
    """
    Analyse si trop de café et trop de sport diminuent la productivité
    
    Args:
        dfFusion (pd.DataFrame): DataFrame fusionné
        seuilCafe (float): Seuil de café excessif
        seuilSport (float): Seuil de sport excessif (minutes)
    
    Returns:
        dict: Résultats de l'analyse
    """
    # Créer groupes
    dfFusion['tropCafe'] = dfFusion['tasses_cafe'] > seuilCafe
    dfFusion['tropSport'] = dfFusion['duree_sport'] > seuilSport
    dfFusion['excesBoth'] = dfFusion['tropCafe'] & dfFusion['tropSport']
    
    # Comparer productivité
    prodExces = dfFusion[dfFusion['excesBoth'] == True]['productivite'].mean()
    prodNormal = dfFusion[dfFusion['excesBoth'] == False]['productivite'].mean()
    
    return {
        'productiviteExces': prodExces,
        'productiviteNormal': prodNormal,
        'difference': prodExces - prodNormal,
        'baisse': prodExces < prodNormal,
        'nbObservationsExces': dfFusion['excesBoth'].sum()
    }


def analyserEquilibreTempsTravailSport(dfFusion):
    """
    Analyse l'équilibre entre heures de travail + sport et productivité
    
    Args:
        dfFusion (pd.DataFrame): DataFrame fusionné
    
    Returns:
        dict: Résultats de l'analyse
    """
    # Créer variable temps total (heures_travail + duree_sport en heures)
    dfFusion['tempsTotal'] = dfFusion['heures_travail'] + dfFusion['duree_sport'] / 60
    
    # Corrélation avec productivité
    corr, pValue = calculerCorrelation(
        dfFusion['tempsTotal'].values,
        dfFusion['productivite'].values
    )
    
    # Trouver le temps optimal (déciles)
    dfFusion['decileTemps'] = pd.qcut(dfFusion['tempsTotal'], q=10, labels=False, duplicates='drop')
    prodParDecile = dfFusion.groupby('decileTemps')['productivite'].mean()
    
    decileOptimal = prodParDecile.idxmax()
    tempsOptimal = dfFusion[dfFusion['decileTemps'] == decileOptimal]['tempsTotal'].mean()
    
    return {
        'correlation': corr,
        'pValue': pValue,
        'tempsOptimal': tempsOptimal,
        'productiviteMax': prodParDecile.max(),
        'prodParDecile': prodParDecile.to_dict()
    }


def analyserCorrelationCaloriesCafe(dfFusion):
    """
    Analyse la corrélation entre calories brûlées et café consommé
    
    Args:
        dfFusion (pd.DataFrame): DataFrame fusionné
    
    Returns:
        dict: Résultats de l'analyse
    """
    corr, pValue = calculerCorrelation(
        dfFusion['calories_sport'].values,
        dfFusion['tasses_cafe'].values
    )
    
    return {
        'correlation': corr,
        'pValue': pValue,
        'significatif': pValue < 0.05
    }


def analyserSportifsConsommentPlusCafe(dfFusion):
    """
    Analyse si les individus sportifs consomment plus de café en moyenne
    
    Args:
        dfFusion (pd.DataFrame): DataFrame fusionné
    
    Returns:
        dict: Résultats de l'analyse
    """
    # Moyennes par individu
    moyennesIndividu = dfFusion.groupby('individu_id').agg({
        'duree_sport': 'mean',
        'tasses_cafe': 'mean'
    }).reset_index()
    
    # Corrélation
    corr, pValue = calculerCorrelation(
        moyennesIndividu['duree_sport'].values,
        moyennesIndividu['tasses_cafe'].values
    )
    
    # Comparer quartiles
    moyennesIndividu['quartileSport'] = pd.qcut(
        moyennesIndividu['duree_sport'], 
        q=4, 
        labels=['Q1', 'Q2', 'Q3', 'Q4'],
        duplicates='drop'
    )
    cafeParQuartile = moyennesIndividu.groupby('quartileSport')['tasses_cafe'].mean()
    
    return {
        'correlation': corr,
        'pValue': pValue,
        'significatif': pValue < 0.05,
        'cafeParQuartile': cafeParQuartile.to_dict()
    }
