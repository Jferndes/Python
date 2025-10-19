# Analyse Statistique : Café, Sport, Calories et Productivité

Application Python d'analyse statistique explorant les relations entre l'activité sportive, la consommation de café et la productivité au travail.

## 📋 Description

Cette application réalise une analyse statistique complète avec :
- Régressions linéaires simples et multivariées
- Visualisations graphiques (scatter plots, résidus, comparaisons)
- Analyses de corrélations
- Réponses à des questions de recherche spécifiques

## 🏗️ Architecture

```
projet/
│
├── main.py                          # Point d'entrée principal
│
├── donnees/
│   ├── chargementDonnees.py        # Chargement des CSV
│   └── nettoyageDonnees.py         # Nettoyage et préparation
│
├── analyse/
│   ├── regressionLineaire.py      # Modèles de régression
│   ├── statistiques.py            # Calculs statistiques
│   └── correlations.py            # Analyses de corrélations
│
├── visualisation/
│   ├── graphiquesRegression.py    # Scatter + droites de régression
│   ├── graphiquesResidus.py       # Graphiques des résidus
│   └── utilitairesGraphiques.py   # Fonctions communes de traçage
│
├── resultats/
│   └── interpretations.py         # Génération des rapports
│
└── config/
    └── constantes.py              # Constantes (METs, etc.)
```

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

### 1. Préparer les données

Placez vos fichiers CSV à la racine du projet :
- `sport_raw.csv`
- `travail_raw.csv`

### 2. Exécuter l'application

```bash
python main.py
```

### 3. Résultats

Les résultats seront générés dans le dossier `resultats/` :
- **Graphiques PNG** : Toutes les visualisations
- **rapport_analyse.txt** : Rapport complet avec interprétations

## 📊 Analyses Réalisées

### 1. Régressions par activité (simple)
Pour chaque activité (course, vélo, natation) :
- Modèle : `calories = a × durée + b`
- Graphique scatter + droite de régression
- Calcul du R²
- Interprétation de la pente (calories/minute)

### 2. Régressions multivariées
Pour chaque activité :
- Modèle : `calories = a × durée + b × poids_kg + c`
- Visualisation de l'influence de chaque variable
- Comparaison avec le modèle simple

### 3. Analyse des résidus
Pour chaque régression :
- Graphique résidus vs durée
- Distribution des résidus (histogramme)
- Q-Q plot (normalité)
- Tests de linéarité, homoscédasticité, outliers

### 4. Régression café → productivité
- Modèle : `productivité = a × tasses_café + b`
- Analyse de l'intervalle 0-6 tasses
- Identification du seuil de rendement décroissant

### 5. Questions de recherche

L'application répond aux questions suivantes :

1. **Sport intense → café ?** Les jours de sport intense sont-ils suivis de plus de café le lendemain ?
2. **Actifs → productifs ?** Les individus actifs sont-ils plus productifs ?
3. **Excès → baisse ?** Trop de café ET trop de sport diminuent-ils la productivité ?
4. **Équilibre temps ?** Y a-t-il un équilibre optimal entre heures de travail + sport et productivité ?
5. **Calories ↔ café ?** Corrélation entre calories brûlées et café consommé ?
6. **Sportifs → café ?** Les sportifs consomment-ils plus de café en moyenne ?

## 📈 Format des données

### sport_raw.csv
```
individu_id,date,activite,duree,unite,poids_kg,calories
1,2024-01-01,course,30.5,min,75.0,298.5
```

### travail_raw.csv
```
individu_id,date,tasses_cafe,heures_travail,productivite
1,2024-01-01,3,8.0,65.2
```

## 🎨 Graphiques Générés

- `regression_simple_course.png`
- `regression_simple_velo.png`
- `regression_simple_natation.png`
- `regression_multivariee_course.png`
- `regression_multivariee_velo.png`
- `regression_multivariee_natation.png`
- `residus_course.png`
- `residus_velo.png`
- `residus_natation.png`
- `qqplot_course.png`
- `qqplot_velo.png`
- `qqplot_natation.png`
- `comparaison_activites.png`
- `regression_cafe_productivite.png`

## 🔧 Principes de conception

- **Architecture modulaire** : Séparation claire des responsabilités
- **Fonctions pures** : Pas d'effets de bord
- **Pas de classes** : Architecture procédurale
- **Nomenclature française** : Variables et fichiers en français (camelCase)
- **Réutilisabilité** : Fonctions génériques

## 📝 Exemple de sortie

```
═══════════════════════════════════════════════════════════════════
SECTION 1 : ANALYSE DES ACTIVITÉS SPORTIVES
═══════════════════════════════════════════════════════════════════

┌─ COURSE ────────────────────────────────────────────────────────
│ Pente : 9.85 calories/minute
│ Équivalent : 591 calories/heure
│ R² : 0.856
│ Qualité : Excellent
└──────────────────────────────────────────────────────────────────
```

## 🔮 Extensions futures (facultatif)

- Transformation en API REST
- Dockerisation avec docker-compose
- Tests unitaires
- Interface web
- Analyses du jour précédent

## 👨‍💻 Auteur

Projet d'analyse statistique développé avec Python, Pandas, NumPy, SciPy et Matplotlib.

## 📄 Licence

Projet académique.