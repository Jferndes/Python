"""
Exercice H: Créer un DataFrame avec des étiquettes d'index personnalisées
"""

import pandas as pd
import numpy as np

# Données de l'examen
exam_data = {
    'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 
             'Michael', 'Matthew', 'Laura', 'Kevin', 'Jonas'],
    'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
    'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
    'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']
}

# Étiquettes d'index
labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

# Création du DataFrame avec index personnalisé
df = pd.DataFrame(exam_data, index=labels)

print("DataFrame avec index personnalisé:")
print(df)