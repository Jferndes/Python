from CylindreV2 import CylindreV2

class ConeV2(CylindreV2):
    """Représente un cône, hérite de Cylindre."""

    @property
    def volume(self) -> float:
        """Retourne le volume du cône."""
        return (1 / 3) * super().volume

    def __str__(self) -> str:
        return f"Le cône de rayon {self.rayon:.2f} et de hauteur {self.hauteur:.2f} a un volume de {self.volume:.2f}"