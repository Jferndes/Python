import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

MET_VALUES = {
    'course': 9.8,
    'velo': 7.5,
    'natation': 8.0
}

def modeliserActiviteSimple(dfSport: pd.DataFrame, activite: str) -> None:
    # Filtrer les données pour l'activité
    dfActivite = dfSport[dfSport['activite'] == activite]
    dfActivite = dfActivite[['calories', 'duree', 'poids_kg']]
    print(dfActivite.head())

    X = dfActivite['duree'].values
    Y = dfActivite['calories'].values
    # Calcul de la régression linéaire
    slope, intercept, r_value, p_value, std_er = stats.linregress(X, Y)

    tracerRegression(X, Y, slope, intercept, activite)



def tracerRegression(X: np.ndarray, Y: np.ndarray, pente: float, ordonneeOrigine: float, activite: str) -> None:
    plt.figure(figsize=(10, 6))
    
    #Nuage de points
    plt.scatter(X, Y, color='blue', label='Données observées', alpha=0.5)

    #Droite de régression
    YReg = pente * X + ordonneeOrigine
    plt.plot(X, YReg, 'r', label='Régression linéaire \n y = {:.2f}x + {:.2f}'.format(pente, ordonneeOrigine))

    #Noms des axes et titre
    plt.xlabel('Durée (minutes)')
    plt.ylabel('Calories brûlées')
    plt.title(f'Régression linéaire des calories brulées par rapport à la durée de l\'activité : {activite}')
    plt.legend()

    #Grille
    plt.grid(True, alpha=0.3)

    #Sauvegarder le graphique
    plt.savefig(f'../app/resultats/RegressionLineaire_{activite}.png', dpi=300, bbox_inches='tight')

    #Afficher le graphique
    plt.show()

def modeliserActiviteMultivariee(dfSport: pd.DataFrame, activite: str):
    # Filtrer et sélectionner les colonnes utiles
    dfActivite = dfSport[dfSport['activite'] == activite][['calories', 'duree', 'poids_kg']].dropna()

    if dfActivite.shape[0] < 3:
        print("Pas assez de données pour la régression multiple.")
        return None

    # Variables explicatives (duree, poids) + biais (constante)
    X1 = dfActivite['duree'].to_numpy(dtype=float)
    X2 = dfActivite['poids_kg'].to_numpy(dtype=float)
    Y = dfActivite['calories'].to_numpy(dtype=float)

    X = np.column_stack([X1, X2, np.ones_like(X1)])

    # Moindres carrés
    beta, residuals, rank, s = np.linalg.lstsq(X, Y, rcond=None)
    a, b, c = beta

    # R^2
    Y_hat = X @ beta
    ss_res = float(np.sum((Y - Y_hat) ** 2))
    ss_tot = float(np.sum((Y - np.mean(Y)) ** 2))
    r2 = 0.0 if ss_tot == 0 else 1.0 - ss_res / ss_tot

    print(f"Régression multiple pour {activite}: calories = {a:.4f}*duree + {b:.4f}*poids + {c:.4f} (R²={r2:.3f})")

    tracerRegression3D(X1, X2, Y, a, b, c, activite, r2)
    return a, b, c, r2

def tracerRegression3D(X_duree: np.ndarray, X_poids: np.ndarray, Y: np.ndarray,
                       a: float, b: float, c: float, activite: str, r2: float | None = None) -> None:
    from matplotlib import cm

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Nuage de points
    ax.scatter(X_duree, X_poids, Y, color='blue', label='Données observées', alpha=0.5)

    # Plan de régression
    x_s = np.linspace(X_duree.min(), X_duree.max(), 20)
    y_s = np.linspace(X_poids.min(), X_poids.max(), 20)
    xx, yy = np.meshgrid(x_s, y_s)
    zz = a * xx + b * yy + c
    ax.plot_surface(xx, yy, zz, cmap=cm.Reds, alpha=0.4, edgecolor='none')

    # Axes et titre
    ax.set_xlabel('Durée (minutes)')
    ax.set_ylabel('Poids (kg)')
    ax.set_zlabel('Calories brûlées')
    titre = f"Régression linéaire multiple : {activite}\n" \
            f"z = {a:.2f}x + {b:.2f}y + {c:.2f}"
    if r2 is not None:
        titre += f" | R² = {r2:.3f}"
    ax.set_title(titre)
    ax.legend()

    # Sauvegarde et affichage
    plt.tight_layout()
    plt.savefig(f'../app/resultats/RegressionLineaireMultiple_{activite}.png', dpi=300, bbox_inches='tight')
    plt.show()


    correlation linéaire numpy
    correlation linéaire numpy
    correlation linéaire numpy