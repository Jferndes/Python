from Animal import Animal

class Volant(Animal):
    def __init__(self, nom):
        super().__init__(nom)

    def voler(self):
        print("Je vole !")