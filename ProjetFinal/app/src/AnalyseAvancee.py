import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


# ============================================================================
# QUESTION 1: Les jours où les individus font du sport intense, 
#             boivent-ils plus de café le lendemain ?
# ============================================================================

def analyserSportIntenseCafeLendemain(dfSport: pd.DataFrame, dfTravail: pd.DataFrame) -> dict:
    """
    Analyse si les individus boivent plus de café le lendemain d'un sport intense.
    
    Args:
        dfSport: DataFrame avec colonnes [individu_id, date, calories, duree, ...]
        dfTravail: DataFrame avec colonnes [individu_id, date, tasses_cafe, ...]
    
    Returns:
        dict: Dictionnaire avec les résultats statistiques
    """
    print("="*80)
    print("QUESTION 1: Sport Intense → Plus de Café le Lendemain ?")
    print("="*80)
    
    # Définir le seuil de sport intense (75e percentile)
    seuilIntense = dfSport['calories'].quantile(0.75)
    print(f"\nSeuil de sport intense (75e percentile): {seuilIntense:.2f} calories")
    
    # Identifier les jours de sport intense
    dfSport = dfSport.copy()
    dfSport['sportIntense'] = dfSport['calories'] >= seuilIntense
    
    # Agréger par individu et date
    dfSportJour = dfSport.groupby(['individu_id', 'date']).agg({
        'calories': 'sum',
        'sportIntense': 'max',
        'duree': 'sum'
    }).reset_index()
    
    # Créer date lendemain
    dfSportJour['dateLendemain'] = pd.to_datetime(dfSportJour['date']) + pd.Timedelta(days=1)
    dfTravail['date'] = pd.to_datetime(dfTravail['date'])
    
    # Jointure: sport du jour J avec café du jour J+1
    dfMerge = dfSportJour.merge(
        dfTravail[['individu_id', 'date', 'tasses_cafe']],
        left_on=['individu_id', 'dateLendemain'],
        right_on=['individu_id', 'date'],
        suffixes=('_sport', '_travail')
    )
    
    print(f"Nombre d'observations: {len(dfMerge)}")
    
    if len(dfMerge) == 0:
        print("⚠️ Aucune correspondance trouvée!")
        return {}
    
    # Séparer les données
    cafeApresIntense = dfMerge[dfMerge['sportIntense'] == True]['tasses_cafe']
    cafeApresNormal = dfMerge[dfMerge['sportIntense'] == False]['tasses_cafe']
    
    # Statistiques descriptives
    print("\n" + "-"*80)
    print("STATISTIQUES DESCRIPTIVES")
    print("-"*80)
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
    
    # Test statistique: Test t de Student
    tStat, pValue = stats.ttest_ind(cafeApresIntense, cafeApresNormal)
    
    print("\n" + "-"*80)
    print("TEST STATISTIQUE (Test t de Student)")
    print("-"*80)
    print(f"Statistique t: {tStat:.4f}")
    print(f"P-value: {pValue:.4f}")
    print(f"Seuil α: 0.05")
    
    if pValue < 0.05:
        print(f"\n✓ CONCLUSION: Différence SIGNIFICATIVE (p < 0.05)")
        if diffMoyenne > 0:
            print("  → Les individus boivent PLUS de café après un sport intense.")
        else:
            print("  → Les individus boivent MOINS de café après un sport intense.")
    else:
        print(f"\n✗ CONCLUSION: Différence NON significative (p ≥ 0.05)")
    
    # Taille d'effet (Cohen's d)
    pooledStd = np.sqrt((cafeApresIntense.std()**2 + cafeApresNormal.std()**2) / 2)
    cohensD = diffMoyenne / pooledStd if pooledStd > 0 else 0
    print(f"\nTaille d'effet (Cohen's d): {cohensD:.4f}")
    
    return {
        'diffMoyenne': diffMoyenne,
        'pValue': pValue,
        'tStat': tStat,
        'cohensD': cohensD,
        'cafeApresIntense': cafeApresIntense,
        'cafeApresNormal': cafeApresNormal
    }


