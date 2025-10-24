import pandas as pd
import numpy as np
from scipy import stats, linalg
import matplotlib.pyplot as plt

MET_VALUES = {
    'course': 9.8,
    'velo': 7.5,
    'natation': 8.0
}

# Conditionnement et RMSE
K = lambda singVal : max(singVal) / min(singVal) if min(singVal) > 0 else 0.0
RMSE = lambda residus, n : np.sqrt(residus / n) if n > 0 else 0.0


'''
    Calcule les calories brûlées pour une activité donnée en utilisant la formule MET.
'''
def calculerCaloriesMET(activite: str, duree: float, poids: float) -> float:
    met = MET_VALUES.get(activite.lower())
    if met is None:
        raise ValueError(f"Activité inconnue: {activite}")

    calories = met * 3.5 * poids / 200 * duree
    return calories

'''
    Calcule les calories brûlées pour une activité donnée en utilisant le modèle.
'''
def calculerCaloriesModele(a, b, c, duree: float, poids: float) -> float:
    return a * duree + b * poids + c

'''
Modelisation par regression linéaire
'''
def modeliserActiviteLineaire(dfSport: pd.DataFrame, activite: str):
    # Filtrer les données pour le type de sport
    dfActivite = dfSport[dfSport['activite'] == activite]
    dfActivite = dfActivite[['calories', 'duree', 'poids_kg']]

    X = dfActivite['duree'].to_numpy(dtype=float)
    Y = dfActivite['calories'].to_numpy(dtype=float)

    # Calcul de la régression linéaire
    res = stats.linregress(X, Y)

    return res, X, Y


'''
Modelisation par moindre carrés
'''
def modeliserActiviteMultivariee(dfSport: pd.DataFrame, activite: str):
    # Filtrer les données pour le type de sport
    dfActivite = dfSport[dfSport['activite'] == activite][['calories', 'duree', 'poids_kg']]

    # Variables explicatives (duree, poids) + biais (constante)
    X1 = dfActivite['duree'].to_numpy(dtype=float)
    X2 = dfActivite['poids_kg'].to_numpy(dtype=float)
    Y = dfActivite['calories'].to_numpy(dtype=float)

    X = np.column_stack([X1, X2, np.ones_like(X1)])

    # Moindres carrés avec scipy : Y = X @ beta -> calories = a*duree + b*poids + c
    #  où beta = (a,b,c), X = (duree, poids, 1) et Y = calories
    beta, residuals, rank, s = linalg.lstsq(X, Y)

    k = K(s)
    rmse = RMSE(residuals, len(dfActivite))

    # R^2
    Y_hat = X @ beta
    ss_res = float(np.sum((Y - Y_hat) ** 2))
    ss_tot = float(np.sum((Y - np.mean(Y)) ** 2))
    r2 = 0.0 if ss_tot == 0 else 1.0 - ss_res / ss_tot

    #tracerRegression3D(X1, X2, Y, a, b, c, activite, r2)
    res = beta, residuals, rank, s, k, rmse, r2
    return res, X1, X2, Y

'''
Modelisation par regression linéaire
'''
def modeliserProductiviteLineaire(dfTravail: pd.DataFrame):
    # Sélection des colonnes
    dfTravail = dfTravail[(dfTravail['tasses_cafe'] >= 0) & (dfTravail['tasses_cafe'] <= 6)][['heures_travail', 'tasses_cafe', 'productivite']]

    X = dfTravail['tasses_cafe'].to_numpy(dtype=int)
    Y = dfTravail['productivite'].to_numpy(dtype=float)

    # Calcul de la régression linéaire
    res = stats.linregress(X, Y)

    return res, X, Y

'''
Modelisation par polynome
'''
def modeliserProductivitePolynome(dfTravail: pd.DataFrame):
    # Sélection des colonnes
    X = dfTravail['tasses_cafe'].to_numpy(dtype=int)
    Y = dfTravail['productivite'].to_numpy(dtype=float)

    # Ajustement polynomial de degré 2
    coeffs = np.polyfit(X, Y, 2)
    a, b, c = coeffs

    # Maximum analytique (pour a < 0)
    max = -b / (2 * a) if a != 0 else 0.0

    #Formule R2
    r2 = 1 - (np.sum((Y - np.polyval(coeffs, X))**2) / np.sum((Y - np.mean(Y))**2))

    return a, b, c, max, r2

'''
Calcul de la corrélation de Pearson entre deux variables
'''
def correlationPearson(x: np.ndarray, y: np.ndarray):
    corr_pearson, p_value = stats.pearsonr(x, y)
    return corr_pearson, p_value

def testStudentT(dfMerged: pd.DataFrame):
    cafeApresIntense = dfMerged[dfMerged['sportIntense'] == True]['tasses_cafe']
    cafeApresNormal = dfMerged[dfMerged['sportIntense'] == False]['tasses_cafe']

    t_stat, p_value = stats.ttest_ind(cafeApresIntense, cafeApresNormal)
    return t_stat, p_value

"""
Analyse la relation entre le sport intense et la consommation de café le lendemain.
"""
def analyseSportEtCafeLendemain(dfTravail: pd.DataFrame, dfSport: pd.DataFrame):
    #Définition du seuil de sport intense
    seuilIntense = dfSport['calories'].quantile(0.75)
    print(seuilIntense)



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

    # Analyse de la corrélation entre calories brûlées et tasses de café le lendemain
    corr_pearson, p_corr = stats.pearsonr(dfMerged['calories'], dfMerged['tasses_cafe'])
    print(f"Corrélation de Pearson: {corr_pearson:.4f}")
    print(f"P-value: {p_corr:.4f}")

    print("Corrélation faible entre calories brûlées et tasses de café le lendemain.")

    #Analyse avec la méthode student t
    cafeApresIntense = dfMerged[dfMerged['sportIntense'] == True]['tasses_cafe']
    cafeApresNormal = dfMerged[dfMerged['sportIntense'] == False]['tasses_cafe']

    print(f"\nAprès sport INTENSE (n={len(cafeApresIntense)}):")
    print(f"  Moyenne: {cafeApresIntense.mean():.2f} tasses")
    print(f"  Écart-type: {cafeApresIntense.std():.2f}")
    print(f"  Médiane: {cafeApresIntense.median():.2f}")

    print(f"\nAprès sport NORMAL (n={len(cafeApresNormal)}):")
    print(f"  Moyenne: {cafeApresNormal.mean():.2f} tasses")
    print(f"  Écart-type: {cafeApresNormal.std():.2f}")
    print(f"  Médiane: {cafeApresNormal.median():.2f}")

    diffMoyenne = cafeApresIntense.mean() - cafeApresNormal.mean()
    print(f"\n➜ Différence de moyenne: {diffMoyenne:.2f} tasses")

    tStat, pValue = stats.ttest_ind(cafeApresIntense, cafeApresNormal)
    print(f"Statistique t: {tStat:.4f}")
    print(f"P-value: {pValue:.4f}")
    print(f"Seuil α: 0.05")
    print()
    