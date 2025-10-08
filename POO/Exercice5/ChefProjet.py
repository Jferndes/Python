from Manager import Manager
from Employe import Employe

class ChefProjet(Manager, Employe):
    def __init__(self, nom: str, age: str, salaire: float, poste: str, equipe: list[Employe], projet: str, **kwargs):
        # Use cooperative multiple inheritance via super()
        super().__init__(nom=nom, age=age, salaire=salaire, poste=poste, equipe=equipe, **kwargs)
        self.projet = projet

    def sePresenter(self):
        return f"{Employe.sePresenter(self)} Je gère le projet '{self.projet}' avec une équipe de {len(self.equipe)} personnes."