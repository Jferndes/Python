from Cercle import Cercle

class Cylindre(Cercle):
    def __init__(self, rayon, hauteur):
        super().__init__(rayon)
        self.hauteur = hauteur

    def volume(self):
        return self.surface() * self.hauteur
    
    def __str__(self):
        return "le cylindre de rayon "+ str(self.rayon)+ " et de hauteur "+ str(self.hauteur)+ " a un volume de "+ str(self.volume())