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


def calculerCaloriesModele(a, b, c, duree: float, poids: float) -> float:
    return a * duree + b * poids + c


def modeliserActiviteLineaire(dfSport: pd.DataFrame, activite: str):
    # Filtrer les données pour le type de sport
    dfActivite = dfSport[dfSport['activite'] == activite]
    dfActivite = dfActivite[['calories', 'duree', 'poids_kg']]

    X = dfActivite['duree'].to_numpy(dtype=float)
    Y = dfActivite['calories'].to_numpy(dtype=float)

    # Calcul de la régression linéaire
    res = stats.linregress(X, Y)

    return res, X, Y


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


def modeliserProductiviteLineaire(dfTravail: pd.DataFrame) -> None:
    # Sélection des colonnes
    dfTravail = dfTravail[(dfTravail['tasses_cafe'] >= 0) & (dfTravail['tasses_cafe'] <= 6)][['heures_travail', 'tasses_cafe', 'productivite']]

    X = dfTravail['tasses_cafe'].to_numpy(dtype=int)
    Y = dfTravail['productivite'].to_numpy(dtype=float)

    # Calcul de la régression linéaire
    res = stats.linregress(X, Y)

    return res, X, Y


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

def tracerRegressionQuadratique(X: np.ndarray, Y: np.ndarray, a: float, b: float, c: float) -> None:
    # Tracer la courbe
    plt.figure(figsize=(10, 6))
    plt.scatter(X, Y, color='blue', label='Données observées', alpha=0.5)
    x_s = np.linspace(X.min(), X.max(), 100)
    y_s = a * x_s**2 + b * x_s + c
    plt.plot(x_s, y_s, 'r', label='Régression quadratique \n y = {:.2f}x² + {:.2f}x + {:.2f}'.format(a, b, c))
    plt.xlabel('Tasses de café')
    plt.ylabel('Productivité')
    plt.title('Régression quadratique de la productivité en fonction des tasses de café')
    plt.legend()
    plt.grid(True, alpha=0.3)
    #plt.savefig(f'../app/resultats/RegressionQuadratique_productivite.png', dpi=300, bbox_inches='tight')
    plt.show()


