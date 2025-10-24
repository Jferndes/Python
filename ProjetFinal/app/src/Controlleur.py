import pandas as pd
import numpy as np
from src.DataLoader import *
from src.Modelisation import *
from src.Visualisation import *

'''
    Analyse des activités sportives
'''
def analyseSport():
    print("### ANALYSE DES ACTIVITÉS SPORTIVES ###\n")
    try:
        dfSport = getSportDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return

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


'''
    Analyse du travail et de la productivité
'''
def analyseTravail():
    print("### ANALYSE DES ACTIVITÉS DE TRAVAIL ###\n")

    try:
        dfTravail = getTravailDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return

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
    tracerPolynome(X, Y, np.array([a, b, c]), "productivite")
    print()


'''
Réponse à la question sur le sport intense et la consommation de café le lendemain
'''
def analyseSportEtCafeLendemain():
    try:
        dfSport = getSportDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return
    
    try:
        dfTravail = getTravailDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return
    
    #Définition du seuil de sport intense
    seuilIntense = dfSport['calories'].quantile(0.75)
    print(seuilIntense)

    #Création d'une colonne pour indiquer si l'activité est intense
    dfSportIntense = dfSport.copy()
    dfSportIntense['sportIntense'] = dfSportIntense['calories'] >= seuilIntense

    # Agrégation des données sportives par individu et par jour
    dfSportJour = dfSportIntense.groupby(['individu_id', 'date']).agg({
        'calories': 'sum',
        'sportIntense': 'max',
        'duree': 'sum'
    }).reset_index()

    # Création d'une colonne date_lendemain pour la jointure
    dfSportJour['date_lendemain'] = dfSportJour['date'] + pd.Timedelta(days=1)

    #Jointure entre sport et travail
    dfMerged = dfSportJour.merge(
        dfTravail[['individu_id', 'date', 'tasses_cafe']],
        left_on=['individu_id', 'date_lendemain'],
        right_on=['individu_id', 'date'],
        suffixes=('_sport', '_travail')
    )
    print(f"\nNombre d'observations avec données sport et café lendemain: {len(dfMerged)}")
    print(dfMerged.head())
    print()

    # Analyse de la corrélation entre calories brûlées et tasses de café le lendemain
    corr_pearson, p_corr = stats.pearsonr(dfMerged['calories'], dfMerged['tasses_cafe'])
    print(f"Corrélation de Pearson: {corr_pearson:.4f}")
    print(f"P-value: {p_corr:.4f}")
    print("Corrélation faible entre calories brûlées et tasses de café le lendemain.")
    print()

    #Analyse avec la méthode student t
    cafeApresIntense = dfMerged[dfMerged['sportIntense'] == True]['tasses_cafe']
    cafeApresNormal = dfMerged[dfMerged['sportIntense'] == False]['tasses_cafe']

    print(f"Après sport INTENSE (n={len(cafeApresIntense)}):")
    print(f"  Moyenne: {cafeApresIntense.mean():.2f} tasses")
    print(f"  Écart-type: {cafeApresIntense.std():.2f}")
    print(f"  Médiane: {cafeApresIntense.median():.2f}")
    print()

    print(f"Après sport NORMAL (n={len(cafeApresNormal)}):")
    print(f"  Moyenne: {cafeApresNormal.mean():.2f} tasses")
    print(f"  Écart-type: {cafeApresNormal.std():.2f}")
    print(f"  Médiane: {cafeApresNormal.median():.2f}")

    diffMoyenne = cafeApresIntense.mean() - cafeApresNormal.mean()
    print(f"Différence de moyenne: {diffMoyenne:.2f} tasses")

    tStat, pValue = stats.ttest_ind(cafeApresIntense, cafeApresNormal)
    print(f"Statistique t: {tStat:.4f}")
    print(f"P-value: {pValue:.4f}")
    print(f"Seuil α: 0.05")
    print("On constate une très légère tendance à boire un peu moins de café le lendemain d’un sport intense, mais cette différence est statistiquement faible et pratiquement négligeable")
    print()


