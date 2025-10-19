"""
Constantes pour l'analyse statistique
"""

# Valeurs MET (Metabolic Equivalent of Task)
METS = {
    'course': 9.8,
    'velo': 7.5,
    'natation': 8.0
}

# Paramètres de modélisation
FORMULE_CALORIES_COEFFICIENT = 3.5
FORMULE_CALORIES_DIVISEUR = 200

# Paramètres café-productivité
PRODUCTIVITE_BASE = 45
PRODUCTIVITE_COEFFICIENT_CAFE = 4.5
CAFE_MAX_LINEAIRE = 6

# Paramètres de visualisation
FIGSIZE_DEFAULT = (10, 6)
COULEURS_ACTIVITES = {
    'course': '#FF6B6B',
    'velo': '#4ECDC4',
    'natation': '#45B7D1'
}
DPI_SAUVEGARDE = 300
