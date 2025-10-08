from Personne import Personne

class Employe(Personne):
    def __init__(self, nom: str = None, age: str = None, salaire: float = None, poste: str = None, **kwargs):
        # pass nom and age to Personne via super(); accept kwargs for cooperative MRO
        super().__init__(nom=nom, age=age, **kwargs)
        self.poste = poste
        self.salaire = salaire

    def sePresenter(self):
        return f"{super().se_presenter()} Je travaille comme {self.poste}."