def analyseActifProductivite():
    try:
        dfSport = getSportDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return
    
    try:
        dfTravail = getTravailDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return

    # Calculer le niveau d'activité moyen par individu (calories moyennes par jour)
    dfSport['date'] = pd.to_datetime(dfSport['date'])
    dfActiviteMoyenne = dfSport.groupby('individu_id').agg({
        'calories': 'mean',
        'duree': 'mean'
    }).reset_index()
    dfActiviteMoyenne.columns = ['individu_id', 'caloriesMoyennes', 'dureeMoyenne']
    
    # Calculer la productivité moyenne par individu
    dfProductiviteMoyenne = dfTravail.groupby('individu_id').agg({
        'productivite': 'mean'
    }).reset_index()
    dfProductiviteMoyenne.columns = ['individu_id', 'productiviteMoyenne']
    
    # Fusion des données
    dfMerge = dfActiviteMoyenne.merge(dfProductiviteMoyenne, on='individu_id')
    
    print(f"\nNombre d'individus analysés: {len(dfMerge)}")
    print(f"Calories moyennes: {dfMerge['caloriesMoyennes'].mean():.2f} ± {dfMerge['caloriesMoyennes'].std():.2f}")
    print(f"Productivité moyenne: {dfMerge['productiviteMoyenne'].mean():.2f} ± {dfMerge['productiviteMoyenne'].std():.2f}")
    
    # Corrélation de Pearson
    corrPearson, pValuePearson = stats.pearsonr(dfMerge['caloriesMoyennes'], dfMerge['productiviteMoyenne'])

    print(f"Corrélation de Pearson: {corrPearson:.4f} (p = {pValuePearson:.4f})")


def analyseSurchargeProductivite():
    try:
        dfSport = getSportDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return
    
    try:
        dfTravail = getTravailDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return
    
    
    # Agréger le sport par jour
    dfSportJour = dfSport.groupby(['individu_id', 'date']).agg({
        'calories': 'sum',
        'duree': 'sum'
    }).reset_index()
    
    # Fusion des données
    dfMerge = dfTravail.merge(dfSportJour, on=['individu_id', 'date'], how='inner')
    print(f"\nNombre d'observations: {len(dfMerge)}")
    
    # Définir les seuils "élevés" (75e percentile)
    seuilCafe = dfMerge['tasses_cafe'].quantile(0.75)
    seuilSport = dfMerge['calories'].quantile(0.75)
    
    print(f"\nSeuil café élevé (75e percentile): {seuilCafe:.0f} tasses")
    print(f"Seuil sport élevé (75e percentile): {seuilSport:.2f} calories")
    print()
    
    # Créer les catégories
    dfMerge['cafeEleve'] = dfMerge['tasses_cafe'] >= seuilCafe
    dfMerge['sportEleve'] = dfMerge['calories'] >= seuilSport
    
    # 4 groupes
    groupeNormal = dfMerge[(~dfMerge['cafeEleve']) & (~dfMerge['sportEleve'])]
    groupeCafeSeul = dfMerge[(dfMerge['cafeEleve']) & (~dfMerge['sportEleve'])]
    groupeSportSeul = dfMerge[(~dfMerge['cafeEleve']) & (dfMerge['sportEleve'])]
    groupeDoubleSurcharge = dfMerge[(dfMerge['cafeEleve']) & (dfMerge['sportEleve'])]
    
    print(f"Normal (café normal + sport normal):")
    print(f"    nb elemennts = {len(groupeNormal)}") 
    print(f"    productivite moyenne = {groupeNormal['productivite'].mean():.2f}")
    print(f"Café élevé seul:")
    print(f"    nb elemennts = {len(groupeCafeSeul)}")
    print(f"    productivite moyenne = {groupeCafeSeul['productivite'].mean():.2f}")
    print(f"    soit +{100*(groupeCafeSeul['productivite'].mean() - groupeNormal['productivite'].mean())/groupeNormal['productivite'].mean():.2f}% par rapport au normal")
    print(f"Sport élevé seul:")
    print(f"    nb elemennts = {len(groupeSportSeul)}")
    print(f"    productivite moyenne = {groupeSportSeul['productivite'].mean():.2f}")
    print(f"    soit +{100*(groupeSportSeul['productivite'].mean() - groupeNormal['productivite'].mean())/groupeNormal['productivite'].mean():.2f}% par rapport au normal")
    print(f"Double surcharge (café + sport élevés):")
    print(f"    nb elemennts = {len(groupeDoubleSurcharge)}")
    print(f"    productivite moyenne = {groupeDoubleSurcharge['productivite'].mean():.2f}")
    print(f"    soit +{100*(groupeDoubleSurcharge['productivite'].mean() - groupeNormal['productivite'].mean())/groupeNormal['productivite'].mean():.2f}% par rapport au normal")
    print()

    # Test ANOVA
    fStat, pValueAnova = stats.f_oneway(
        groupeNormal['productivite'],
        groupeCafeSeul['productivite'],
        groupeSportSeul['productivite'],
        groupeDoubleSurcharge['productivite']
    )
    
    print("Résultats du test ANOVA:")
    print(f"F-statistique: {fStat:.4f}")
    print(f"P-value: {pValueAnova:.4f}")
    print()
    
    # Comparaison entre double surcharge et groupe normal
    tStat, pValueT = stats.ttest_ind(groupeDoubleSurcharge['productivite'], groupeNormal['productivite'])
    diffMoyenne = groupeDoubleSurcharge['productivite'].mean() - groupeNormal['productivite'].mean()
    print("Résultats du test t:")
    print(f"Différence de productivité: {diffMoyenne:.2f}")
    print(f"T-statistique: {tStat:.4f}")
    print(f"P-value: {pValueT:.4f}")
    print()

    print("Conclusion:")
    print("La double surcharge (café élevé + sport élevé) ne baisse pas la productivité par rapport au groupe normal.\nOn observe que c'est surtout la forte consomation de café qui augmente la productivité.")


