from ClasseA import ClasseA
from ClasseB import ClasseB
from ClasseC import ClasseC
from ClasseD import ClasseD

if __name__ == '__main__':
    cA = ClasseA()
    cA.afficher()
    print("-----")
    cB = ClasseB()
    cB.afficher()
    print("-----")
    cC = ClasseC()
    cC.afficher()
    print("-----")
    cD = ClasseD()
    cD.afficher()
    print(ClasseD.mro())  # Method Resolution Order