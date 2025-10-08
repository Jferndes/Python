from ChefProjet import ChefProjet
from Manager import Manager
from Employe import Employe
from Personne import Personne

if __name__ == "__main__":
    # Créer des employés
    emp1 = Employe(nom="Alice", age="30", salaire=50000, poste="Développeuse")
    emp2 = Employe(nom="Bob", age="35", salaire=55000, poste="Designer")
    emp3 = Employe(nom="Charlie", age="28", salaire=48000, poste="Testeur")

    # Créer un manager avec une équipe
    manager = Manager(nom="David", age="40", equipe=[emp1, emp2])

    # Créer un chef de projet avec une équipe et un projet
    chef_projet = ChefProjet(nom="Eve", age="38", salaire=70000, poste="Chef de Projet",
                             equipe=[emp1, emp2, emp3], projet="Nouveau Site Web")

    # Présentations
    print(emp1.sePresenter())
    print(manager.sePresenter())
    print(chef_projet.sePresenter())