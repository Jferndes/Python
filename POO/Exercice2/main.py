from POO.Exercice3.Animal import Animal
from Chien import Chien

if __name__ == '__main__':
    animal = Animal("Générique")
    chien = Chien("Rex")

    animal.parler()  # Affiche "..."
    chien.parler()   # Affiche "Woof!"