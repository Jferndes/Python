from math import pi

class CercleV2:
    """Représente un cercle défini par son rayon."""

    def __init__(self, rayon: float) -> None:
        if rayon <= 0:
            raise ValueError("Le rayon doit être positif.")
        self._rayon = rayon

    @property
    def rayon(self) -> float:
        return self._rayon

    @rayon.setter
    def rayon(self, valeur: float) -> None:
        if valeur <= 0:
            raise ValueError("Le rayon doit être positif.")
        self._rayon = valeur

    @property
    def surface(self) -> float:
        """Retourne la surface du cercle."""
        return pi * self.rayon**2

    def __str__(self) -> str:
        return f"Le cercle de rayon {self.rayon:.2f} a une surface de {self.surface:.2f}"