def visualiserSportIntenseCafe(resultats: dict, nomFichier: str = 'q1_sport_intense_cafe.png') -> None:
    """
    Visualise la relation entre sport intense et consommation de café.
    """
    if not resultats:
        return
    
    cafeApresIntense = resultats['cafeApresIntense']
    cafeApresNormal = resultats['cafeApresNormal']
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Graphique 1: Boîtes à moustaches
    ax1 = axes[0]
    dataPlot = [cafeApresNormal, cafeApresIntense]
    bp = ax1.boxplot(dataPlot, labels=['Sport Normal', 'Sport Intense'], patch_artist=True)
    bp['boxes'][0].set_facecolor('lightblue')
    bp['boxes'][1].set_facecolor('coral')
    ax1.set_ylabel('Tasses de café (lendemain)')
    ax1.set_title('Consommation de café selon l\'intensité du sport')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Graphique 2: Histogrammes
    ax2 = axes[1]
    ax2.hist(cafeApresNormal, alpha=0.6, label=f'Sport Normal (n={len(cafeApresNormal)})', 
             bins=range(0, int(max(cafeApresNormal.max(), cafeApresIntense.max())) + 2), 
             color='lightblue', edgecolor='black')
    ax2.hist(cafeApresIntense, alpha=0.6, label=f'Sport Intense (n={len(cafeApresIntense)})', 
             bins=range(0, int(max(cafeApresNormal.max(), cafeApresIntense.max())) + 2), 
             color='coral', edgecolor='black')
    ax2.set_xlabel('Tasses de café (lendemain)')
    ax2.set_ylabel('Fréquence')
    ax2.set_title('Distribution de la consommation de café')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(nomFichier, dpi=300, bbox_inches='tight')
    print(f"\n📊 Graphique sauvegardé: {nomFichier}")
    plt.close()


# ============================================================================
# QUESTION 2: Les individus actifs sont-ils plus productifs ?
# ============================================================================

def analyserActiviteProductivite(dfSport: pd.DataFrame, dfTravail: pd.DataFrame) -> dict:
    """
    Analyse si les individus actifs sont plus productifs.
    On définit l'activité par le nombre moyen de calories brûlées par semaine.
    
    Returns:
        dict: Résultats de l'analyse de corrélation
    """
    print("\n" + "="*80)
    print("QUESTION 2: Les Individus Actifs sont-ils Plus Productifs ?")
    print("="*80)
    
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
    
    # Corrélation de Spearman (non-paramétrique)
    corrSpearman, pValueSpearman = stats.spearmanr(dfMerge['caloriesMoyennes'], dfMerge['productiviteMoyenne'])
    
    print("\n" + "-"*80)
    print("CORRÉLATIONS")
    print("-"*80)
    print(f"Corrélation de Pearson: {corrPearson:.4f} (p = {pValuePearson:.4f})")
    print(f"Corrélation de Spearman: {corrSpearman:.4f} (p = {pValueSpearman:.4f})")
    
    # Interprétation
    print("\n" + "-"*80)
    print("INTERPRÉTATION")
    print("-"*80)
    
    if abs(corrPearson) < 0.1:
        interpretation = "Corrélation négligeable"
    elif abs(corrPearson) < 0.3:
        interpretation = "Corrélation faible"
    elif abs(corrPearson) < 0.5:
        interpretation = "Corrélation moyenne"
    else:
        interpretation = "Corrélation forte"
    
    print(f"Force de la corrélation: {interpretation}")
    
    if pValuePearson < 0.05:
        print("✓ La corrélation est SIGNIFICATIVE (p < 0.05)")
        if corrPearson > 0:
            print("  → Les individus plus actifs sont PLUS productifs")
        else:
            print("  → Les individus plus actifs sont MOINS productifs")
    else:
        print("✗ La corrélation n'est PAS significative (p ≥ 0.05)")
    
    return {
        'dfMerge': dfMerge,
        'corrPearson': corrPearson,
        'pValuePearson': pValuePearson,
        'corrSpearman': corrSpearman,
        'pValueSpearman': pValueSpearman
    }


