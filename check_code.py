import subprocess



def run_bandit():
    print("Lancement de l'analyse statique avec Bandit..")

    try:
        result = (subprocess.run(["bandit","-r","."],
            text=True,
            capture_output=True,
            check=False))

        print(result.stdout)
        if result.returncode != 0:
                print("Bandit a détecté des problèmes de sécurité.")
        else:
                print("Aucun problème de sécurité détecté par Bandit.")
    except FileNotFoundError:
        print("Erreur : Bandit n'est pas installé. Veuillez l'installer via 'pip install bandit'.")



print(run_bandit())