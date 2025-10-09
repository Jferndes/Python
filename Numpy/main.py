import numpy as np


if __name__ == "__main__":
    print("Hello, World!")
    #Ex1
    #np.info(np.add)

    #Ex2
    # tab = np.array([1, 2, 3, 4, 5])
    # tab2 = np.zeros((3, 4))
    # print("Array tab:", tab)
    # print("Array tab2 (zeros):", tab2)
    # testZero = np.all(tab == 0)
    # testZero2 = np.all(tab2 == 0)
    # print("All elements are zero:", testZero)
    # print("All elements are zero (tab2):", testZero2)

    ##Ex3
    #tableau = np.array([0, np.nan, 2, np.nan, 5])
    #resultat = np.isnan(tableau)
    #print("Tableau d'origine :")
    #print(tableau)
    #print("\nRésultat du test (True = NaN, False = non NaN) :")
    #print(resultat)

    ##Ex4
    ## Création de deux tableaux
    #tableau1 = np.array([1, 2, 3, 4, 5])
    #tableau2 = np.array([1, 2, 0, 4, 5])
    #tableau3 = np.array([1, 2, 0, 4, 5])
    #
    ## Test élément par élément
    #resultat = np.equal(tableau1, tableau2)
    #resultat2 = np.equal(tableau2, tableau3)
    #print("Résultat du test entre tableau1 et tableau2 :")
    #print(resultat)
    #print("Résultat du test entre tableau2 et tableau3 :")
    #print(resultat2)


    ###Ex5
    ## Création de deux tableaux
    #tableau1 = np.array([3, 5, 7, 9])
    #tableau2 = np.array([4, 5, 2, 9])
    #
    ## Comparaisons élément par élément
    #plus_grand = np.greater(tableau1, tableau2)
    #plus_grand_egal = np.greater_equal(tableau1, tableau2)
    #moins = np.less(tableau1, tableau2)
    #moins_egal = np.less_equal(tableau1, tableau2)
    #
    ## Affichage des résultats
    #print("Tableau 1 :", tableau1)
    #print("Tableau 2 :", tableau2)
    #
    #print("\nComparaison élément par élément :")
    #print("tableau1 > tableau2  →", plus_grand)
    #print("tableau1 >= tableau2 →", plus_grand_egal)
    #print("tableau1 < tableau2  →", moins)
    #print("tableau1 <= tableau2 →", moins_egal)

    ##Ex6
    ## Création du tableau
    #tableau = np.array([1, 7, 13, 105])
#
    ## Affichage du tableau
    #print("Tableau :", tableau)
#
    ## Taille de la mémoire occupée (en octets)
    #taille_octets = tableau.nbytes
#
    #print("\nTaille de la mémoire occupée par le tableau :", taille_octets, "octets")

    ##Ex7
    ## Création des tableaux
    #zeros = np.zeros(10, dtype=int)
    #zeros2 = np.zeros((3, 10), dtype=int)
    #uns = np.ones(10, dtype=int)
    #cinq = np.full(10, 5, dtype=int)
#
    ## Affichage du résultat
    #print("Tableau :")
    #print(zeros)
    #print(zeros2)
    #print(uns)
    #print(cinq)

    ###Ex8
    ## Création d'un tableau 3x4
    #tableau = np.arange(12).reshape(3, 4)
#
    #print("Tableau 3x4 :")
    #print(tableau)
#
    #print("\nItération sur les éléments du tableau :")
    #for ligne in tableau:
    #    for element in ligne:
    #        print(element, end=' ')
    #    print()  # saut de ligne après chaque ligne du tableau
    
    ##Ex9
    #    # Création d'une matrice identité 3x3
    #matrice_identite = np.identity(3, dtype=int)
#
    ## Affichage de la matrice
    #print("Matrice d'identité 3x3 :")
    #print(matrice_identite)

    ##Ex10
    #tableau = np.array([[1, 2, 3, 4],
    #                [5, 6, 7, 8],
    #                [9, 10, 11, 12]])
    #
    #print("=== Utilisation de np.flip() ===")
    #print("\nLignes inversées avec np.flip() :")
    #print(np.flip(tableau, axis=0))
#
    #print("\nColonnes inversées avec np.flip() :")
    #print(np.flip(tableau, axis=1))
#
    #print("\nLignes ET colonnes inversées avec np.flip() :")
    #print(np.flip(tableau))

    ##Ex11
    ## Créer deux tableaux de même taille
    #tableau1 = np.array([[1, 2, 3],
    #                    [4, 5, 6],
    #                    [7, 8, 9]])
#
    #tableau2 = np.array([[2, 2, 2],
    #                    [3, 3, 3],
    #                    [4, 4, 4]])
#
    #print("Tableau 1 :")
    #print(tableau1)
    #print("\nTableau 2 :")
    #print(tableau2)
    #print()
#
    ## Méthode 1 : Multiplication élément par élément avec l'opérateur *
    #resultat = tableau1 * tableau2
    #print("Multiplication élément par élément (avec *) :")
    #print(resultat)
    #print()
#
    ## Méthode 2 : Utiliser np.multiply() - équivalent
    #resultat2 = np.multiply(tableau1, tableau2)
    #print("Multiplication avec np.multiply() :")
    #print(resultat2)
    #print()
#
    ## Vérification que les deux méthodes donnent le même résultat
    #print("Les résultats sont identiques :", np.array_equal(resultat, resultat2))
    #print()
#
    #resultat3 = np.dot(tableau1, tableau2)
    #print("Produit matriciel avec np.dot() :")
    #print(resultat3)
    #print()

    

