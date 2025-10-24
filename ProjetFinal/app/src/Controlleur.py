import pandas as pd
import numpy as np
from src.DataLoader import *
from src.Modelisation import *
from src.Visualisation import *

'''
    Analyse des activités sportives
'''
def analyseSportLineaire():
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
        
        res["lineaire"]["activite"].append(activite)
        #Visualisation
        tracerRegression(X, Y, slope, intercept, activite)
    print()

    res = {
        "activite": [
            "nom",
            "slope",
            "intercept",
            "r2",
            "p_value",
            "std_error"
        ]
    }
    return res

def analyseSportMultivariee():
    try:
        dfSport = getSportDF()
    except Exception as e:
        print(f"Impossible de continuer : les données n'ont pas pu être chargées. Erreur: {e}")
        return

    resultats = []
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

        resActivite = {
            "activite": activite,
            "coefficients": {
                "a": a,
                "b": b,
                "c": c
            },
            "stats": {
                "rang": rank,
                "residus": residuals,
                "s": s.tolist(),
                "k": k,
                "r2": r2,
                "rmse": rmse,
            },
            "comparaison": {
                "calories_MET": calMET,
                "calories_modele": calModele,
                "ecartRelatif": ecartRelatif
            }
        }
        resultats.append(resActivite)

        #Visualisation
        tracerRegression3D(X1, X2, Y, a, b, c, activite, r2)
    print()

    return resultats
            


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
    tracerRegression(X, Y, slope, intercept, "productivite")
    print()

    print("Analyse productivité polynomiale:")
    a, b, c, max, r2 = modeliserProductivitePolynome(dfTravail)
    print(f"Productivité: -> y = {a:.2f}x² + {b:.2f}x + {c:.2f}")
    print(f"  Maximum: {max:.2f} tasses de café")
    print(f"  R²: {r2:.3f}")
    print()
    
    conclusion = f"Le coefficient a est négatif ({a:.2f}). Cela indique que la productivité augmente jusqu'à un maximum ({max:.2f}), puis diminue.\n    Dans le cas 0-6 tasses, on s'apparente à une droite croissante. Donc plus on boit de café, plus on est productif."
    print(conclusion)
    print()

    #Visualisation
    tracerPolynome(X, Y, np.array([a, b, c]))
    print()

    res = {
        "lineaire": {
            "slope": slope,
            "intercept": intercept,
            "r2": r_value**2,
            "p_value": p_value,
            "std_error": std_er
        },
        "polynome": {
            "coefficients": {
                "a": a,
                "b": b,
                "c": c
            },
            "r2": r2,
            "maximum": max
        },
        "conclusion": conclusion
    }
    return res


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
    conclusion = "On constate une tres legere tendance a boire un peu moins de cafe le lendemain d un sport intense, mais cette difference est statistiquement faible et pratiquement negligeable"
    print(f"Statistique t: {tStat:.4f}")
    print(f"P-value: {pValue:.4f}")
    print(f"Seuil α: 0.05")
    print(conclusion)
    print()

    #json réponse
    res = {
        "conclusion": conclusion,
        "corr": {
            "corr_pearson": corr_pearson,
            "p_value": p_corr
        },
        "ttest": {
            "diff_moyenne": diffMoyenne,
            "t_stat": tStat,
            "p_value": pValue
        },
        "stats":[
            {
                "type": "intense",
                "n": len(cafeApresIntense),
                "moyenne": cafeApresIntense.mean(),
                "std": cafeApresIntense.std(),
                "mediane": cafeApresIntense.median()
            },
            {
                "type": "normal",
                "n": len(cafeApresNormal),
                "moyenne": cafeApresNormal.mean(),
                "std": cafeApresNormal.std(),
                "mediane": cafeApresNormal.median()
            }
        ]
    }

    return res


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
    conclusion = "Il ne semble pas y avoir de corrélation entre le niveau d'activité moyen et la productivité moyenne."
    print(conclusion)

    #json réponse
    res = {
        "n": len(dfMerge),
        "calories_moyennes": {
            "moyenne": dfMerge['caloriesMoyennes'].mean(),
            "std": dfMerge['caloriesMoyennes'].std()
        },
        "productivite_moyenne": {
            "moyenne": dfMerge['productiviteMoyenne'].mean(),
            "std": dfMerge['productiviteMoyenne'].std()
        },
        "conclusion": conclusion,
        "corr": {
            "corr_pearson": corrPearson,
            "p_value": pValuePearson
        }
    }

    return res


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

    ecartRelatif = lambda x, y: 100 * (x - y) / y if y != 0 else 0.0
    ecartGroupeCafeSeul = ecartRelatif(groupeCafeSeul['productivite'].mean(), groupeNormal['productivite'].mean())
    ecartGroupeSportSeul = ecartRelatif(groupeSportSeul['productivite'].mean(), groupeNormal['productivite'].mean())
    ecartGroupeDoubleSurcharge = ecartRelatif(groupeDoubleSurcharge['productivite'].mean(), groupeNormal['productivite'].mean())
    
    print(f"Normal (café normal + sport normal):")
    print(f"    nb elemennts = {len(groupeNormal)}") 
    print(f"    productivite moyenne = {groupeNormal['productivite'].mean():.2f}")
    print(f"Café élevé seul:")
    print(f"    nb elemennts = {len(groupeCafeSeul)}")
    print(f"    productivite moyenne = {groupeCafeSeul['productivite'].mean():.2f}")
    print(f"    soit +{ecartGroupeCafeSeul:.2f}% par rapport au normal")
    print(f"Sport élevé seul:")
    print(f"    nb elemennts = {len(groupeSportSeul)}")
    print(f"    productivite moyenne = {groupeSportSeul['productivite'].mean():.2f}")
    print(f"    soit +{ecartGroupeSportSeul:.2f}% par rapport au normal")
    print(f"Double surcharge (café + sport élevés):")
    print(f"    nb elemennts = {len(groupeDoubleSurcharge)}")
    print(f"    productivite moyenne = {groupeDoubleSurcharge['productivite'].mean():.2f}")
    print(f"    soit +{ecartGroupeDoubleSurcharge:.2f}% par rapport au normal")
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

    conclusion = "La double surcharge (café élevé + sport élevé) ne baisse pas la productivité par rapport au groupe normal.\nOn observe que c'est surtout la forte consomation de café qui augmente la productivité."
    print("Conclusion:")
    print(conclusion)

    res = {
        "anova": {
            "f_stat": fStat,
            "p_value": pValueAnova
        },
        "ttest": {
            "t_stat": tStat,
            "p_value": pValueT,
            "diff_moyenne": diffMoyenne
        },
        "stats": [
            {
                "groupe": "normal",
                "productivite_moyenne": groupeNormal['productivite'].mean(),
                "nb_elements": len(groupeNormal),
                "ecart_relatif": 0.0
            },
            {
                "groupe": "cafe_eleve",
                "productivite_moyenne": groupeCafeSeul['productivite'].mean(),
                "nb_elements": len(groupeCafeSeul),
                "ecart_relatif": ecartGroupeCafeSeul

            },
            {
                "groupe": "sport_eleve",
                "productivite_moyenne": groupeSportSeul['productivite'].mean(),
                "nb_elements": len(groupeSportSeul),
                "ecart_relatif": ecartGroupeSportSeul
            },
            {
                "groupe": "double_surcharge",
                "productivite_moyenne": groupeDoubleSurcharge['productivite'].mean(),
                "nb_elements": len(groupeDoubleSurcharge),
                "ecart_relatif": ecartGroupeDoubleSurcharge
            }
        ],
        "conclusion": conclusion
    }

    return res


