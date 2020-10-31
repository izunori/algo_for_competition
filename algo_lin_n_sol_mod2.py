def num_of_sol_mod2(A,b):
    H = len(A)
    W = len(A[0])

    G = []
    for a,s in zip(A,b):
        v = 0
        for i,t in enumerate(a[::-1]):
            if t:
                v += (1<<i)
        v = (v<<1) + s
        G.append(v)

    done = [False]*H
    for w in range(W,0,-1): # first digit is in b
        c = 1<<w
        for h in range(H):
            if not done[h] and c&G[h]:
                done[h] = True
                for h2 in range(H):
                    if not done[h2] and c&G[h2]:
                        G[h2] ^= G[h]
                break
    for z_row, _ in [(row, dn) for row,dn in zip(G,done) if not dn]:
        if (z_row % 2):
            # case : no solution
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
