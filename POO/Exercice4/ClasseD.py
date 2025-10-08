from ClasseB import ClasseB
from ClasseC import ClasseC

class ClasseD(ClasseB, ClasseC):
    def __init__(self):
        super().__init__()