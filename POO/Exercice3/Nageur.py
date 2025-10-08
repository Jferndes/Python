from Animal import Animal

class Nageur(Animal):
    def __init__(self, nom):
        super().__init__(nom)

    def nager(self):
        print("Je nage !")