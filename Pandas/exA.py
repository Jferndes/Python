import pandas as pd

def exA():

    # Méthode 1 : Créer une Series à partir d'une liste
    print("=== Méthode 1 : Series à partir d'une liste ===")
    data = [10, 20, 30, 40, 50]
    serie1 = pd.Series(data)
    print(serie1)
    print()

    # Méthode 2 : Créer une Series avec des index personnalisés
    print("=== Méthode 2 : Series avec index personnalisés ===")
    data = [85, 92, 78, 95, 88]
    index = ['Math', 'Français', 'Histoire', 'Anglais', 'Sciences']
    serie2 = pd.Series(data, index=index)
    print(serie2)
    print()

    # Méthode 3 : Créer une Series à partir d'un dictionnaire
    print("=== Méthode 3 : Series à partir d'un dictionnaire ===")
    dictionnaire = {
        'Lundi': 25,
        'Mardi': 28,
        'Mercredi': 23,
        'Jeudi': 30,
        'Vendredi': 27
    }
    serie3 = pd.Series(dictionnaire)
    print(serie3)
    print()

    # Afficher quelques informations sur la Series
    print("=== Informations sur la Series ===")
    print(f"Type de l'objet : {type(serie2)}")
    print(f"Nombre d'éléments : {len(serie2)}")
    print(f"Type des données : {serie2.dtype}")
    print(f"Index : {serie2.index.tolist()}")
    print(f"Valeurs : {serie2.values.tolist()}")