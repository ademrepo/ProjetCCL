# Documentation de la partie DFS

Cette partie traite l'étiquetage des composantes connexes (CCL) d'une image binaire avec un parcours en profondeur (DFS), en deux versions : itérative (pile explicite) et récursive. Les deux marchent en 4-connexité et en 8-connexité.

## 1. Les fichiers

| Fichier | Rôle |
|---|---|
| `dfs_iteratif.py` | La fonction `dfs_iteratif(I, connexite)`, DFS avec une pile gérée à la main |
| `dfs_recursif.py` | La fonction `dfs_recursif(I, connexite)`, DFS avec une fonction qui s'appelle elle-même |
| `test_exemple.py` | Vérifie les deux fonctions sur l'exemple 5×6 de l'énoncé et sur quelques cas limites |
| `bench_dfs.py` | Mesure le temps et la mémoire des deux DFS et écrit un CSV. **Attend le générateur d'images du groupe et le vérificateur** (voir section 9) |

## 2. Entrée et sortie

- **Entrée `I`** : liste de listes de 0 et 1, de taille H × W. 0 = fond, 1 = objet.
- **Entrée `connexite`** : 4 ou 8. Toute autre valeur lève une `ValueError`.
- **Sortie `(L, n)`** :
  - `L` : image étiquetée, même taille que `I`. Le fond reste à 0, chaque tache a un entier > 0 différent.
  - `n` : nombre de taches.

Les labels sont donnés dans l'ordre de découverte (balayage ligne par ligne, de haut en bas et de gauche à droite), donc 1, 2, 3, ... n sans trou. C'est ce qui permet de retrouver exactement l'image de l'énoncé.

## 3. Le voisinage

```python
VOISINS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
VOISINS_8 = VOISINS_4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]
```

Chaque couple est un décalage `(dx, dy)` à ajouter à la position `(x, y)` du pixel courant. En 4-connexité on regarde haut, bas, gauche, droite. En 8-connexité on ajoute les quatre diagonales. Le paramètre `connexite` choisit simplement la liste : c'est pour cela qu'un seul code donne les 4 versions demandées (itératif/récursif × 4/8).

Un voisin `(a, b)` est utilisable si les trois conditions sont vraies :
1. il est dans l'image : `0 <= a < H and 0 <= b < W` ;
2. c'est un pixel d'objet : `I[a][b] == 1` ;
3. il n'a pas encore de label : `L[a][b] == 0`.

La condition 3 remplace une matrice « visités » : `L` joue ce rôle, comme l'énoncé le suggère (`I(i,j) = 1 et L(i,j) = 0`).

## 4. L'algorithme général (commun aux deux versions)

```
L = matrice H×W remplie de 0
n = 0
pour chaque pixel (i, j) :
    si I[i][j] == 1 et L[i][j] == 0 :      # nouvelle tache
        n = n + 1
        colorier toute la tache de (i, j) avec le label n   # le DFS
retourner (L, n)
```

Il y a donc deux niveaux : la double boucle trouve les taches, le DFS colorie une tache complète. L'image des « visités » est `L` elle-même.

## 5. `dfs_iteratif`

```python
for i in range(H):
    for j in range(W):
        if I[i][j] == 1 and L[i][j] == 0:
            n += 1
            L[i][j] = n
            pile = [(i, j)]
            while pile:
                x, y = pile.pop()
                for dx, dy in voisins:
                    a, b = x + dx, y + dy
                    if 0 <= a < H and 0 <= b < W and I[a][b] == 1 and L[a][b] == 0:
                        L[a][b] = n
                        pile.append((a, b))
```

- `pile` est une simple liste Python. `append` ajoute à la fin et `pop()` retire à la fin : c'est bien une pile (dernier entré, premier sorti), ce qui donne un parcours en profondeur.
- On donne le label au pixel de départ avant de le mettre dans la pile.
- Tant que la pile n'est pas vide : on retire un pixel, on regarde chacun de ses voisins, et chaque voisin utilisable reçoit tout de suite le label `n` puis entre dans la pile.
- Quand la pile est vide, tous les pixels de la tache ont été coloriés.

