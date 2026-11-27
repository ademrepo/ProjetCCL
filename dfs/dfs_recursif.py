VOISINS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
VOISINS_8 = VOISINS_4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def dfs_recursif(I, connexite=4):
    if connexite == 4:
        voisins = VOISINS_4
    elif connexite == 8:
        voisins = VOISINS_8
    else:
        raise ValueError("connexite doit valoir 4 ou 8")

    H = len(I)
    W = len(I[0]) if H > 0 else 0
    L = [[0] * W for _ in range(H)]

    def dfs(x, y, label):
        L[x][y] = label
        for dx, dy in voisins:
            a, b = x + dx, y + dy
            if 0 <= a < H and 0 <= b < W and I[a][b] == 1 and L[a][b] == 0:
                dfs(a, b, label)

    n = 0
    for i in range(H):
        for j in range(W):
            if I[i][j] == 1 and L[i][j] == 0:
                n += 1
                dfs(i, j, n)
    return L, n
