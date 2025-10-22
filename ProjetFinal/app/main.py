from src.Controlleur import *


if __name__ == "__main__":
    AnalyseSport()
    AnalyseTravail()








    '''
    # ========== PARTIE 1: DONNÉES SPORT ==========
    cheminCSV = './data/sport_raw.csv'
    dfSport = loadData(cheminCSV)
    
    print('\n' + '='*80)
    print('NETTOYAGE DES DONNÉES SPORT')
    print('='*80)
    dfSport = nettoyageDataSport(dfSport)
    infoDataFrame(dfSport)

    #for activite in ['course', 'natation', 'velo']:
    #    modeliserActiviteSimple(dfSport, activite)

    #for activite in ['course', 'natation', 'velo']:
    #modeliserActiviteMultivariee(dfSport, 'velo')

    # ========== PARTIE 2: DONNÉES PRODUCTIVITÉ ==========
    cheminCSV = './data/travail_raw.csv'
    dfTravail = loadData(cheminCSV)
    print('\n' + '='*80)
    print('NETTOYAGE DES DONNÉES PRODUCTIVITÉ')
    dfTravail = nettoyageDataTravail(dfTravail)
    infoDataFrame(dfTravail)

    modeliserProductiviteSimple(dfTravail)
    modeliserProductiviteQuadra(dfTravail)

    # ========== PARTIE 3: ANALYSE CROISÉE SPORT ET PRODUCTIVITÉ ==========
    print('\n' + '='*80)
    print('ANALYSE CROISÉE: Sport et Productivité')
    print('='*80)

    analyser_sport_cafe_lendemain(dfTravail, dfSport)
    '''