def analyseEquilibreTempsProductivite():
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
    print()

    # Corrélation linéaire
    corrLineaire, pValueLineaire = stats.pearsonr(dfMerge['tempsTotal'], dfMerge['productivite'])
    print(f"Corrélation de Pearson: {corrLineaire:.4f} (p = {pValueLineaire:.4f})")
    conclusion = "Il ne semble pas y avoir de corrélation linéaire significative entre le temps total et la productivité."
    print(conclusion)
    print()

    res = {
        "n": len(dfMerge),
        "temps_total_moyen": {
            "moyenne": dfMerge['tempsTotal'].mean(),
            "std": dfMerge['tempsTotal'].std()
        },
        "corr": {
            "corr_pearson": corrLineaire,
            "p_value": pValueLineaire
        },
        "conclusion": conclusion
    }

    return res


def analyseCorrelationCaloriesCafe():
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
        'calories': 'sum'
    }).reset_index()
    
    # Fusion
    dfMerge = dfTravail.merge(dfSportJour, on=['individu_id', 'date'], how='inner')
    
    print(f"\nNombre d'observations: {len(dfMerge)}")
    print(f"Calories moyennes: {dfMerge['calories'].mean():.2f} kcal")
    print(f"Tasses de café moyennes: {dfMerge['tasses_cafe'].mean():.2f}")
    
    # Corrélation de Pearson
    corrPearson, pValuePearson = stats.pearsonr(dfMerge['calories'], dfMerge['tasses_cafe'])
    
    print(f"Corrélation de Pearson: {corrPearson:.4f} (p = {pValuePearson:.4f})")
    conclusion = "Il n'y a pas de corrélation significative entre les calories brûlées et la consommation de café."
    print(conclusion)
    print()

    res = {
        "n": len(dfMerge),
        "calories_moyennes": dfMerge['calories'].mean(),
        "tasses_cafe_moyennes": dfMerge['tasses_cafe'].mean(),
        "conclusion": conclusion,
        "corr": {
            "corr_pearson": corrPearson,
            "p_value": pValuePearson
        }
    }
    return res


