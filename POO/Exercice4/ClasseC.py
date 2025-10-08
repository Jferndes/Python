from ClasseA import ClasseA

class ClasseC(ClasseA):

    def __init__(self):
        super().__init__()

    def afficher(self):
        super().afficher()
        print("Je suis C")