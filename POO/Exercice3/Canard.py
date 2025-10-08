from Volant import Volant
from Nageur import Nageur

class Canard(Volant, Nageur):
    def __init__(self, nom):
        super().__init__(nom)

    def parler(self):
        print("Coin coin !")
    