**Pourquoi le label est donné à l'ajout et pas au retrait.** Si on attendait le `pop` pour étiqueter, un pixel pourrait être ajouté plusieurs fois (une fois par chaque voisin déjà traité qui le voit) avant d'être retiré, puisque son `L` serait encore 0. La pile grossirait pour rien et on referait du travail. En étiquetant à l'ajout, chaque pixel entre dans la pile au plus une fois.

## 6. `dfs_recursif`

```python
def dfs(x, y, label):
    L[x][y] = label
    for dx, dy in voisins:
        a, b = x + dx, y + dy
        if 0 <= a < H and 0 <= b < W and I[a][b] == 1 and L[a][b] == 0:
            dfs(a, b, label)
```

- La fonction étiquette le pixel courant, puis s'appelle sur chaque voisin utilisable.
- Ici la « pile » est la pile d'appels de Python : chaque appel en cours en occupe un cadre.
- `dfs` est définie à l'intérieur de `dfs_recursif` pour accéder à `L`, `I`, `H`, `W` et `voisins` sans les repasser en paramètre.
- La boucle principale est la même que pour la version itérative : à chaque nouvelle tache, `n += 1` puis `dfs(i, j, n)`.

**Limite.** La profondeur de récursion peut atteindre la longueur du plus long chemin dans une tache, donc jusqu'à environ H × W (une tache en serpentin). Python limite la profondeur à environ 1000 appels par défaut (`sys.getrecursionlimit()`). Au-delà, on obtient une `RecursionError`. Augmenter la limite avec `sys.setrecursionlimit` retarde le problème mais ne le règle pas : en dépassant ce que la pile système supporte, le programme peut planter. C'est la raison d'être de la version itérative.

## 7. Exemple pas à pas (4-connexité)

```
I =  1 1 0
     0 1 0
     0 0 1
```

Le balayage trouve (0,0) : c'est un 1 sans label, donc `n = 1`, `L[0][0] = 1`, `pile = [(0,0)]`.

| Étape | Pixel retiré | Ce qui se passe | Pile après |
|---|---|---|---|
| 1 | (0,0) | Le voisin (0,1) vaut 1 : label 1, ajouté | [(0,1)] |
| 2 | (0,1) | Le voisin (1,1) vaut 1 : label 1, ajouté | [(1,1)] |
| 3 | (1,1) | Voisins déjà étiquetés ou à 0 : rien à ajouter | [] |

La tache 1 est terminée. Le balayage continue et trouve (2,2), qui vaut 1 sans label, donc `n = 2`. Ce pixel est en diagonale de (1,1) : en 4-connexité c'est une autre tache, en 8-connexité il aurait fait partie de la tache 1 et on aurait eu `n = 1`.

```
L =  1 1 0
     0 1 0
     0 0 2
```

## 8. Complexité

Notations : H hauteur, W largeur, N = H × W nombre de pixels, k = 4 ou 8 (taille du voisinage).

### Temps : O(H × W)

- Création de `L` : O(N).
- Le balayage regarde chaque pixel une fois : O(N).
- Chaque pixel d'objet est étiqueté une seule fois, donc entre au plus une fois dans la pile (ou fait l'objet d'un seul appel récursif). Pour chacun on teste k voisins, avec k constant : O(k × N) = O(N).
- Total : O(N), pour les deux versions. En 8-connexité la constante est plus grande (8 tests au lieu de 4) mais l'ordre de grandeur est le même.

### Mémoire : O(H × W)

