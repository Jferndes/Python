from Cylindre import Cylindre

class Cone(Cylindre):
    def __init__(self, rayon, hauteur):
        super().__init__(rayon, hauteur)

    def volume(self):
        return (1/3) * super().volume()
    
    def __str__(self):
        return "le cone de rayon "+ str(self.rayon)+ " et de hauteur "+ str(self.hauteur)+ " a un volume de "+ str(self.volume())