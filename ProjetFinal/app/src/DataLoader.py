import pandas as pd
import numpy as np

'''
Construire un DataFrame à partir d'un fichier CSV
'''
def loadData(cheminCSV: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(cheminCSV)
        print("Données chargées avec succès.")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")
        return None

'''
Information sur un DataFrame
'''
def infoDataFrame(data: pd.DataFrame) -> None:
    print('Info DataFrame:')
    print('Taille:', data.shape)
    print()

    print(data.dtypes.to_frame('dtype'))
    print()

    stats = data.describe()
    print('Statistiques descriptives:')
    print(stats)
    print()


'''
Nettoyer les données du dataframe sport
'''
def nettoyageDataSport(dfSport: pd.DataFrame) -> pd.DataFrame:
    print('### START nettoyageDataSport ###')
    dfClean = dfSport.copy()

    print('tableau des valeurs manquantes avant nettoyage:')
    na_before = dfClean.isna().sum()
    print(na_before.to_frame('NA_avant'))
    print()
    
    # Correction des valeurs manquantes dans la colonne 'poids_kg' par la moyenne
    print(f"Moyenne poids_kg avant nettoyage: {dfClean['poids_kg'].mean()}")
    dfClean['poids_kg'] = dfClean['poids_kg'].transform(lambda s: s.fillna(s.mean()))
    print(f"Moyenne poids_kg après nettoyage: {dfClean['poids_kg'].mean()}")
    print()
    
    dfClean = dfClean.dropna()
    print('tableau des valeurs manquantes après nettoyage:')
    na_after = dfClean.isna().sum()
    print(na_after.to_frame('NA_apres'))
    print()

    # Gestion des dates invalides dans la colonne 'date'
    dfClean['date'] = pd.to_datetime(dfClean['date'], errors='coerce')
    dfClean = dfClean.dropna(subset=['date'])

    # Convertir toutes les durées en minutes
    print('Conversion des durées en minutes:')
    print(dfClean[['duree','unite']].head())
    dfHeures = dfClean['unite'] == 'h'
    dfClean.loc[dfHeures, 'duree'] = dfClean.loc[dfHeures, 'duree'] * 60
    dfClean['unite'] = 'min'
    print('---------------- Après conversion ------------------')
    print(dfClean[['duree','unite']].head())
    print(dfClean['unite'].unique())
    print()

    # Corriger les noms des sports
    print('Correction des noms des sports:')
    print('Avant correction:', dfClean['activite'].unique())
    corrections = {
        'run': 'course',
        'cours': 'course',
        'velò': 'velo'
    }
    dfClean['activite'] = dfClean['activite'].replace(corrections)
    print('Après correction:', dfClean['activite'].unique())
    print()

    print('### END nettoyageDataSport ###')
    print()
    return dfClean


'''
Nettoyer les données du dataframe travail
'''
def nettoyageDataTravail(dfTravail: pd.DataFrame) -> pd.DataFrame:
    print('### START nettoyageDataTravail ###')
    dfClean = dfTravail.copy()

    print('tableau des valeurs manquantes avant nettoyage:')
    na_before = dfClean.isna().sum()
    print(na_before.to_frame('NA_avant'))
    print()
    
    # Correction des valeurs manquantes dans la colonne 'heures_travail' par la moyenne
    print(f"Moyenne heures_travail avant nettoyage: {dfClean['heures_travail'].mean()}")
    dfClean['heures_travail'] = dfClean['heures_travail'].transform(lambda s: s.fillna(s.mean()))
    print(f"Moyenne heures_travail après nettoyage: {dfClean['heures_travail'].mean()}")
    print()
    
    dfClean = dfClean.dropna()
    print('tableau des valeurs manquantes après nettoyage:')
    na_after = dfClean.isna().sum()
    print(na_after.to_frame('NA_apres'))
    print()

    # Gestion des dates invalides dans la colonne 'date'
    dfClean['date'] = pd.to_datetime(dfClean['date'], errors='coerce')
    dfClean = dfClean.dropna(subset=['date'])


    corrections = {
        'deux': '2',
        'trois': '3',
        'cinq': '5'
    }
    print('Correction des valeurs du nombre de tasses de café:')
    print('Avant correction:', dfClean['tasses_cafe'].unique())
    # Remplacer les mots par des chiffres
    dfClean['tasses_cafe'] = dfClean['tasses_cafe'].replace(corrections)
    # Extraire les chiffres par l'expression régulière
    dfClean['tasses_cafe'] = dfClean['tasses_cafe'].str.extract(r'(\d+)')[0]
    # Convertir en entier
    dfClean['tasses_cafe'] = pd.to_numeric(dfClean['tasses_cafe'], errors='coerce').astype('int64')
    print('Après correction:', dfClean['tasses_cafe'].unique())
    print()

    print('### END nettoyageDataTravail ###')
    print()
    return dfClean