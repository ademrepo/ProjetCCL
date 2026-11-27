from dfs_iteratif import dfs_iteratif
from dfs_recursif import dfs_recursif

I = [
    [1, 1, 0, 0, 1, 0],
    [1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 1, 0],
]
L_ATTENDU = [
    [1, 1, 0, 0, 2, 0],
    [1, 0, 0, 2, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [3, 3, 0, 4, 0, 0],
    [0, 3, 0, 4, 4, 0],
]

DIAGONALE = [[1, 0], [0, 1]]

for nom, f in [("dfs_iteratif", dfs_iteratif), ("dfs_recursif", dfs_recursif)]:
    for c in (4, 8):
        L, n = f(I, c)
        assert n == 4 and L == L_ATTENDU, (nom, c, L, n)

    assert f(DIAGONALE, 4) == ([[1, 0], [0, 2]], 2), nom
    assert f(DIAGONALE, 8) == ([[1, 0], [0, 1]], 1), nom
    assert f([], 4) == ([], 0), nom
    assert f([[0, 0], [0, 0]], 8) == ([[0, 0], [0, 0]], 0), nom
    assert f([[1, 1], [1, 1]], 4) == ([[1, 1], [1, 1]], 1), nom
    assert f([[1]], 4) == ([[1]], 1), nom
    print(nom, ": OK (4 et 8-connexite)")

