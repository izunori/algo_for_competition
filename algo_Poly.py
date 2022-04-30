from algo_nnt import NNT
def polyInv(f, r=-1, MOD=998244353):
    r = r if r > 0 else len(f)
    f = f + [0]*(r-len(f))
    g = [pow(f[0],MOD-2,MOD)]
    nnt = NNT(MOD)
    m = 1
    while m < r:
        h = nnt.polymul(f[:2*m],g)[m:2*m]
        ng = [(-x%MOD) for x in nnt.polymul(h,g)]
        g = g + ng[:m]
        m *= 2
    return g[:r]

def test():
    f = [3,-2,3,-400,5,6]
    g = polyInv(f)
    nnt = NNT(998244353)
    print(nnt.polymul(f,g))

def perf():
    from time import perf_counter as time
    import random
    MOD = 998244353
    N = 10**5
    f = [random.randint(0,MOD-1) for _ in range(N)]
    start = time()
    g = polyInv(f)
    #nnt = NNT()
    #print(nnt.polymul(f,g)[:N])
    print(f"{time() - start}")

if __name__=='__main__':
    test()
    perf()

