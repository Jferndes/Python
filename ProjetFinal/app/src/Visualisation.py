import matplotlib.pyplot as plt
import numpy as np

'''
Tracé de la régression linéaire des calories brulées en fonction de la durée de l'activité
'''
def tracerRegression(X: np.ndarray, Y: np.ndarray, pente: float, ordonneeOrigine: float, activite: str, show: bool = False) -> None:
    plt.figure(figsize=(10, 6))
    
    #Nuage de points
    plt.scatter(X, Y, color='blue', label='Données observées', alpha=0.5)

    #Droite de régression
    YReg = pente * X + ordonneeOrigine
    plt.plot(X, YReg, 'r', label=f"Régression linéaire \n y = {pente:.2f}x {'+' if ordonneeOrigine >= 0 else '-'} {abs(ordonneeOrigine):.2f}")

    #Noms des axes et titre
    if activite == "productivité":
        plt.xlabel('Nombre de tasses de café (unités)')
        plt.ylabel('Productivité (unités)')
        plt.title('Régression linéaire de la productivité en fonction du nombre de tasses de café')
    else:
        plt.xlabel('Durée (minutes)')
        plt.ylabel('Calories brûlées (Kcal)')
        plt.title(f'Régression linéaire des calories brulées par rapport à la durée de l\'activité : {activite}')
    plt.legend()

    #Grille
    plt.grid(True, alpha=0.3)

    #Sauvegarder le graphique
    plt.savefig(f'../app/resultats/RegressionLineaire_{activite}.png', dpi=300, bbox_inches='tight')
    print(f"    Graphique de régression linéaire sauvegardé sous: '/app/resultats/RegressionLineaire_{activite}.png'")

    #Afficher le graphique
    if show:
        plt.show()
    plt.close()


'''
Tracé de la régression linéaire multivarié des calories brulées en fonction de la durée de l'activité
'''
def tracerRegression3D(X_duree: np.ndarray, X_poids: np.ndarray, Y: np.ndarray, a: float, b: float, c: float, activite: str, r2: float, show: bool = False) -> None:

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Nuage de points
    ax.scatter(X_duree, X_poids, Y, color='blue', label='Données observées', alpha=0.5, marker='x')

    # Plan de régression
    x_s = np.linspace(X_duree.min(), X_duree.max(), 20)
    y_s = np.linspace(X_poids.min(), X_poids.max(), 20)
    xx, yy = np.meshgrid(x_s, y_s)
    zz = a * xx + b * yy + c
    ax.plot_surface(xx, yy, zz, color='orange', alpha=0.4)

    # Axes et titre
    ax.set_xlabel('Durée (minutes)')
    ax.set_ylabel('Poids (kg)')
    ax.set_zlabel('Calories brûlées')
    titre = f"Régression linéaire multiple : {activite}\n" \
            f"z = {a:.2f}x {'+' if b >= 0 else '-'} {abs(b):.2f}y {'+' if c >= 0 else '-'} {abs(c):.2f}"
    if r2 is not None:
        titre += f" | R² = {r2:.3f}"
    ax.set_title(titre)
    ax.legend()

    # Sauvegarde et affichage
    plt.tight_layout()
    plt.savefig(f'../app/resultats/RegressionLineaireMultivariée_{activite}.png', dpi=300, bbox_inches='tight')
    print(f"    Graphique de régression linéaire sauvegardé sous: '/app/resultats/RegressionLineaireMultivariée_{activite}.png'")
    
    if show:
        plt.show()
    plt.close()

def tracerPolynome(X: np.ndarray, Y: np.ndarray, coeffs: np.ndarray, type: str, show: bool = False) -> None:
    plt.figure(figsize=(10, 6))
    
    #Nuage de points
    plt.scatter(X, Y, color='blue', label='Données observées', alpha=0.5)

    #Courbe du polynôme
    X_fit = np.linspace(X.min(), X.max(), 100)
    Y_fit = np.polyval(coeffs, X_fit)
    plt.plot(X_fit, Y_fit, 'r', label=f"Régression polynomiale \n y = {coeffs[0]:.2f}x² + {coeffs[1]:.2f}x + {coeffs[2]:.2f}")

    #Noms des axes et titre
    if type == "equilibre":
        plt.xlabel('Temps total (heures)')
        plt.ylabel('Productivité (unités)')
        plt.title('Régression polynomiale de la productivité en fonction du temps total')
    elif type == "productivite":
        plt.xlabel('Nombre de tasses de café (unités)')
        plt.ylabel('Productivité (unités)')
        plt.title('Régression polynomiale de la productivité en fonction du nombre de tasses de café')
    plt.legend()

    #Grille
    plt.grid(True, alpha=0.3)

    #Sauvegarder le graphique
    plt.savefig(f'../app/resultats/RegressionPolynomiale_{type}.png', dpi=300, bbox_inches='tight')
    print(f"    Graphique de régression polynomiale sauvegardé sous: '/app/resultats/RegressionPolynomiale_{type}.png'")

    #Afficher le graphique
    if show:
        plt.show()
    plt.close()
