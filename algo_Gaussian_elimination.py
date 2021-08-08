# return the number of x which satisfies Ax=b
def num_of_sol(A,b,MOD):
    H = len(A)
    W = len(A[0])

    G = A[:]
    for a,s in zip(G,b):
        a.append(s)

    done = [False]*H
    for w in range(W):
        for h in range(H):
            if not done[h] and G[h][w] != 0:
                p = G[h][w]
                rp = pow(p, MOD-2, MOD)
                for w2 in range(W+1):
                    G[h][w2] = (rp*G[h][w2] % MOD) # p -> 1
                done[h] = True
                for h2 in range(H):
                    if not done[h2]:
                        s = G[h2][w]
                        for w2 in range(W+1):
                            G[h2][w2] = (G[h2][w2] - s*G[h][w2]) % MOD
                break
    for z_row, _ in [(row, dn) for row,dn in zip(G,done) if not dn]:
        if z_row[-1] != 0:
            # case : no solution
            return 0
    rank = sum(done)
    return pow(MOD, W - rank)

def test():
    MOD = 101
    A = [
            [ 3, 2,-4],
            [ 2, 4, 8],
            [ 3, 6, 12],
        ]
    b = [1, 14, 21]
    n = num_of_sol(A,b,MOD)
    print(f"{n}=={MOD}")

def perf():
    import random
    from time import perf_counter as time
    H = 300
    W = 300
    M = 100
    MOD = 10**9+7
    A = [[random.randint(-M,M) for w in range(W)] for h in range(H)]
    b = [random.randint(-M,M) for h in range(H)]
    start = time()
    n = num_of_sol(A,b,MOD)
    print(f"{(time()-start)*1000}ms")

if __name__=='__main__':
    test()
    #perf()