def analyseeSportifsConsommationCafe():
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

    # Calculer le niveau sportif par individu (calories totales)
    niveauSportif = dfSport.groupby('individu_id').agg({
        'calories': 'sum',
        'duree': 'sum'
    }).reset_index()
    niveauSportif.columns = ['individu_id', 'caloriesTotal', 'dureeTotal']
    
    # Calculer la consommation de café par individu
    consommationCafe = dfTravail.groupby('individu_id').agg({
        'tasses_cafe': 'mean'
    }).reset_index()
    consommationCafe.columns = ['individu_id', 'cafeMoyen']
    
    # Fusion
    dfMerge = niveauSportif.merge(consommationCafe, on='individu_id')
    
    print(f"Nombre d'individus: {len(dfMerge)}")
    
    # Séparer en 3 groupes (tertiles)
    tertile1 = dfMerge['dureeTotal'].quantile(0.33)
    tertile2 = dfMerge['dureeTotal'].quantile(0.66)

    print(f"Seuils de catégorisation:")
    print(f"  Peu sportif: < {tertile1:.0f} min total")
    print(f"  Moyennement sportif: {tertile1:.0f} - {tertile2:.0f} min")
    print(f"  Très sportif: > {tertile2:.0f} min")
    print()

    # Créer les groupes
    groupePeuSportif = dfMerge[dfMerge['dureeTotal'] < tertile1]
    groupeMoyennement = dfMerge[(dfMerge['dureeTotal'] >= tertile1) & (dfMerge['dureeTotal'] < tertile2)]
    groupeTresSportif = dfMerge[dfMerge['dureeTotal'] >= tertile2]

    print(f"Peu sportif (n={len(groupePeuSportif)}):")
    print(f"  Café moyen: {groupePeuSportif['cafeMoyen'].mean():.2f} tasses")
    print(f"  Écart-type: {groupePeuSportif['cafeMoyen'].std():.2f}")
    
    print(f"\nMoyennement sportif (n={len(groupeMoyennement)}):")
    print(f"  Café moyen: {groupeMoyennement['cafeMoyen'].mean():.2f} tasses")
    print(f"  Écart-type: {groupeMoyennement['cafeMoyen'].std():.2f}")
    
    print(f"\nTrès sportif (n={len(groupeTresSportif)}):")
    print(f"  Café moyen: {groupeTresSportif['cafeMoyen'].mean():.2f} tasses")
    print(f"  Écart-type: {groupeTresSportif['cafeMoyen'].std():.2f}")
    print()
    
    # Test ANOVA
    fStat, pValueAnova = stats.f_oneway(
        groupePeuSportif['cafeMoyen'],
        groupeMoyennement['cafeMoyen'],
        groupeTresSportif['cafeMoyen']
    )
    
    print(f"F-statistique: {fStat:.4f}")
    print(f"P-value: {pValueAnova:.4f}")
    print("Différence entre les groupes (p < 0.05)")
    print()

    # Comparaison directe: Très sportif vs Peu sportif
    tStat, pValueT = stats.ttest_ind(groupeTresSportif['cafeMoyen'], groupePeuSportif['cafeMoyen'])
    diffMoyenne = groupeTresSportif['cafeMoyen'].mean() - groupePeuSportif['cafeMoyen'].mean()
    
    print(f"Différence de consommation: {diffMoyenne:.2f} tasses")
    print(f"T-statistique: {tStat:.4f}")
    print(f"P-value: {pValueT:.4f}")
    print()
    
    # Corrélation globale
    corrPearson, pValueCorr = stats.pearsonr(dfMerge['caloriesTotal'], dfMerge['cafeMoyen'])
    print(f"Corrélation de Pearson: {corrPearson:.4f} (p = {pValueCorr:.4f})")
    conclusion = "Les individus très sportifs ont une consommation de café quasiment égale à celle des individus peu sportifs."
    print(f"Conclusion: {conclusion}")
    print()

    res = {
        "conclusion": conclusion,
        "anova": {
            "f_stat": fStat,
            "p_value": pValueAnova
        },
        "ttest": {
            "diff_moyenne": diffMoyenne,
            "t_stat": tStat,
            "p_value": pValueT
        },
        "corr": {
            "corr_pearson": corrPearson,
            "p_value": pValueCorr
        },
        "stats": [
            {
                "groupe": "peu_sportif",
                "n": len(groupePeuSportif),
                "cafe_moyen": groupePeuSportif['cafeMoyen'].mean(),
                "std": groupePeuSportif['cafeMoyen'].std()
            },
            {
                "groupe": "moyennement_sportif",
                "n": len(groupeMoyennement),
                "cafe_moyen": groupeMoyennement['cafeMoyen'].mean(),
                "std": groupeMoyennement['cafeMoyen'].std()
            },
            {
                "groupe": "tres_sportif",
                "n": len(groupeTresSportif),
                "cafe_moyen": groupeTresSportif['cafeMoyen'].mean(),
                "std": groupeTresSportif['cafeMoyen'].std()
            }
        ]
    }

    return res