def analyser_sport_cafe_lendemain(dfTravail: pd.DataFrame, dfSport: pd.DataFrame) -> pd.DataFrame:
    """
    Analyse la relation entre le sport intense et la consommation de café le lendemain.
    """
    print("="*80)
    print("ANALYSE: Sport Intense et Consommation de Café le Lendemain")
    print("="*80)
    
    print(f"\nNombre d'observations sport: {len(dfSport)}")
    print(f"Nombre d'observations travail: {len(dfTravail)}")
    
    # Définition du sport "intense" basé sur les calories brûlées
    # On calcule le seuil du 75e percentile (quartile supérieur)
    seuil_intense = dfSport['calories'].quantile(0.75)
    print(f"\nSeuil de sport intense (75e percentile): {seuil_intense:.2f} calories")
    
    # Identifier les jours de sport intense par individu
    dfSport['sport_intense'] = dfSport['calories'] >= seuil_intense
    
    # Agréger par individu et date: maximum de calories et indicateur de sport intense
    dfSportJour = dfSport.groupby(['individu_id', 'date']).agg({
        'calories': 'sum',
        'sport_intense': 'max',  # True si au moins une séance intense
        'duree': 'sum'
    }).reset_index()
    
    print(f"\nNombre de jours avec sport: {len(dfSportJour)}")
    print(f"Nombre de jours avec sport intense: {dfSportJour['sport_intense'].sum()}")
    
    # Créer une colonne "date_lendemain" pour faire la jointure
    dfSportJour['date_lendemain'] = dfSportJour['date'] + pd.Timedelta(days=1)

    print(dfSportJour.head())
    
    # Jointure: sport du jour J avec café du jour J+1
    dfMerged = dfSportJour.merge(
        dfTravail[['individu_id', 'date', 'tasses_cafe']],
        left_on=['individu_id', 'date_lendemain'],
        right_on=['individu_id', 'date'],
        suffixes=('_sport', '_travail')
    )
    
    print(f"\nNombre d'observations avec données sport et café lendemain: {len(dfMerged)}")
    print(dfMerged.head())
    
    if len(dfMerged) == 0:
        print("Aucune correspondance trouvée entre les jours de sport et le lendemain!")
        return
    
    # Séparation des données
    cafe_apres_intense = dfMerged[dfMerged['sport_intense'] == True]['tasses_cafe']
    cafe_apres_normal = dfMerged[dfMerged['sport_intense'] == False]['tasses_cafe']
    
    print("\n" + "="*80)
    print("RÉSULTATS STATISTIQUES")
    print("="*80)
    
    # Statistiques descriptives
    print("\nAprès sport INTENSE:")
    print(f"  Nombre d'observations: {len(cafe_apres_intense)}")
    print(f"  Moyenne de tasses de café: {cafe_apres_intense.mean():.2f}")
    print(f"  Écart-type: {cafe_apres_intense.std():.2f}")
    print(f"  Médiane: {cafe_apres_intense.median():.2f}")
    
    print("\nAprès sport NORMAL:")
    print(f"  Nombre d'observations: {len(cafe_apres_normal)}")
    print(f"  Moyenne de tasses de café: {cafe_apres_normal.mean():.2f}")
    print(f"  Écart-type: {cafe_apres_normal.std():.2f}")
    print(f"  Médiane: {cafe_apres_normal.median():.2f}")
    
    diff_moyenne = cafe_apres_intense.mean() - cafe_apres_normal.mean()
    print(f"\nDifférence de moyenne: {diff_moyenne:.2f} tasses")
    
    # Test statistique: Test t de Student pour échantillons indépendants
    print("\n" + "-"*80)
    print("TEST STATISTIQUE (Test t de Student)")
    print("-"*80)
    
    t_stat, p_value = stats.ttest_ind(cafe_apres_intense, cafe_apres_normal)
    
    print(f"Statistique t: {t_stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Seuil de significativité (α): 0.05")
    
    if p_value < 0.05:
        print(f"\n✓ CONCLUSION: Différence SIGNIFICATIVE (p < 0.05)")
        if diff_moyenne > 0:
            print("  → Les individus boivent PLUS de café le lendemain d'un sport intense.")
        else:
            print("  → Les individus boivent MOINS de café le lendemain d'un sport intense.")
    else:
        print(f"\n✗ CONCLUSION: Différence NON significative (p ≥ 0.05)")
        print("  → Pas de preuve d'une différence dans la consommation de café.")
    
    # Calcul de la taille d'effet (Cohen's d)
    pooled_std = np.sqrt((cafe_apres_intense.std()**2 + cafe_apres_normal.std()**2) / 2)
    cohens_d = diff_moyenne / pooled_std
    print(f"\nTaille d'effet (Cohen's d): {cohens_d:.4f}")
    
    if abs(cohens_d) < 0.2:
        print("  → Effet négligeable")
    elif abs(cohens_d) < 0.5:
        print("  → Effet faible")
    elif abs(cohens_d) < 0.8:
        print("  → Effet moyen")
    else:
        print("  → Effet important")
    
    # Visualisation
    plt.figure(figsize=(12, 5))
    
    # Graphique 1: Boîtes à moustaches
    plt.subplot(1, 2, 1)
    data_plot = [cafe_apres_normal, cafe_apres_intense]
    bp = plt.boxplot(data_plot, labels=['Sport Normal', 'Sport Intense'], patch_artist=True)
    bp['boxes'][0].set_facecolor('lightblue')
    bp['boxes'][1].set_facecolor('coral')
    plt.ylabel('Tasses de café (lendemain)')
    plt.title('Consommation de café selon l\'intensité du sport')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Graphique 2: Histogrammes
    plt.subplot(1, 2, 2)
    plt.hist(cafe_apres_normal, alpha=0.5, label=f'Sport Normal (n={len(cafe_apres_normal)})', 
             bins=range(0, 8), color='lightblue', edgecolor='black')
    plt.hist(cafe_apres_intense, alpha=0.5, label=f'Sport Intense (n={len(cafe_apres_intense)})', 
             bins=range(0, 8), color='coral', edgecolor='black')
    plt.xlabel('Tasses de café (lendemain)')
    plt.ylabel('Fréquence')
    plt.title('Distribution de la consommation de café')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('sport_intense_cafe_lendemain.png', dpi=300, bbox_inches='tight')
    print("\n📊 Graphique sauvegardé: sport_intense_cafe_lendemain.png")
    plt.show()
    
    # Analyse complémentaire: corrélation avec les calories
    print("\n" + "="*80)
    print("ANALYSE COMPLÉMENTAIRE: Corrélation calories vs café lendemain")
    print("="*80)
    
    corr_pearson, p_corr = stats.pearsonr(dfMerged['calories'], dfMerged['tasses_cafe'])
    print(f"Corrélation de Pearson: {corr_pearson:.4f}")
    print(f"P-value: {p_corr:.4f}")
    
    if abs(corr_pearson) < 0.1:
        print("  → Corrélation négligeable")
    elif abs(corr_pearson) < 0.3:
        print("  → Corrélation faible")
    elif abs(corr_pearson) < 0.5:
        print("  → Corrélation moyenne")
    else:
        print("  → Corrélation forte")
    
    return dfMerged