def visualiserActiviteProductivite(resultats: dict, nomFichier: str = 'q2_activite_productivite.png') -> None:
    """
    Visualise la relation entre activité physique et productivité.
    """
    dfMerge = resultats['dfMerge']
    corrPearson = resultats['corrPearson']
    pValue = resultats['pValuePearson']
    
    plt.figure(figsize=(10, 6))
    plt.scatter(dfMerge['caloriesMoyennes'], dfMerge['productiviteMoyenne'], 
                alpha=0.6, color='steelblue', edgecolors='black', s=80)
    
    # Ligne de tendance
    z = np.polyfit(dfMerge['caloriesMoyennes'], dfMerge['productiviteMoyenne'], 1)
    p = np.poly1d(z)
    plt.plot(dfMerge['caloriesMoyennes'], p(dfMerge['caloriesMoyennes']), 
             "r--", alpha=0.8, linewidth=2, label=f'Tendance linéaire')
    
    plt.xlabel('Calories moyennes brûlées par jour (kcal)', fontsize=12)
    plt.ylabel('Productivité moyenne', fontsize=12)
    plt.title(f'Relation Activité Physique - Productivité\n(r = {corrPearson:.3f}, p = {pValue:.4f})', 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nomFichier, dpi=300, bbox_inches='tight')
    print(f"\n📊 Graphique sauvegardé: {nomFichier}")
    plt.close()


# ============================================================================
# QUESTION 3: Trop de café ET trop de sport → baisse de productivité ?
# ============================================================================

