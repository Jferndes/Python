"""
Script pour créer la structure de dossiers du projet
"""
import os


def creerStructure():
    """
    Crée tous les dossiers nécessaires pour le projet
    """
    dossiers = [
        'donnees',
        'analyse',
        'visualisation',
        'resultats',
        'config'
    ]
    
    print("Création de la structure du projet...")
    print("="*50)
    
    for dossier in dossiers:
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            print(f"✓ Dossier créé : {dossier}/")
            
            # Créer __init__.py pour que Python reconnaisse comme package
            init_file = os.path.join(dossier, '__init__.py')
            with open(init_file, 'w') as f:
                f.write(f'"""\nPackage {dossier}\n"""\n')
        else:
            print(f"  Dossier existe déjà : {dossier}/")
    
    print("="*50)
    print("✓ Structure créée avec succès !")
    print("\nStructure du projet :")
    print("""
projet/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── setup_structure.py
│
├── donnees/
│   ├── __init__.py
│   ├── chargementDonnees.py
│   └── nettoyageDonnees.py
│
├── analyse/
│   ├── __init__.py
│   ├── regressionLineaire.py
│   ├── statistiques.py
│   └── correlations.py
│
├── visualisation/
│   ├── __init__.py
│   ├── graphiquesRegression.py
│   ├── graphiquesResidus.py
│   └── utilitairesGraphiques.py
│
├── resultats/
│   ├── __init__.py
│   └── interpretations.py
│
└── config/
    ├── __init__.py
    └── constantes.py
    """)


if __name__ == "__main__":
    creerStructure()
