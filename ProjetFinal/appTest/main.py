"""
Application principale d'analyse statistique
Café, Sport, Calories et Productivité
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Imports des modules
from donnees.chargementDonnees import chargerDonneesSport, chargerDonneesTravail, afficherApercu
from donnees.nettoyageDonnees import (
    nettoyerDonneesSport, nettoyerDonneesTravail, 
    filtrerParActivite, fusionnerDonnees, ajouterJourPrecedent
)
from analyse.regressionLineaire import (
    regressionLineaireSimple, regressionLineaireMultiple,
    interpreterPenteCalories
)
from analyse.correlations import (
    analyserSportIntenseCafe, analyserActifProductif,
    analyserExcesCafeSport, analyserEquilibreTempsTravailSport,
    analyserCorrelationCaloriesCafe, analyserSportifsConsommentPlusCafe
)
from visualisation.utilitairesGraphiques import configurerStyle
from visualisation.graphiquesRegression import (
    tracerScatterAvecRegression, tracerRegressionMultivariee,
    tracerRegressionCafeProductivite, tracerComparaisonActivites
)
from visualisation.graphiquesResidus import (
    tracerResidusDuree, analyserResidus, tracerQQPlot
)
from resultats.interpretations import genererRapportComplet, sauvegarderRapport


def main():
    """
    Fonction principale de l'application
    """
    print("\n" + "="*70)
    print("  APPLICATION D'ANALYSE STATISTIQUE")
    print("  Café, Sport, Calories et Productivité")
    print("="*70 + "\n")
    
    # Configuration du style graphique
    configurerStyle()
    
    # ========================================================================
    # ÉTAPE 1 : CHARGEMENT DES DONNÉES
    # ========================================================================
    print("\n" + "─"*70)
    print("ÉTAPE 1 : Chargement des données")
    print("─"*70)
    
    dfSport = chargerDonneesSport('sport_raw.csv')
    dfTravail = chargerDonneesTravail('travail_raw.csv')
    
    # Afficher aperçu
    afficherApercu(dfSport, "Sport")
    afficherApercu(dfTravail, "Travail")
    
    # ========================================================================
    # ÉTAPE 2 : NETTOYAGE DES DONNÉES
    # ========================================================================
    print("\n" + "─"*70)
    print("ÉTAPE 2 : Nettoyage des données")
    print("─"*70)
    
    dfSportClean = nettoyerDonneesSport(dfSport)
    dfTravailClean = nettoyerDonneesTravail(dfTravail)
    
    # ========================================================================
    # ÉTAPE 3 : RÉGRESSIONS PAR ACTIVITÉ (SIMPLE)
    # ========================================================================
    print("\n" + "─"*70)
    print("ÉTAPE 3 : Régressions linéaires simples par activité")
    print("─"*70)
    
    activites = ['course', 'velo', 'natation']
    resultatsRegressionActivites = {}
    
    for activite in activites:
        print(f"\n▸ Analyse de l'activité : {activite.upper()}")
        
        # Filtrer données
        dfActivite = filtrerParActivite(dfSportClean, activite)
        
        # Régression simple : calories = a * duree + b
        x = dfActivite['duree'].values
        y = dfActivite['calories'].values
        
        resultats = regressionLineaireSimple(x, y)
        resultatsRegressionActivites[activite] = resultats
        
        # Afficher interprétation
        print(interpreterPenteCalories(resultats['pente'], activite))
        print(f"R² = {resultats['r2']:.3f}")
        
        # Tracer graphique
        nomFichier = f'regression_simple_{activite}.png'
        tracerScatterAvecRegression(resultats, activite, nomFichier)
        
        # Analyse des résidus
        print(analyserResidus(resultats, activite))
        tracerResidusDuree(resultats, activite, f'residus_{activite}.png')
        tracerQQPlot(resultats, activite, f'qqplot_{activite}.png')
    
    # Comparaison des activités
    print("\n▸ Comparaison des intensités entre activités")
    tracerComparaisonActivites(resultatsRegressionActivites, 'comparaison_activites.png')
    
    # ========================================================================
    # ÉTAPE 4 : RÉGRESSIONS MULTIVARIÉES
    # ========================================================================
    print("\n" + "─"*70)
    print("ÉTAPE 4 : Régressions linéaires multivariées")
    print("─"*70)
    
    for activite in activites:
        print(f"\n▸ Régression multivariée : {activite.upper()}")
        
        dfActivite = filtrerParActivite(dfSportClean, activite)
        
        # Régression : calories = a*duree + b*poids_kg + c
        X = np.column_stack([
            dfActivite['duree'].values,
            dfActivite['poids_kg'].values
        ])
        y = dfActivite['calories'].values
        
        resultats = regressionLineaireMultiple(X, y)
        
        print(f"Coefficients :")
        print(f"  • Durée : {resultats['coefficients'][0]:.2f} cal/min")
        print(f"  • Poids : {resultats['coefficients'][1]:.2f} cal/kg")
        print(f"  • Intercept : {resultats['intercept']:.2f}")
        print(f"  • R² : {resultats['r2']:.3f}")
        
        # Tracer graphique
        nomFichier = f'regression_multivariee_{activite}.png'
        tracerRegressionMultivariee(resultats, activite, nomFichier)
    
    # ========================================================================
    # ÉTAPE 5 : RÉGRESSION CAFÉ → PRODUCTIVITÉ
    # ========================================================================
    print("\n" + "─"*70)
    print("ÉTAPE 5 : Régression café → productivité (0-6 tasses)")
    print("─"*70)
    
    # Filtrer pour 0-6 tasses
    dfCafe = dfTravailClean[dfTravailClean['tasses_cafe'] <= 6].copy()
    
    x = dfCafe['tasses_cafe'].values
    y = dfCafe['productivite'].values
    
    resultatsRegressionCafe = regressionLineaireSimple(x, y)
    
    print(f"\nÉquation : Productivité = {resultatsRegressionCafe['pente']:.2f} × café + {resultatsRegressionCafe['intercept']:.2f}")
    print(f"R² = {resultatsRegressionCafe['r2']:.3f}")
    print(f"\nInterprétation de la pente :")
    print(f"  Chaque tasse de café augmente la productivité de {resultatsRegressionCafe['pente']:.2f} points")
    print(f"  L'effet devient décroissant après 6 tasses (saturation)")
    
    # Tracer graphique
    tracerRegressionCafeProductivite(resultatsRegressionCafe, 'regression_cafe_productivite.png')
    
    # ========================================================================
    # ÉTAPE 6 : FUSION DES DONNÉES ET ANALYSES CROISÉES
    # ========================================================================
    print("\n" + "─"*70)
    print("ÉTAPE 6 : Analyses croisées (fusion des datasets)")
    print("─"*70)
    
    # Fusionner les données
    dfFusion = fusionnerDonnees(dfSportClean, dfTravailClean)
    dfFusion = ajouterJourPrecedent(dfFusion)
    
    print(f"✓ Données fusionnées : {len(dfFusion)} observations")
    
    # ========================================================================
    # ÉTAPE 7 : RÉPONSES AUX QUESTIONS
    # ========================================================================
    print("\n" + "─"*70)
    print("ÉTAPE 7 : Réponses aux questions de recherche")
    print("─"*70)
    
    print("\n▸ Question 1 : Sport intense → plus de café le lendemain ?")
    analysesSportCafe = analyserSportIntenseCafe(dfFusion, seuilIntense=60)
    print(f"  Café après sport intense : {analysesSportCafe['cafeApresSportIntense']:.2f} tasses")
    print(f"  Café sans sport intense : {analysesSportCafe['cafeSansSportIntense']:.2f} tasses")
    print(f"  Différence : {analysesSportCafe['difference']:+.2f} tasses")
    print(f"  Significatif : {'Oui' if analysesSportCafe['significatif'] else 'Non'} (p={analysesSportCafe['pValue']:.4f})")
    
    print("\n▸ Question 2 : Individus actifs plus productifs ?")
    analysesActifProductif = analyserActifProductif(dfFusion, seuilActif=30)
    print(f"  Productivité actifs : {analysesActifProductif['productiviteActifs']:.2f}")
    print(f"  Productivité sédentaires : {analysesActifProductif['productiviteSedentaires']:.2f}")
    print(f"  Différence : {analysesActifProductif['difference']:+.2f}")
    print(f"  Corrélation : {analysesActifProductif['correlation']:.3f}")
    print(f"  Significatif : {'Oui' if analysesActifProductif['significatif'] else 'Non'}")
    
    print("\n▸ Question 3 : Trop de café + trop de sport → baisse productivité ?")
    analysesExces = analyserExcesCafeSport(dfFusion, seuilCafe=6, seuilSport=90)
    print(f"  Productivité avec excès : {analysesExces['productiviteExces']:.2f}")
    print(f"  Productivité normale : {analysesExces['productiviteNormal']:.2f}")
    print(f"  Différence : {analysesExces['difference']:+.2f}")
    print(f"  Baisse observée : {'Oui' if analysesExces['baisse'] else 'Non'}")
    
    print("\n▸ Question 4 : Équilibre temps travail + sport vs productivité ?")
    analysesEquilibre = analyserEquilibreTempsTravailSport(dfFusion)
    print(f"  Corrélation : {analysesEquilibre['correlation']:.3f}")
    print(f"  Temps optimal : {analysesEquilibre['tempsOptimal']:.1f} heures")
    print(f"  Productivité max : {analysesEquilibre['productiviteMax']:.2f}")
    
    print("\n▸ Question 5 : Corrélation calories et café ?")
    analysesCaloriesCafe = analyserCorrelationCaloriesCafe(dfFusion)
    print(f"  Corrélation : {analysesCaloriesCafe['correlation']:.3f}")
    print(f"  Significatif : {'Oui' if analysesCaloriesCafe['significatif'] else 'Non'} (p={analysesCaloriesCafe['pValue']:.4f})")
    
    print("\n▸ Question 6 : Sportifs consomment plus de café ?")
    analysesSportifsConsommentPlusCafe = analyserSportifsConsommentPlusCafe(dfFusion)
    print(f"  Corrélation moyenne : {analysesSportifsConsommentPlusCafe['correlation']:.3f}")
    print(f"  Significatif : {'Oui' if analysesSportifsConsommentPlusCafe['significatif'] else 'Non'}")
    if 'cafeParQuartile' in analysesSportifsConsommentPlusCafe:
        print(f"  Café par quartile d'activité :")
        for quartile, cafe in analysesSportifsConsommentPlusCafe['cafeParQuartile'].items():
            print(f"    {quartile} : {cafe:.2f} tasses")
    
    # ========================================================================
    # ÉTAPE 8 : GÉNÉRATION DU RAPPORT FINAL
    # ========================================================================
    print("\n" + "─"*70)
    print("ÉTAPE 8 : Génération du rapport final")
    print("─"*70)
    
    rapport = genererRapportComplet(
        resultatsRegressionActivites,
        resultatsRegressionCafe,
        analysesSportCafe,
        analysesActifProductif,
        analysesExces,
        analysesEquilibre,
        analysesCaloriesCafe,
        analysesSportifsConsommentPlusCafe
    )
    
    # Afficher le rapport
    print(rapport)
    
    # Sauvegarder le rapport
    sauvegarderRapport(rapport)
    
    # ========================================================================
    # FIN
    # ========================================================================
    print("\n" + "="*70)
    print("  ANALYSE TERMINÉE AVEC SUCCÈS !")
    print("  Tous les graphiques et rapports ont été sauvegardés dans './resultats/'")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
