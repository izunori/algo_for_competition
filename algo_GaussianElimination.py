# inplace
MOD = 998244353

def dprint(G):
    print()
    [print(row) for row in G]

def GaussianElimination(G):
    H,W = len(G),len(G[0])

    cache = [0]*W
    for w in range(W):
        for h in range(w,H):
            if G[h][w] != 0:
                G[w],G[h] = G[h],G[w]
                break
        else:
            continue
        p = G[w][w]
        rp = pow(p, MOD-2, MOD)
        for w2 in range(w,W):
            cache[w2] = G[w][w2]*rp%MOD
        for h2 in range(w+1,H):
            if G[h2][w] != 0:
                for w2 in range(W-1,w-1,-1):
                    G[h2][w2] = (G[h2][w2] - G[h2][w]*cache[w2]) % MOD

# return the number of x which satisfies Ax=b
def dimOfSolveSpace(A,b):
    for row,s in zip(A,b):
        row.append(s)

    GaussianElimination(A)

    n_cons = 0
    for *row,b in A[::-1]:
        if not any(row) and b:
            return -1
        if row:
            n_cons += 1
    return len(A) - n_cons

def test():
    G = [
            [ 3, 2,-4],
            [ 2, 4, 8],
            [ 3, 6, 12],
        ]
    GaussianElimination(G)
    dprint(G)

def testNoSolution():
    A = [
            [ 3, 2,-4],
            [ 2, 4, 8],
            [ 6, 4, -8],
        ]
    b = [1, 14, 3]
    n = dimOfSolveSpace(A,b)
    print(f"{n}=={-1}")

def perf():
    import random
    from time import perf_counter as time
    N = 200
    A = [[random.randint(0,MOD-1) for _ in range(N)] for _ in range(N)]
    start = time()
    GaussianElimination(A)
    print(f"{time()-start}")

if __name__=='__main__':
    test()
    testNoSolution()
    perf()
