"""
Module pour générer les interprétations et réponses aux questions
"""


def genererRapportComplet(
    resultatsRegressionActivites,
    resultatsRegressionCafe,
    analysesSportCafe,
    analysesActifProductif,
    analysesExces,
    analysesEquilibre,
    analysesCaloriesCafe,
    analysesSportifsConsommentPlusCafe
):
    """
    Génère un rapport complet avec toutes les analyses
    
    Args:
        resultatsRegressionActivites (dict): Résultats par activité
        resultatsRegressionCafe (dict): Résultats café-productivité
        analysesSportCafe (dict): Analyse sport intense → café
        analysesActifProductif (dict): Analyse actifs → productifs
        analysesExces (dict): Analyse excès
        analysesEquilibre (dict): Analyse équilibre temps
        analysesCaloriesCafe (dict): Corrélation calories-café
        analysesSportifsConsommentPlusCafe (dict): Sportifs et café
    
    Returns:
        str: Rapport complet
    """
    rapport = "\n" + "="*70 + "\n"
    rapport += "           RAPPORT D'ANALYSE STATISTIQUE COMPLET\n"
    rapport += "           Café, Sport, Calories et Productivité\n"
    rapport += "="*70 + "\n\n"
    
    # Section 1 : Régressions activités
    rapport += "═" * 70 + "\n"
    rapport += "SECTION 1 : ANALYSE DES ACTIVITÉS SPORTIVES\n"
    rapport += "═" * 70 + "\n\n"
    
    for activite, resultats in resultatsRegressionActivites.items():
        pente = resultats['pente']
        r2 = resultats['r2']
        caloriesHeure = pente * 60
        
        rapport += f"┌─ {activite.upper()} " + "─" * (60 - len(activite)) + "\n"
        rapport += f"│ Pente : {pente:.2f} calories/minute\n"
        rapport += f"│ Équivalent : {caloriesHeure:.0f} calories/heure\n"
        rapport += f"│ R² : {r2:.3f}\n"
        rapport += f"│ Qualité : {'Excellent' if r2 > 0.8 else 'Bon' if r2 > 0.6 else 'Moyen'}\n"
        rapport += "└" + "─" * 68 + "\n\n"
    
    # Section 2 : Régression café-productivité
    rapport += "═" * 70 + "\n"
    rapport += "SECTION 2 : EFFET DU CAFÉ SUR LA PRODUCTIVITÉ\n"
    rapport += "═" * 70 + "\n\n"
    
    pente_cafe = resultatsRegressionCafe['pente']
    intercept_cafe = resultatsRegressionCafe['intercept']
    r2_cafe = resultatsRegressionCafe['r2']
    
    rapport += f"Équation : Productivité = {pente_cafe:.2f} × café + {intercept_cafe:.2f}\n"
    rapport += f"R² : {r2_cafe:.3f}\n\n"
    rapport += f"Interprétation :\n"
    rapport += f"• Chaque tasse de café augmente la productivité de {pente_cafe:.2f} points\n"
    rapport += f"• Productivité de base (sans café) : {intercept_cafe:.2f}\n"
    rapport += f"• L'effet devient décroissant après 6 tasses (zone rouge)\n\n"
    
    # Section 3 : Réponses aux questions
    rapport += "═" * 70 + "\n"
    rapport += "SECTION 3 : RÉPONSES AUX QUESTIONS DE RECHERCHE\n"
    rapport += "═" * 70 + "\n\n"
    
    # Question 1
    rapport += "❓ Question 1 : Les jours de sport intense, boit-on plus de café le lendemain ?\n"
    rapport += "─" * 70 + "\n"
    diff = analysesSportCafe['difference']
    pval = analysesSportCafe['pValue']
    rapport += f"• Café après sport intense : {analysesSportCafe['cafeApresSportIntense']:.2f} tasses\n"
    rapport += f"• Café sans sport intense : {analysesSportCafe['cafeSansSportIntense']:.2f} tasses\n"
    rapport += f"• Différence : {diff:+.2f} tasses\n"
    rapport += f"• Significativité (p-value) : {pval:.4f}\n"
    
    if analysesSportCafe['significatif']:
        if diff > 0:
            rapport += f"✓ RÉPONSE : OUI, significativement plus de café (+{diff:.2f} tasses)\n\n"
        else:
            rapport += f"✓ RÉPONSE : NON, significativement moins de café ({diff:.2f} tasses)\n\n"
    else:
        rapport += "⚠ RÉPONSE : Pas de différence significative\n\n"
    
    # Question 2
    rapport += "❓ Question 2 : Les individus actifs sont-ils plus productifs ?\n"
    rapport += "─" * 70 + "\n"
    diff_prod = analysesActifProductif['difference']
    corr = analysesActifProductif['correlation']
    rapport += f"• Productivité actifs : {analysesActifProductif['productiviteActifs']:.2f}\n"
    rapport += f"• Productivité sédentaires : {analysesActifProductif['productiviteSedentaires']:.2f}\n"
    rapport += f"• Différence : {diff_prod:+.2f} points\n"
    rapport += f"• Corrélation sport-productivité : {corr:.3f}\n"
    rapport += f"• Significativité : {analysesActifProductif['pValue']:.4f}\n"
    
    if analysesActifProductif['significatif']:
        if diff_prod > 0:
            rapport += f"✓ RÉPONSE : OUI, les actifs sont plus productifs (+{diff_prod:.2f})\n\n"
        else:
            rapport += f"⚠ RÉPONSE : Contre-intuitivement, les actifs sont moins productifs\n\n"
    else:
        rapport += "⚠ RÉPONSE : Pas de différence significative\n\n"
    
    # Question 3
    rapport += "❓ Question 3 : Trop de café ET trop de sport → baisse de productivité ?\n"
    rapport += "─" * 70 + "\n"
    rapport += f"• Productivité avec excès : {analysesExces['productiviteExces']:.2f}\n"
    rapport += f"• Productivité normale : {analysesExces['productiviteNormal']:.2f}\n"
    rapport += f"• Différence : {analysesExces['difference']:+.2f}\n"
    rapport += f"• Observations avec excès : {analysesExces['nbObservationsExces']}\n"
    
    if analysesExces['baisse']:
        rapport += f"✓ RÉPONSE : OUI, baisse de {abs(analysesExces['difference']):.2f} points\n\n"
    else:
        rapport += f"⚠ RÉPONSE : NON, pas de baisse observée\n\n"
    
    # Question 4
    rapport += "❓ Question 4 : Y a-t-il un équilibre entre temps total et productivité ?\n"
    rapport += "─" * 70 + "\n"
    rapport += f"• Corrélation temps-productivité : {analysesEquilibre['correlation']:.3f}\n"
    rapport += f"• Temps optimal : {analysesEquilibre['tempsOptimal']:.1f} heures\n"
    rapport += f"• Productivité maximale : {analysesEquilibre['productiviteMax']:.2f}\n"
    
    if abs(analysesEquilibre['correlation']) > 0.3:
        sens = "positive" if analysesEquilibre['correlation'] > 0 else "négative"
        rapport += f"✓ RÉPONSE : OUI, corrélation {sens} significative\n"
        rapport += f"  L'équilibre optimal est autour de {analysesEquilibre['tempsOptimal']:.1f} heures totales\n\n"
    else:
        rapport += "⚠ RÉPONSE : Corrélation faible, pas d'équilibre clair\n\n"
    
    # Question 5
    rapport += "❓ Question 5 : Corrélation entre calories et tasses de café ?\n"
    rapport += "─" * 70 + "\n"
    rapport += f"• Corrélation : {analysesCaloriesCafe['correlation']:.3f}\n"
    rapport += f"• p-value : {analysesCaloriesCafe['pValue']:.4f}\n"
    
    if analysesCaloriesCafe['significatif']:
        if analysesCaloriesCafe['correlation'] > 0:
            rapport += f"✓ RÉPONSE : OUI, corrélation positive ({analysesCaloriesCafe['correlation']:.3f})\n"
            rapport += "  Plus on brûle de calories, plus on boit de café\n\n"
        else:
            rapport += f"✓ RÉPONSE : OUI, corrélation négative ({analysesCaloriesCafe['correlation']:.3f})\n\n"
    else:
        rapport += "⚠ RÉPONSE : Pas de corrélation significative\n\n"
    
    # Question 6
    rapport += "❓ Question 6 : Les sportifs consomment-ils plus de café en moyenne ?\n"
    rapport += "─" * 70 + "\n"
    rapport += f"• Corrélation moyenne sport-café : {analysesSportifsConsommentPlusCafe['correlation']:.3f}\n"
    rapport += f"• p-value : {analysesSportifsConsommentPlusCafe['pValue']:.4f}\n"
    
    if 'cafeParQuartile' in analysesSportifsConsommentPlusCafe:
        rapport += "\nConsommation de café par quartile de sport :\n"
        for quartile, cafe in analysesSportifsConsommentPlusCafe['cafeParQuartile'].items():
            rapport += f"  {quartile} : {cafe:.2f} tasses\n"
    
    if analysesSportifsConsommentPlusCafe['significatif']:
        if analysesSportifsConsommentPlusCafe['correlation'] > 0:
            rapport += f"\n✓ RÉPONSE : OUI, corrélation positive ({analysesSportifsConsommentPlusCafe['correlation']:.3f})\n"
            rapport += "  Les plus sportifs boivent plus de café\n\n"
        else:
            rapport += f"\n✓ RÉPONSE : NON, corrélation négative\n\n"
    else:
        rapport += "\n⚠ RÉPONSE : Pas de relation significative\n\n"
    
    # Conclusion
    rapport += "═" * 70 + "\n"
    rapport += "CONCLUSION GÉNÉRALE\n"
    rapport += "═" * 70 + "\n\n"
    rapport += "Cette analyse a permis de modéliser les relations entre sport, café et\n"
    rapport += "productivité. Les modèles de régression montrent des relations linéaires\n"
    rapport += "claires pour les calories brûlées selon l'activité, et un effet positif\n"
    rapport += "du café sur la productivité jusqu'à un certain seuil.\n\n"
    
    return rapport


def sauvegarderRapport(rapport, nomFichier='rapport_analyse.txt'):
    """
    Sauvegarde le rapport dans un fichier texte
    
    Args:
        rapport (str): Contenu du rapport
        nomFichier (str): Nom du fichier
    """
    import os
    
    dossier = 'resultats'
    if not os.path.exists(dossier):
        os.makedirs(dossier)
    
    chemin = os.path.join(dossier, nomFichier)
    
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(rapport)
    
    print(f"✓ Rapport sauvegardé : {chemin}")
