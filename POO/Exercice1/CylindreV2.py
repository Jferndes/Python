from CercleV2 import CercleV2

class CylindreV2(CercleV2):
    """Représente un cylindre, hérite de Cercle."""

    def __init__(self, rayon: float, hauteur: float) -> None:
        super().__init__(rayon)
        if hauteur <= 0:
            raise ValueError("La hauteur doit être positive.")
        self._hauteur = hauteur

    @property
    def hauteur(self) -> float:
        return self._hauteur

    @hauteur.setter
    def hauteur(self, valeur: float) -> None:
        if valeur <= 0:
            raise ValueError("La hauteur doit être positive.")
        self._hauteur = valeur

    @property
    def volume(self) -> float:
        """Retourne le volume du cylindre."""
        return self.surface * self.hauteur

    def __str__(self) -> str:
        return f"Le cylindre de rayon {self.rayon:.2f} et de hauteur {self.hauteur:.2f} a un volume de {self.volume:.2f}"