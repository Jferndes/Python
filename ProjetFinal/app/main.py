from src.Controlleur import *

def run_menu():
    options = {
        "1": ("Analyser le sport Linéaire", "analyseSportLineaire"),
        "2": ("Analyser le sport Multivariée", "analyseSportMultivariee"),
        "3": ("Analyser le travail", "analyseTravail"),
        "4": ("Sport et café le lendemain", "analyseSportEtCafeLendemain"),
        "5": ("Actif vs productivité", "analyseActifProductivite"),
        "6": ("Surcharge vs productivité", "analyseSurchargeProductivite"),
        "7": ("Équilibre du temps vs productivité", "analyseEquilibreTempsProductivite"),
        "8": ("Corrélation calories vs café", "analyseCorrelationCaloriesCafe"),
        "9": ("Sportifs: consommation de café", "analyseeSportifsConsommationCafe"),
        "0": ("Quitter", None),
    }

    while True:
        print("\n=== Menu d'analyse ===")
        for k in [str(i) for i in range(1, 9)]:
            if k in options:
                print(f"{k}. {options[k][0]}")
        print("0. Quitter")

        choix = input("Votre choix: ").strip()
        if choix in ("0", "q", "Q"):
            print("Au revoir.")
            break

        label, fn_name = options.get(choix, (None, None))
        if not fn_name:
            print("Choix invalide.")
            continue

        fn = globals().get(fn_name)
        if not callable(fn):
            print(f"Fonction '{fn_name}' introuvable. Vérifiez src/Controlleur.py")
            continue

        try:
            print(f"\n--- {label} ---")
            fn()
        except Exception as e:
            print(f"Erreur lors de l'exécution: {e}")
        finally:
            input("\nAppuyez sur Entrée pour revenir au menu...")

if __name__ == "__main__":
    print("### Start main ###")
    run_menu()
