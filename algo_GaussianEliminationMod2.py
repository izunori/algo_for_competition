def GaussianEliminationMod2(G):
    H,W = len(G),len(G[0])

    for w in range(W):
        for h in range(w,H):
            if G[h][w]:
                G[w],G[h] = G[h],G[w]
                break
        else:
            continue
        for h2 in range(w+1,H):
            if G[h2][w]:
                for w2 in range(W-1,w-1,-1):
                    G[h2][w2] = (G[h2][w2] ^ (G[h2][w] & G[w][w2]))

def dimOfSolveSpace(A,b):
    H = len(A)
    W = len(A[0])

    for row,x in zip(A,b):
        row.append(x)

    GaussianEliminationMod2(A)

    n_cons = 0
    for *row,b in A[::-1]:
        if not any(row) and b:
            return -1
        if row:
            n_cons += 1
    return len(A) - n_cons

def test():
    A = [
            [1,0,1],
            [1,1,1],
            [1,0,0],
        ]
    b = [0, 0, 1]
    n = dimOfSolveSpace(A,b)
    print(f"{n}==1")

def perf():
    import random
    from time import perf_counter as time
    H = 10
    W = 10
    A = [[random.randint(0,1) for w in range(W)] for h in range(H)]
    b = [random.randint(0,1) for h in range(H)]
    start = time()
    n = dimOfSolveSpace(A,b)
    print(n)
    print(f"{(time()-start)*1000}ms")

if __name__=='__main__':
    test()
    #perf()
