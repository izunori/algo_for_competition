# G = [A|b]

def GaussianEliminationBit(G):
    # deprecated
    H = len(G)

    done = [False]*H
    for w in range(W):
        c = 1<<w
        for h in range(H):
            if not done[h] and G[h]&c:
                done[h] = True
                for h2 in range(H):
                    if G[h2]&c and h != h2:
                        G[h2] ^= G[h]
    return G, done

def GaussianEliminationMod2(G):
    H = len(G)
    W = len(G[0])-1

    done = [False]*H
    for w in range(W):
        for h in range(H):
            if not done[h] and G[h][w]:
                done[h] = True
                for h2 in range(H):
                    if G[h2][w] and h != h2:
                        for w2 in range(W+1):
                            G[h2][w2] ^= G[h][w2]
    return G, done

def Ab2G(A,b):
    G = []
    for a,s in zip(A,b):
        v = 0
        for i,t in enumerate(a[::-1]):
            if t:
                v += (1<<i)
        v = (v<<1) + s
        G.append(v)
    return G

def num_of_sol_mod2(A,b):
    H = len(A)
    W = len(A[0])

    for row,x in zip(A,b):
        row.append(x)

    G, done = GaussianEliminationMod2(A)

    for z_row, dn in zip(G,done):
        if not dn and z_row[-1] == 1:
            return 0
    rank = sum(done)
    return pow(2, W - rank)

def test():
    A = [
            [1,0,1],
            [0,1,1],
            [1,0,0],
        ]
    b = [0, 0, 1]
    n = num_of_sol_mod2(A,b)
    print(f"{n}==1")

def perf():
    import random
    from time import perf_counter as time
    H = 10
    W = 10
    A = [[random.randint(0,1) for w in range(W)] for h in range(H)]
    b = [random.randint(0,1) for h in range(H)]
    start = time()
    n = num_of_sol_mod2(A,b)
    print(n)
    print(f"{(time()-start)*1000}ms")

if __name__=='__main__':
    test()
    #perf()