| Structure | Contenu | Taille |
|---|---|---|
| `I` (image) | Matrice H × W de 0/1 (liste de listes) | O(N) |
| `L` (labels) | Matrice H × W d'entiers, sert aussi de « visités » | O(N) |
| Visités | Pas de structure à part : `L[x][y] == 0` signifie « pas encore visité » | 0 en plus |
| Composantes | Un simple compteur `n` | O(1) |
| `pile` (itératif) | Liste de couples (x, y) | au plus le nombre de pixels d'objet, donc O(N) au pire |
| Pile d'appels (récursif) | Un cadre par appel en cours | profondeur maximale, jusqu'à O(N) au pire |

Total : O(N) dans les deux cas (sans compter l'image d'entrée, qui est elle aussi en O(N)).

**Nuance entre les deux versions.** Le pire cas n'est pas le même :
- Pour le récursif, le pire cas est une grande tache en serpentin (chemin long et fin) : la profondeur approche H × W / 2.
- Pour l'itératif, la pile contient les pixels trouvés mais pas encore traités ; sur un serpentin elle reste très petite. Elle grossit surtout sur des zones larges et pleines, mais reste bornée par le nombre de pixels d'objet puisque chaque pixel y entre au plus une fois.
- À taille de pile égale, un cadre d'appel récursif coûte beaucoup plus de mémoire qu'un simple couple `(x, y)` dans une liste.

## 9. Mesures : `bench_dfs.py`

- `mesurer_temps` : `time.perf_counter`, on garde le meilleur de 3 répétitions.
- `mesurer_memoire` : `tracemalloc`, on garde le pic de mémoire alloué pendant l'appel (cela inclut `L` et la pile, pas l'image d'entrée qui existe déjà).
- Le temps et la mémoire sont mesurés dans deux appels séparés, car `tracemalloc` ralentit l'exécution.
- Si le récursif dépasse la limite de Python, la ligne du CSV a des valeurs vides et un message est affiché.
- Le CSV a les colonnes `algorithme, connexite, H, W, densite, temps_s, memoire_ko`, le même format à utiliser dans tout le groupe pour pouvoir fusionner les résultats.

**À faire avant de lancer de vraies mesures :**
1. Attendre le générateur d'images du groupe pour que tous les algorithmes soient comparés sur les mêmes images.
2. Passer chaque résultat dans le vérificateur : une mesure faite sur un résultat faux n'a aucune valeur.

`bench_dfs.py` ne contient donc aucun générateur : `benchmark(images, "resultats.csv")` reçoit une liste de `(I, densite)`.

## 10. Tests

`test_exemple.py` vérifie les deux fonctions, en 4 et en 8-connexité, sur :
- l'exemple 5×6 de l'énoncé (4 taches, labels 1 à 4) ;
- une diagonale `[[1,0],[0,1]]` : 2 taches en 4-connexité, 1 en 8 ;
- une image vide, une image toute à 0, une image toute à 1, un seul pixel.

Ce test compare à des réponses écrites à la main sur de petites images. Il ne remplace pas le vérificateur, qui contrôle n'importe quelle image sans réponse attendue.

Lancer : `python test_exemple.py` dans le dossier `dfs`.

## 11. Questions probables à l'oral

- **Pourquoi donner le label à l'ajout dans la pile ?** Pour qu'un pixel n'entre qu'une fois dans la pile (section 5).
- **Pourquoi pas de matrice « visités » ?** `L[x][y] == 0` indique déjà qu'un pixel n'a pas été traité (section 3).
- **Quelle est la différence entre itératif et récursif ?** C'est la même idée. Dans l'un on gère la pile, dans l'autre c'est Python qui gère la pile d'appels, qui est limitée (section 6).
- **Quand le récursif plante-t-il ?** Quand la profondeur dépasse la limite de Python (~1000), par exemple sur une grande tache en serpentin.
- **Pourquoi la complexité est la même en 4 et en 8 ?** Le nombre de voisins est une constante : 8 au lieu de 4 change la constante, pas l'ordre de grandeur.
- **Que change la connexité sur le résultat ?** En 8, des pixels en diagonale sont reliés : il y a moins ou autant de taches qu'en 4.
