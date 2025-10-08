from Personne import Personne
from Employe import Employe

class Manager(Personne):
    def __init__(self, nom: str = None, age: str = None, equipe: list[Employe] = None, **kwargs):
        # cooperative init: forward nom/age and any other kwargs
        super().__init__(nom=nom, age=age, **kwargs)
        self.equipe = equipe or []  # liste d'objets Employe

    def sePresenter(self):
        return f"{super().se_presenter()} Je suis manager d'une équipe de {len(self.equipe)} personnes."