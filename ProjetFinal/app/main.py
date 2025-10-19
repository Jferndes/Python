import pandas as pd
import numpy as np

from src.DataLoader import *
from src.Modelisation import *

if __name__ == "__main__":
    print("="*80)
    print("PROJET FINAL - ANALYSE SPORTIVE ET PRODUCTIVITÉ")
    print("="*80)
    
    # ========== PARTIE 1: DONNÉES SPORT ==========
    cheminCSV = './data/sport_raw.csv'
    dfSport = loadData(cheminCSV)
    
    print('\n' + '='*80)
    print('NETTOYAGE DES DONNÉES SPORT')
    print('='*80)
    dfSport = nettoyageDataSport(dfSport)
    infoDataFrame(dfSport)

    for activite in ['course', 'natation', 'velo']:
        modeliserActiviteSimple(dfSport, activite)
    