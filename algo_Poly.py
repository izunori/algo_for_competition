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

def polyDiff(f,MOD=998244353):
    return [(n*a)%MOD for n,a in enumerate(f[1:], 1)]

def test():
    import random
    MOD = 998244353
    K = 100
    N = random.randint(1,K)
    f = [random.randint(0,MOD-1) for _ in range(N)]
    r = random.randint(N,K)
    g = polyInv(f,r)
    nnt = NNT(998244353)
    ans = [1]+[0]*(r-1)
    res = nnt.polymul(f,g)[:r]
    if ans == res:
        print('OK')
    else:
        print(f,r)

def testDiff():
    f = [2,3,4,5]
    ans = [3,8,15]
    res = polyDiff(f)
    print(res==ans)

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
    testDiff()

