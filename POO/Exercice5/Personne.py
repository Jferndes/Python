class Personne:
    def __init__(self, nom: str = None, age: str = None, **kwargs):
        # accept kwargs for cooperative multiple inheritance
        self.nom = nom
        self.age = age
        super().__init__(**kwargs)

    def se_presenter(self):
        return f"Je m'appelle {self.nom} et j'ai {self.age} ans."