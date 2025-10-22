import pandas as pd
import numpy as np
from src.DataLoader import *
from src.Modelisation import *
from src.Visualisation import *

'''
    Analyse des activités sportives
'''
def AnalyseSport():
    print("### ANALYSE DES ACTIVITÉS SPORTIVES ###\n")
    cheminCSV = "./data/sport_raw.csv"
    
    # Chargement des données
    dfSport = loadData(cheminCSV)
    if dfSport is None:
        print("Impossible de continuer : les données n'ont pas pu être chargées.")
        return
    
    # Nettoyage des données
    dfSport = nettoyageDataSport(dfSport)

    # Statistiques descriptives
    #infoDataFrame(dfSport)

    print("Analyse des activités sportives linéaire:")
    for activite in ['course', 'natation', 'velo']:
        # Modélisation par regression linéaire
        res, X, Y = modeliserActiviteLineaire(dfSport, activite)
        slope, intercept, r_value, p_value, std_er = res
        
        # Résultats
        print(f"Activité: {activite} -> y = {slope:.2f}x + {intercept:.2f}")
        print(f"  R² = {r_value**2:.3f}")
        print(f"  p-value: {p_value:.2f}")
        print(f"  Erreur standard: {std_er:.2f} et t = a / std_er = {slope/std_er:.2f}")

        #Visualisation
        tracerRegression(X, Y, slope, intercept, activite)
    print()

    print("Analyse des activités sportives multivariée:")
    for activite in ['course', 'natation', 'velo']:
        # Modélisation par regression linéaire
        res, X1, X2, Y = modeliserActiviteMultivariee(dfSport, activite)
        beta, residuals, rank, s, k, rmse, r2 = res
        a, b, c = beta

        dfSportFiltre = dfSport[dfSport['activite'] == activite]
        calMET = calculerCaloriesMET(activite, 60, 70)
        calModele = calculerCaloriesModele(a, b, c, 60, 70)
        ecartRelatif = 100 * abs(calModele - calMET) / calMET if calMET != 0 else 0.0

        # Résultats
        print(f"Activité: {activite} -> calories = {a:.2f}*duree + {b:.2f}*poids + {c:.2f}")
        print(f"    R²: {r2:.3f})")
        print(f"    Résidus: {residuals}")
        print(f"    Erreur moyenne par prédiction: ±{rmse:.2f} calories soit {100*rmse/dfSportFiltre['calories'].mean():.2f}% d'erreur")
        print(f"    Rang: {rank}")
        print(f"    Singular values: {s}")
        print(f"    Conditionnement (κ): {k:.2f}")
        print(f"    Comparaison MET vs Modèle:")
        print(f"        MET: {calMET:.2f} kcal")
        print(f"        Modèle: {calModele:.2f} kcal")
        print(f"        Ecart relatif: {ecartRelatif:.2f}%")

        #Visualisation
        tracerRegression3D(X1, X2, Y, a, b, c, activite, r2)
    print()

def AnalyseTravail():
    print("### ANALYSE DES ACTIVITÉS DE TRAVAIL ###\n")
    cheminCSV = "./data/travail_raw.csv"
    
    # Chargement des données
    dfTravail = loadData(cheminCSV)
    if dfTravail is None:
        print("Impossible de continuer : les données n'ont pas pu être chargées.")
        return
    
    # Nettoyage des données
    dfTravail = nettoyageDataTravail(dfTravail)

    # Statistiques descriptives
    #infoDataFrame(dfTravail)

    # Modélisation par regression linéaire
    print("Analyse productivité linéaire:")
    res, X, Y = modeliserProductiviteLineaire(dfTravail)
    slope, intercept, r_value, p_value, std_er = res

    # Résultats
    print(f"Productivité: -> y = {slope:.2f}x + {intercept:.2f}")
    print(f"Maximum: Vu que c'est une droite, pas de maximum défini. On doit regarder le polynome degré 2.")
    print(f"  R²: {r_value**2:.3f}")
    print(f"  p-value: {p_value:.2f}")
    print(f"  Erreur standard: {std_er:.2f} et t = a / std_er = {slope/std_er:.2f}")

    #Visualisation
    tracerRegression(X, Y, slope, intercept, "productivité")
    print()

    print("Analyse productivité polynomiale:")
    a, b, c, max, r2 = modeliserProductivitePolynome(dfTravail)
    print(f"Productivité: -> y = {a:.2f}x² + {b:.2f}x + {c:.2f}")
    print(f"  Maximum: {max:.2f} tasses de café")
    print(f"  R²: {r2:.3f}")
    print(f"    Le coefficient a est négatif ({a:.2f}). Cela indique que la productivité augmente jusqu'à un maximum ({max:.2f}), puis diminue.\n    Dans le cas 0-6 tasses, on s'apparente à une droite croissante. Donc plus on boit de café, plus on est productif.")

    #Visualisation
    tracerPolynome(X, Y, np.array([a, b, c]))
    print()