def analyserEquilibreTempsProductivite():
    try:
        dfSport = getSportDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return
    
    try:
        dfTravail = getTravailDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return
    
    
    # Convertir durée sport en heures
    dfSportJour = dfSport.groupby(['individu_id', 'date']).agg({
        'duree': 'sum'
    }).reset_index()
    dfSportJour['heures_sport'] = dfSportJour['duree'] / 60.0
    
    # Fusion
    dfMerge = dfTravail.merge(dfSportJour[['individu_id', 'date', 'heures_sport']], 
                              on=['individu_id', 'date'], how='left')
    dfMerge['heures_sport'] = dfMerge['heures_sport'].fillna(0)
    
    # Calculer le temps total
    dfMerge['tempsTotal'] = dfMerge['heures_travail'] + dfMerge['heures_sport']
    
    print(f"Nombre d'observations: {len(dfMerge)}")
    print(f"Temps total moyen: {dfMerge['tempsTotal'].mean():.2f}h ± {dfMerge['tempsTotal'].std():.2f}h")
    print(f"  - Heures de travail: {dfMerge['heures_travail'].mean():.2f}h ± {dfMerge['heures_travail'].std():.2f}h")
    print(f"  - Heures de sport: {dfMerge['heures_sport'].mean():.2f}h ± {dfMerge['heures_sport'].std():.2f}h")
    
    # Corrélation linéaire
    corrLineaire, pValueLineaire = stats.pearsonr(dfMerge['tempsTotal'], dfMerge['productivite'])
    print(f"Corrélation de Pearson: {corrLineaire:.4f} (p = {pValueLineaire:.4f})")
    print()
    
    # Régression polynomiale (degré 2) pour détecter un optimum
    coeffs = np.polyfit(dfMerge['tempsTotal'], dfMerge['productivite'], 2)
    a, b, c = coeffs
    
    print(f"Équation: y = {a:.4f}x² + {b:.4f}x + {c:.4f}")
    
    # Calculer R²
    yPred = np.polyval(coeffs, dfMerge['tempsTotal'])
    r2 = 1 - (np.sum((dfMerge['productivite'] - yPred)**2) / 
              np.sum((dfMerge['productivite'] - dfMerge['productivite'].mean())**2))
    print(f"R²: {r2:.4f}")
    print()
    
    # Point optimal (si parabole concave, a < 0)
    if a < 0:
        tempsOptimal = -b / (2 * a)
        productiviteOptimale = np.polyval(coeffs, tempsOptimal)
        print(f"Optimum détecté (parabole concave):")
        print(f"  Temps total optimal: {tempsOptimal:.2f} heures")
        print(f"  Productivité maximale: {productiviteOptimale:.2f}")

        tracerPolynome(dfMerge['productivite'],dfMerge['tempsTotal'], coeffs, "equilibre", show=True)
    else:
        tempsOptimal = None
        productiviteOptimale = None
        print("Pas d'optimum (parabole convexe, a > 0)")
    
    return {
        'dfMerge': dfMerge,
        'corrLineaire': corrLineaire,
        'pValueLineaire': pValueLineaire,
        'coeffsPolynome': coeffs,
        'r2': r2,
        'tempsOptimal': tempsOptimal,
        'productiviteOptimale': productiviteOptimale
    }