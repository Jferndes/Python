from math import pi

class Cercle:
    
    def __init__(self, rayon):
        self.rayon = rayon

    def surface(self):
        return pi * self.rayon ** 2
    
    def __str__(self):
        return "le cercle de rayon "+ str(self.rayon)+ " a une surface de "+ str(self.surface())

    