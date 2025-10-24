Supprimer le .venv si existant avant de créer un nouvel environnement virtuel
Ce mettre dans le répertoire app et lancer la commande :

    python -m venv venv  -> pour créer un environnement virtuel si non existant
    venv\Scripts\activate  -> pour activer l'environnement virtuel sous windows
    pip install -r requirements.txt -> pour installer les dépendances

    python main.py -> pour l'app console
    python api.py -> pour l'api flask
    
    Les images générées seront dans le dossier app/resultats

    Pour Docker utiliser la commande suivante dans le répertoire app :
    docker-compose up --build

    Listes des Api disponibles:
        /api/v1/analyses/sport/lineaire                                "Analyse des activités sportives linéaire"
        /api/v1/analyses/sport/multivariee                             "Analyse des activités sportives multivariée"
        /api/v1/analyses/travail                                       "Analyse des données de productivité au travail"
        /api/v1/analyses/images/regressionSimple/<string:activite>     "Obtenir l'image de la régression linéaire simple pour une activité donnée (course, velo, natation, productivite)",
        /api/v1/analyses/images/regressionMultiple/<string:activite>   "Obtenir l'image de la régression linéaire multiple pour une activité donnée (course, velo, natation)",
        /api/v1/analyses/images/polynome/<string:activite>             "Obtenir l'image de la régression polynomiale pour une activité donnée (productivite)",
        /api/v1/analyses/sport-cafe-lendemain                          "Analyse du sport et consommation de café le lendemain",
        /api/v1/analyses/actif-productivite                            "Analyse de l'activité physique vs productivité",
        /api/v1/analyses/surcharge-productivite                        "Analyse de la surcharge de travail vs productivité",
        /api/v1/analyses/equilibre-temps-productivite                  "Analyse de l'équilibre du temps vs productivité",
        /api/v1/analyses/correlation-calories-cafe                     "Analyse de la corrélation entre calories brûlées et consommation de café",
        /api/v1/analyses/sportifs-consommation-cafe                    "Analyse de la consommation de café chez les sportifs"

