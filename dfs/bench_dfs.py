import csv
import time
import tracemalloc

from dfs_iteratif import dfs_iteratif
from dfs_recursif import dfs_recursif

# ATTENTION : ce fichier attend le generateur d'images du groupe et le verificateur.
# Il ne contient volontairement aucun generateur : on lui passe les images en entree.
# Ne pas lancer de vraies mesures avant que les resultats soient verifies.

ALGOS = {"dfs_iteratif": dfs_iteratif, "dfs_recursif": dfs_recursif}
COLONNES = ["algorithme", "connexite", "H", "W", "densite", "temps_s", "memoire_ko"]


def mesurer_temps(algo, I, connexite, repetitions=3):
    meilleur = None
    for _ in range(repetitions):
        debut = time.perf_counter()
        algo(I, connexite)
        duree = time.perf_counter() - debut
        if meilleur is None or duree < meilleur:
            meilleur = duree
    return meilleur


def mesurer_memoire(algo, I, connexite):
    tracemalloc.start()
    algo(I, connexite)
    _, pic = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pic / 1024


def benchmark(images, fichier_csv):
    # images : liste de tuples (I, densite)
    with open(fichier_csv, "w", newline="") as f:
        out = csv.writer(f)
        out.writerow(COLONNES)
        for I, densite in images:
            H = len(I)
            W = len(I[0]) if H > 0 else 0
            for nom, algo in ALGOS.items():
                for connexite in (4, 8):
                    try:
                        t = mesurer_temps(algo, I, connexite)
                        m = mesurer_memoire(algo, I, connexite)
                    except RecursionError:
                        print(nom, connexite, H, W, ": RecursionError")
                        t, m = "", ""
                    out.writerow([nom, connexite, H, W, densite, t, m])