def analyserSurchargeProductivite(dfSport: pd.DataFrame, dfTravail: pd.DataFrame) -> dict:
    """
    Analyse si trop de café ET trop de sport entraînent une baisse de productivité.
    On identifie les valeurs "élevées" comme > 75e percentile.
    """
    print("\n" + "="*80)
    print("QUESTION 3: Trop de Café ET Trop de Sport → Baisse de Productivité ?")
    print("="*80)
    
    # Préparer les données par jour
    dfSport['date'] = pd.to_datetime(dfSport['date'])
    dfTravail['date'] = pd.to_datetime(dfTravail['date'])
    
    # Agréger le sport par jour
    dfSportJour = dfSport.groupby(['individu_id', 'date']).agg({
        'calories': 'sum',
        'duree': 'sum'
    }).reset_index()
    
    # Fusion des données
    dfMerge = dfTravail.merge(dfSportJour, on=['individu_id', 'date'], how='inner')
    
    print(f"\nNombre d'observations: {len(dfMerge)}")
    
    # Définir les seuils "élevés" (75e percentile)
    seuilCafeEleve = dfMerge['tasses_cafe'].quantile(0.75)
    seuilSportEleve = dfMerge['calories'].quantile(0.75)
    
    print(f"\nSeuil café élevé (75e percentile): {seuilCafeEleve:.0f} tasses")
    print(f"Seuil sport élevé (75e percentile): {seuilSportEleve:.2f} calories")
    
    # Créer les catégories
    dfMerge['cafeEleve'] = dfMerge['tasses_cafe'] >= seuilCafeEleve
    dfMerge['sportEleve'] = dfMerge['calories'] >= seuilSportEleve
    
    # 4 groupes
    groupeNormal = dfMerge[(~dfMerge['cafeEleve']) & (~dfMerge['sportEleve'])]
    groupeCafeSeul = dfMerge[(dfMerge['cafeEleve']) & (~dfMerge['sportEleve'])]
    groupeSportSeul = dfMerge[(~dfMerge['cafeEleve']) & (dfMerge['sportEleve'])]
    groupeDoubleSurcharge = dfMerge[(dfMerge['cafeEleve']) & (dfMerge['sportEleve'])]
    
    print("\n" + "-"*80)
    print("RÉPARTITION DES GROUPES")
    print("-"*80)
    print(f"Normal (café normal + sport normal): n={len(groupeNormal)}, prod={groupeNormal['productivite'].mean():.2f}")
    print(f"Café élevé seul: n={len(groupeCafeSeul)}, prod={groupeCafeSeul['productivite'].mean():.2f}")
    print(f"Sport élevé seul: n={len(groupeSportSeul)}, prod={groupeSportSeul['productivite'].mean():.2f}")
    print(f"Double surcharge (café + sport élevés): n={len(groupeDoubleSurcharge)}, prod={groupeDoubleSurcharge['productivite'].mean():.2f}")
    
    # Test ANOVA
    print("\n" + "-"*80)
    print("TEST ANOVA (Analyse de variance)")
    print("-"*80)
    
    fStat, pValueAnova = stats.f_oneway(
        groupeNormal['productivite'],
        groupeCafeSeul['productivite'],
        groupeSportSeul['productivite'],
        groupeDoubleSurcharge['productivite']
    )
    
    print(f"F-statistique: {fStat:.4f}")
    print(f"P-value: {pValueAnova:.4f}")
    
    if pValueAnova < 0.05:
        print("✓ Il existe une différence SIGNIFICATIVE entre les groupes (p < 0.05)")
    else:
        print("✗ Pas de différence significative entre les groupes (p ≥ 0.05)")
    
    # Comparaison spécifique: Double surcharge vs Normal
    print("\n" + "-"*80)
    print("COMPARAISON: Double Surcharge vs Normal")
    print("-"*80)
    
    if len(groupeDoubleSurcharge) > 0 and len(groupeNormal) > 0:
        tStat, pValueT = stats.ttest_ind(groupeDoubleSurcharge['productivite'], groupeNormal['productivite'])
        diffMoyenne = groupeDoubleSurcharge['productivite'].mean() - groupeNormal['productivite'].mean()
        
        print(f"Différence de productivité: {diffMoyenne:.2f}")
        print(f"T-statistique: {tStat:.4f}")
        print(f"P-value: {pValueT:.4f}")
        
        if pValueT < 0.05:
            if diffMoyenne < 0:
                print("✓ La double surcharge entraîne une BAISSE SIGNIFICATIVE de productivité")
            else:
                print("✓ La double surcharge entraîne une HAUSSE SIGNIFICATIVE de productivité")
        else:
            print("✗ Pas de différence significative")
    
    return {
        'dfMerge': dfMerge,
        'groupeNormal': groupeNormal,
        'groupeCafeSeul': groupeCafeSeul,
        'groupeSportSeul': groupeSportSeul,
        'groupeDoubleSurcharge': groupeDoubleSurcharge,
        'pValueAnova': pValueAnova,
        'fStat': fStat
    }


