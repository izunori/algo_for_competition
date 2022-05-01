from algo_nnt import NNT
def polyInv(f,r=-1,MOD=998244353):
    assert f[0] != 0
    r = r if r > 0 else len(f)
    if r <= 2750 or len(f) <= 600:
        return polyInvSimple(f,r,MOD)
    return polyInvNNT(f,r,MOD)
def polyInvNNT(f, r=-1, MOD=998244353):
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
def polyInvSimple(f,r=-1,MOD=998244353):
    assert f[0] != 0
    r = r if r > 0 else len(f)
    g = [0]*r
    g[0] = pow(f[0],MOD-2,MOD)
    for n in range(1,r):
        for i in range(1,min(n+1,len(f))):
            g[n] = (g[n]+f[i]*g[n-i])%MOD
        g[n] = (-g[n]*g[0])%MOD
    return g

def polyDiff(f,MOD=998244353):
    return [(n*a)%MOD for n,a in enumerate(f[1:], 1)]

def polyDiv(f, g, MOD=998244353):
    while g[-1] == 0 : # TODO Refact
        g.pop()
    n,m = len(f),len(g)
    if n < m:
        return 0,f
    nnt = NNT(MOD)
    q = nnt.polymul(f[::-1], polyInv(g[::-1],n))[n-m::-1]
    gq = nnt.polymul(g,q[:m-1])
    r = [(a-b)%MOD for a,b in zip(f,gq[:m-1])]
    return q,r

def testInv():
    print("--test Inversion")
    import random
    MOD = 998244353
    K = random.randint(100,200)
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

def perfInv():
    print("--perf Inversion")
    import random
    from time import perf_counter as time
    MOD = 998244353
    N = 2*10**3
    f = [random.randint(0,MOD-1) for _ in range(N)]
    r = N

    start = time()
    g1 = polyInvNNT(f,r)
    print(f"{time() - start}")

    start = time()
    g2 = polyInvSimple(f,r)
    print(f"{time() - start}")

    start = time()
    g2 = polyInv(f,r)
    print(f"{time() - start}")
    print(g1==g2)

def testDiff():
    print("--test Diff")
    f = [2,3,4,5]
    ans = [3,8,15]
    res = polyDiff(f)
    print(res==ans)

def testDiv():
    print("--test Division")
    import random
    MOD = 998244353
    N = 5
    M = random.randint(1,N)
    f = [random.randint(0,MOD-1) for _ in range(N)]
    g = [random.randint(0,MOD-1) for _ in range(M)]
    q,r = polyDiv(f,g)
    nnt = NNT(MOD)
    gq = nnt.polymul(g,q)
    for i,x in enumerate(r):
        gq[i] = (gq[i]+x)%MOD
    for x,y in zip(f,gq):
        if x%MOD!=y%MOD:
            print('NG')
            return
    print('OK')

def perfDiv():
    print("--perf Division")
    import random
    from time import perf_counter as time

    MOD=998244353
    N = 2*10**5
    M = N//2
    f = [random.randint(0,MOD-1) for _ in range(N)]
    g = [random.randint(0,MOD-1) for _ in range(M)]

    start=time()
    q,r=polyDiv(f,g,MOD)
    print(f"{time()-start}") 


if __name__=='__main__':
    #testInv()
    #testInv() # JIT
    #testInv() # JIT
    #testInv() # JIT
    #testInv() # JIT
    #testDiff()
    testDiv()
    #perfInv()
    perfDiv()

