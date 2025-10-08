from POO.Exercice3.Animal import Animal

class Chien(Animal):

    def __init__(self, nom):
        super().__init__(nom)
    
    def parler(self):
        print("Woof!")