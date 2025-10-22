import pandas as pd

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
def nettoyageDataSport(dfSport: pd.DataFrame, debug: bool = False) -> pd.DataFrame:
    if debug: print('### START nettoyageDataSport ###')
    if dfSport is None:
        print("Erreur: DataFrame est None, impossible de nettoyer les données.")
        return None
    dfClean = dfSport.copy()

    if debug: print('tableau des valeurs manquantes avant nettoyage:')
    na_before = dfClean.isna().sum()
    if debug: print(na_before.to_frame('NA_avant'))
    if debug: print()
    
    # Correction des valeurs manquantes dans la colonne 'poids_kg' par la moyenne
    if debug: print(f"Moyenne poids_kg avant nettoyage: {dfClean['poids_kg'].mean()}")
    dfClean['poids_kg'] = dfClean['poids_kg'].transform(lambda s: s.fillna(s.mean()))
    if debug: print(f"Moyenne poids_kg après nettoyage: {dfClean['poids_kg'].mean()}")
    if debug: print()
    
    dfClean = dfClean.dropna()
    if debug:print('tableau des valeurs manquantes après nettoyage:')
    na_after = dfClean.isna().sum()
    if debug: print(na_after.to_frame('NA_apres'))
    if debug: print()

    # Gestion des dates invalides dans la colonne 'date'
    dfClean['date'] = pd.to_datetime(dfClean['date'], errors='coerce')
    dfClean = dfClean.dropna(subset=['date'])

    # Convertir toutes les durées en minutes
    if debug: print('Conversion des durées en minutes:')
    if debug: print(dfClean[['duree','unite']].head())
    dfHeures = dfClean['unite'] == 'h'
    dfClean.loc[dfHeures, 'duree'] = dfClean.loc[dfHeures, 'duree'] * 60
    dfClean['unite'] = 'min'
    if debug: print('---------------- Après conversion ------------------')
    if debug: print(dfClean[['duree','unite']].head())
    if debug: print(dfClean['unite'].unique())
    if debug: print()

    # Corriger les noms des sports
    if debug: print('Correction des noms des sports:')
    if debug: print('Avant correction:', dfClean['activite'].unique())
    corrections = {
        'run': 'course',
        'cours': 'course',
        'velò': 'velo'
    }
    dfClean['activite'] = dfClean['activite'].replace(corrections)
    if debug: print('Après correction:', dfClean['activite'].unique())
    if debug: print()

    print('Données sport nettoyées avec succès.\n')
    return dfClean


'''
Nettoyer les données du dataframe travail
'''
def nettoyageDataTravail(dfTravail: pd.DataFrame, debug: bool = False) -> pd.DataFrame:
    if debug: print('### START nettoyageDataTravail ###')
    if dfTravail is None:
        print("Erreur: DataFrame est None, impossible de nettoyer les données.")
        return None
    dfClean = dfTravail.copy()

    if debug: print('tableau des valeurs manquantes avant nettoyage:')
    na_before = dfClean.isna().sum()
    if debug: print(na_before.to_frame('NA_avant'))
    if debug: print()
    
    # Correction des valeurs manquantes dans la colonne 'heures_travail' par la moyenne
    if debug: print(f"Moyenne heures_travail avant nettoyage: {dfClean['heures_travail'].mean()}")
    dfClean['heures_travail'] = dfClean['heures_travail'].transform(lambda s: s.fillna(s.mean()))
    if debug: print(f"Moyenne heures_travail après nettoyage: {dfClean['heures_travail'].mean()}")
    if debug: print()

    dfClean = dfClean.dropna()
    if debug: print('tableau des valeurs manquantes après nettoyage:')
    na_after = dfClean.isna().sum()
    if debug: print(na_after.to_frame('NA_apres'))
    if debug: print()

    # Gestion des dates invalides dans la colonne 'date'
    dfClean['date'] = pd.to_datetime(dfClean['date'], errors='coerce')
    dfClean = dfClean.dropna(subset=['date'])


    corrections = {
        'deux': '2',
        'trois': '3',
        'cinq': '5'
    }
    if debug: print('Correction des valeurs du nombre de tasses de café:')
    if debug: print('Avant correction:', dfClean['tasses_cafe'].unique())
    # Remplacer les mots par des chiffres
    dfClean['tasses_cafe'] = dfClean['tasses_cafe'].replace(corrections)
    # Extraire les chiffres par l'expression régulière
    dfClean['tasses_cafe'] = dfClean['tasses_cafe'].str.extract(r'(\d+)')[0]
    # Convertir en entier
    dfClean['tasses_cafe'] = pd.to_numeric(dfClean['tasses_cafe'], errors='coerce').astype('int64')
    if debug: print('Après correction:', dfClean['tasses_cafe'].unique())
    if debug: print()

    print('Données sport nettoyées avec succès.\n')
    return dfClean