def visualiserSurchargeProductivite(resultats: dict, nomFichier: str = 'q3_surcharge_productivite.png') -> None:
    """
    Visualise l'impact de la surcharge (café + sport) sur la productivité.
    """
    groupes = [
        resultats['groupeNormal']['productivite'],
        resultats['groupeCafeSeul']['productivite'],
        resultats['groupeSportSeul']['productivite'],
        resultats['groupeDoubleSurcharge']['productivite']
    ]
    
    labels = ['Normal', 'Café élevé', 'Sport élevé', 'Double\nsurcharge']
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graphique 1: Boîtes à moustaches
    ax1 = axes[0]
    bp = ax1.boxplot(groupes, labels=labels, patch_artist=True)
    couleurs = ['lightgreen', 'lightblue', 'lightyellow', 'lightcoral']
    for patch, couleur in zip(bp['boxes'], couleurs):
        patch.set_facecolor(couleur)
    
    ax1.set_ylabel('Productivité', fontsize=12)
    ax1.set_title('Productivité selon le niveau de café et sport', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Graphique 2: Moyennes avec barres d'erreur
    ax2 = axes[1]
    moyennes = [g.mean() for g in groupes]
    ecartTypes = [g.std() for g in groupes]
    
    barres = ax2.bar(labels, moyennes, yerr=ecartTypes, capsize=5, 
                     color=couleurs, edgecolor='black', alpha=0.8)
    ax2.set_ylabel('Productivité moyenne', fontsize=12)
    ax2.set_title('Moyennes de productivité par groupe', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Ajouter les valeurs sur les barres
    for i, (moy, barre) in enumerate(zip(moyennes, barres)):
        ax2.text(barre.get_x() + barre.get_width()/2, moy + ecartTypes[i] + 1, 
                f'{moy:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(nomFichier, dpi=300, bbox_inches='tight')
    print(f"\n📊 Graphique sauvegardé: {nomFichier}")
    plt.close()


# ============================================================================
# QUESTION 4: Équilibre entre "heures_travail + duree_sport" et productivité ?
# ============================================================================

def analyserEquilibreTempsProductivite(dfSport: pd.DataFrame, dfTravail: pd.DataFrame) -> dict:
    """
    Analyse s'il existe un équilibre optimal entre temps total 
    (heures de travail + durée de sport) et la productivité.
    """
    print("\n" + "="*80)
    print("QUESTION 4: Équilibre Temps Total (Travail + Sport) et Productivité ?")
    print("="*80)
    
    # Préparer les données
    dfSport['date'] = pd.to_datetime(dfSport['date'])
    dfTravail['date'] = pd.to_datetime(dfTravail['date'])
    
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
    
    print(f"\nNombre d'observations: {len(dfMerge)}")
    print(f"Temps total moyen: {dfMerge['tempsTotal'].mean():.2f}h ± {dfMerge['tempsTotal'].std():.2f}h")
    print(f"  - Heures de travail: {dfMerge['heures_travail'].mean():.2f}h ± {dfMerge['heures_travail'].std():.2f}h")
    print(f"  - Heures de sport: {dfMerge['heures_sport'].mean():.2f}h ± {dfMerge['heures_sport'].std():.2f}h")
    
    # Corrélation linéaire
    corrLineaire, pValueLineaire = stats.pearsonr(dfMerge['tempsTotal'], dfMerge['productivite'])
    
    print("\n" + "-"*80)
    print("CORRÉLATION LINÉAIRE")
    print("-"*80)
    print(f"Corrélation de Pearson: {corrLineaire:.4f} (p = {pValueLineaire:.4f})")
    
    # Régression polynomiale (degré 2) pour détecter un optimum
    coeffs = np.polyfit(dfMerge['tempsTotal'], dfMerge['productivite'], 2)
    a, b, c = coeffs
    
    print("\n" + "-"*80)
    print("RÉGRESSION POLYNOMIALE (degré 2)")
    print("-"*80)
    print(f"Équation: y = {a:.4f}x² + {b:.4f}x + {c:.4f}")
    
    # Calculer R²
    yPred = np.polyval(coeffs, dfMerge['tempsTotal'])
    r2 = 1 - (np.sum((dfMerge['productivite'] - yPred)**2) / 
              np.sum((dfMerge['productivite'] - dfMerge['productivite'].mean())**2))
    print(f"R²: {r2:.4f}")
    
    # Point optimal (si parabole concave, a < 0)
    if a < 0:
        tempsOptimal = -b / (2 * a)
        productiviteOptimale = np.polyval(coeffs, tempsOptimal)
        print(f"\n✓ Optimum détecté (parabole concave):")
        print(f"  Temps total optimal: {tempsOptimal:.2f} heures")
        print(f"  Productivité maximale: {productiviteOptimale:.2f}")
    else:
        tempsOptimal = None
        productiviteOptimale = None
        print(f"\n✗ Pas d'optimum (parabole convexe, a > 0)")
    
    return {
        'dfMerge': dfMerge,
        'corrLineaire': corrLineaire,
        'pValueLineaire': pValueLineaire,
        'coeffsPolynome': coeffs,
        'r2': r2,
        'tempsOptimal': tempsOptimal,
        'productiviteOptimale': productiviteOptimale
    }


def visualiserEquilibreTemps(resultats: dict, nomFichier: str = 'q4_equilibre_temps.png') -> None:
    """
    Visualise la relation entre temps total et productivité.
    """
    dfMerge = resultats['dfMerge']
    coeffs = resultats['coeffsPolynome']
    r2 = resultats['r2']
    tempsOptimal = resultats['tempsOptimal']
    
    plt.figure(figsize=(12, 6))
    
    # Nuage de points
    plt.scatter(dfMerge['tempsTotal'], dfMerge['productivite'], 
                alpha=0.5, color='steelblue', edgecolors='black', s=60)
    
    # Courbe polynomiale
    xFit = np.linspace(dfMerge['tempsTotal'].min(), dfMerge['tempsTotal'].max(), 100)
    yFit = np.polyval(coeffs, xFit)
    plt.plot(xFit, yFit, 'r-', linewidth=2.5, 
             label=f'Régression polynomiale (R² = {r2:.3f})')
    
    # Point optimal si existe
    if tempsOptimal is not None:
        prodOpt = resultats['productiviteOptimale']
        plt.plot(tempsOptimal, prodOpt, 'go', markersize=12, 
                label=f'Optimum: {tempsOptimal:.1f}h', zorder=5)
        plt.axvline(tempsOptimal, color='green', linestyle='--', alpha=0.5)
    
    plt.xlabel('Temps total (heures de travail + heures de sport)', fontsize=12)
    plt.ylabel('Productivité', fontsize=12)
    plt.title('Relation entre Temps Total et Productivité', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nomFichier, dpi=300, bbox_inches='tight')
    print(f"\n📊 Graphique sauvegardé: {nomFichier}")
    plt.close()


# ============================================================================
# QUESTION 5: Corrélation entre calories et tasses_cafe ?
# ============================================================================

def analyserCorrelationCaloriesCafe(dfSport: pd.DataFrame, dfTravail: pd.DataFrame) -> dict:
    """
    Analyse s'il existe une corrélation entre les calories brûlées 
    et la consommation de café.
    """
    print("\n" + "="*80)
    print("QUESTION 5: Corrélation entre Calories Brûlées et Consommation de Café ?")
    print("="*80)
    
    # Préparer les données
    dfSport['date'] = pd.to_datetime(dfSport['date'])
    dfTravail['date'] = pd.to_datetime(dfTravail['date'])
    
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
    
    # Corrélation de Spearman
    corrSpearman, pValueSpearman = stats.spearmanr(dfMerge['calories'], dfMerge['tasses_cafe'])
    
    print("\n" + "-"*80)
    print("CORRÉLATIONS")
    print("-"*80)
    print(f"Corrélation de Pearson: {corrPearson:.4f} (p = {pValuePearson:.4f})")
    print(f"Corrélation de Spearman: {corrSpearman:.4f} (p = {pValueSpearman:.4f})")
    
    # Interprétation
    print("\n" + "-"*80)
    print("INTERPRÉTATION")
    print("-"*80)
    
    if abs(corrPearson) < 0.1:
        interpretation = "Corrélation négligeable"
    elif abs(corrPearson) < 0.3:
        interpretation = "Corrélation faible"
    elif abs(corrPearson) < 0.5:
        interpretation = "Corrélation moyenne"
    else:
        interpretation = "Corrélation forte"
    
    print(f"Force: {interpretation}")
    
    if pValuePearson < 0.05:
        print("✓ La corrélation est SIGNIFICATIVE (p < 0.05)")
        if corrPearson > 0:
            print("  → Plus de calories brûlées = Plus de café")
        else:
            print("  → Plus de calories brûlées = Moins de café")
    else:
        print("✗ La corrélation n'est PAS significative (p ≥ 0.05)")
    
    return {
        'dfMerge': dfMerge,
        'corrPearson': corrPearson,
        'pValuePearson': pValuePearson,
        'corrSpearman': corrSpearman,
        'pValueSpearman': pValueSpearman
    }


def visualiserCorrelationCaloriesCafe(resultats: dict, nomFichier: str = 'q5_correlation_calories_cafe.png') -> None:
    """
    Visualise la corrélation entre calories et café.
    """
    dfMerge = resultats['dfMerge']
    corrPearson = resultats['corrPearson']
    pValue = resultats['pValuePearson']
    
    plt.figure(figsize=(10, 6))
    plt.scatter(dfMerge['calories'], dfMerge['tasses_cafe'], 
                alpha=0.5, color='chocolate', edgecolors='black', s=60)
    
    # Ligne de tendance
    z = np.polyfit(dfMerge['calories'], dfMerge['tasses_cafe'], 1)
    p = np.poly1d(z)
    plt.plot(dfMerge['calories'], p(dfMerge['calories']), 
             "r--", alpha=0.8, linewidth=2, label='Tendance linéaire')
    
    plt.xlabel('Calories brûlées (kcal)', fontsize=12)
    plt.ylabel('Tasses de café', fontsize=12)
    plt.title(f'Corrélation Calories Brûlées - Consommation de Café\n(r = {corrPearson:.3f}, p = {pValue:.4f})', 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nomFichier, dpi=300, bbox_inches='tight')
    print(f"\n📊 Graphique sauvegardé: {nomFichier}")
    plt.close()


# ============================================================================
# QUESTION 6: Les individus les plus sportifs consomment-ils plus de café ?
# ============================================================================

def analyserSportifsConsommationCafe(dfSport: pd.DataFrame, dfTravail: pd.DataFrame) -> dict:
    """
    Compare la consommation de café entre individus très sportifs vs peu sportifs.
    """
    print("\n" + "="*80)
    print("QUESTION 6: Les Plus Sportifs Consomment-ils Plus de Café ?")
    print("="*80)
    
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
    
    print(f"\nNombre d'individus: {len(dfMerge)}")
    
    # Séparer en 3 groupes (tertiles)
    tertile1 = dfMerge['caloriesTotal'].quantile(0.33)
    tertile2 = dfMerge['caloriesTotal'].quantile(0.66)
    
    print(f"\nSeuils de catégorisation:")
    print(f"  Peu sportif: < {tertile1:.0f} kcal total")
    print(f"  Moyennement sportif: {tertile1:.0f} - {tertile2:.0f} kcal")
    print(f"  Très sportif: > {tertile2:.0f} kcal")
    
    # Créer les groupes
    groupePeuSportif = dfMerge[dfMerge['caloriesTotal'] < tertile1]
    groupeMoyennement = dfMerge[(dfMerge['caloriesTotal'] >= tertile1) & (dfMerge['caloriesTotal'] < tertile2)]
    groupeTresSportif = dfMerge[dfMerge['caloriesTotal'] >= tertile2]
    
    print("\n" + "-"*80)
    print("STATISTIQUES PAR GROUPE")
    print("-"*80)
    print(f"\nPeu sportif (n={len(groupePeuSportif)}):")
    print(f"  Café moyen: {groupePeuSportif['cafeMoyen'].mean():.2f} tasses")
    print(f"  Écart-type: {groupePeuSportif['cafeMoyen'].std():.2f}")
    
    print(f"\nMoyennement sportif (n={len(groupeMoyennement)}):")
    print(f"  Café moyen: {groupeMoyennement['cafeMoyen'].mean():.2f} tasses")
    print(f"  Écart-type: {groupeMoyennement['cafeMoyen'].std():.2f}")
    
    print(f"\nTrès sportif (n={len(groupeTresSportif)}):")
    print(f"  Café moyen: {groupeTresSportif['cafeMoyen'].mean():.2f} tasses")
    print(f"  Écart-type: {groupeTresSportif['cafeMoyen'].std():.2f}")
    
    # Test ANOVA
    print("\n" + "-"*80)
    print("TEST ANOVA")
    print("-"*80)
    
    fStat, pValueAnova = stats.f_oneway(
        groupePeuSportif['cafeMoyen'],
        groupeMoyennement['cafeMoyen'],
        groupeTresSportif['cafeMoyen']
    )
    
    print(f"F-statistique: {fStat:.4f}")
    print(f"P-value: {pValueAnova:.4f}")
    
    if pValueAnova < 0.05:
        print("✓ Différence SIGNIFICATIVE entre les groupes (p < 0.05)")
    else:
        print("✗ Pas de différence significative (p ≥ 0.05)")
    
    # Comparaison directe: Très sportif vs Peu sportif
    print("\n" + "-"*80)
    print("COMPARAISON: Très Sportif vs Peu Sportif")
    print("-"*80)
    
    tStat, pValueT = stats.ttest_ind(groupeTresSportif['cafeMoyen'], groupePeuSportif['cafeMoyen'])
    diffMoyenne = groupeTresSportif['cafeMoyen'].mean() - groupePeuSportif['cafeMoyen'].mean()
    
    print(f"Différence de consommation: {diffMoyenne:.2f} tasses")
    print(f"T-statistique: {tStat:.4f}")
    print(f"P-value: {pValueT:.4f}")
    
    if pValueT < 0.05:
        if diffMoyenne > 0:
            print("✓ Les individus très sportifs boivent PLUS de café (significatif)")
        else:
            print("✓ Les individus très sportifs boivent MOINS de café (significatif)")
    else:
        print("✗ Pas de différence significative")
    
    # Corrélation globale
    corrPearson, pValueCorr = stats.pearsonr(dfMerge['caloriesTotal'], dfMerge['cafeMoyen'])
    
    print("\n" + "-"*80)
    print("CORRÉLATION GLOBALE")
    print("-"*80)
    print(f"Corrélation de Pearson: {corrPearson:.4f} (p = {pValueCorr:.4f})")
    
    return {
        'dfMerge': dfMerge,
        'groupePeuSportif': groupePeuSportif,
        'groupeMoyennement': groupeMoyennement,
        'groupeTresSportif': groupeTresSportif,
        'pValueAnova': pValueAnova,
        'corrPearson': corrPearson,
        'pValueCorr': pValueCorr
    }


def visualiserSportifsConsommationCafe(resultats: dict, nomFichier: str = 'q6_sportifs_cafe.png') -> None:
    """
    Visualise la consommation de café selon le niveau sportif.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graphique 1: Boîtes à moustaches par groupe
    ax1 = axes[0]
    groupes = [
        resultats['groupePeuSportif']['cafeMoyen'],
        resultats['groupeMoyennement']['cafeMoyen'],
        resultats['groupeTresSportif']['cafeMoyen']
    ]
    bp = ax1.boxplot(groupes, labels=['Peu\nsportif', 'Moyennement\nsportif', 'Très\nsportif'], 
                     patch_artist=True)
    couleurs = ['lightcoral', 'lightyellow', 'lightgreen']
    for patch, couleur in zip(bp['boxes'], couleurs):
        patch.set_facecolor(couleur)
    
    ax1.set_ylabel('Consommation moyenne de café (tasses)', fontsize=11)
    ax1.set_title('Consommation de café selon le niveau sportif', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Graphique 2: Nuage de points + tendance
    ax2 = axes[1]
    dfMerge = resultats['dfMerge']
    ax2.scatter(dfMerge['caloriesTotal'], dfMerge['cafeMoyen'], 
                alpha=0.6, color='purple', edgecolors='black', s=80)
    
    # Ligne de tendance
    z = np.polyfit(dfMerge['caloriesTotal'], dfMerge['cafeMoyen'], 1)
    p = np.poly1d(z)
    ax2.plot(dfMerge['caloriesTotal'], p(dfMerge['caloriesTotal']), 
             "r--", alpha=0.8, linewidth=2, label='Tendance linéaire')
    
    ax2.set_xlabel('Calories totales brûlées', fontsize=11)
    ax2.set_ylabel('Consommation moyenne de café (tasses)', fontsize=11)
    ax2.set_title('Corrélation Activité Sportive - Café', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nomFichier, dpi=300, bbox_inches='tight')
    print(f"\n📊 Graphique sauvegardé: {nomFichier}")
    plt.close()