from Cercle import Cercle
from Cylindre import Cylindre
from Cone import Cone
from CercleV2 import CercleV2
from CylindreV2 import CylindreV2
from ConeV2 import ConeV2

def main():
    
    c1 = Cercle(3)
    print(c1.rayon)
    #print(c1._rayon)
    print(c1)

    cyl1 = Cylindre(3, 5)
    print(cyl1)

    cone1 = Cone(3, 5)
    print(cone1)

    c2 = CercleV2(3)
    print(c2.rayon)
    print(c2._rayon)
    print(c2)

    cyl2 = CylindreV2(3, 5)
    print(cyl2)

    cone2 = ConeV2(3, 5)
    print(cone2.volume)
    print(cone2)



if __name__ == '__main__':
    main()
