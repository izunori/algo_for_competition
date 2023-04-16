from algo_nnt import NNT
from itertools import zip_longest
MOD = 998244353
nnt = NNT()
def polyInv(f,r=-1):
    assert f[0] != 0
    r = r if r > 0 else len(f)
    if r <= 6750 or len(f) <= 400:
        return polyInvSimple(f,r)
    return polyInvNNT(f,r)
def polyInvNNT(f, r=-1):
    r = r if r > 0 else len(f)
    f = f + [0]*(r-len(f))
    g = [pow(f[0],MOD-2,MOD)]
    m = 1
    while m < r:
        h = nnt.polymul(f[:2*m],g)[m:2*m]
        ng = [(-x%MOD) for x in nnt.polymul(h,g)]
        g = g + ng[:m]
        m *= 2
    return g[:r]
def polyInvSimple(f,r=-1):
    assert f[0] != 0
    r = r if r > 0 else len(f)
    g = [0]*r
    g[0] = pow(f[0],MOD-2,MOD)
    for n in range(1,r):
        for i in range(1,min(n+1,len(f))):
            g[n] = (g[n]+f[i]*g[n-i])%MOD
        g[n] = (-g[n]*g[0])%MOD
    return g

def polyAdd(f,g):
    return [(x+y)%MOD for x,y in zip_longest(f,g,fillvalue=0)]

def polyDiff(f):
    return [(n*a)%MOD for n,a in enumerate(f[1:], 1)]

def polyInt(f):
    return [0] + [x * pow(i,MOD-2,MOD) % MOD for i,x in enumerate(f,1)]

def polyDiv(f, g):
    while g[-1] == 0 : # TODO Refact
        g.pop()
    n,m = len(f),len(g)
    if n < m:
        return 0,f
    nnt = NNT()
    q = nnt.polymul(f[::-1], polyInv(g[::-1],n))[n-m::-1]
    gq = nnt.polymul(g,q[:m-1])
    r = [(a-b)%MOD for a,b in zip(f,gq[:m-1])]
    return q,r

def testInv():
    print("--test Inversion")
    import random
    K = random.randint(100,200)
    N = random.randint(1,K)
    f = [random.randint(0,MOD-1) for _ in range(N)]
    r = random.randint(N,K)
    g = polyInv(f,r)
    nnt = NNT()
    ans = [1]+[0]*(r-1)
    res = nnt.polymul(f,g)[:r]
    if ans == res:
        print('OK')
    else:
        print(f,r)

# f[0] must be 1
def polyLog(f):
    assert f[0] == 1
    df = polyDiff(f)
    rf = polyInv(f)
    dfrf = nnt.polymul(df,rf)
    return polyInt(dfrf)[:len(f)+1]

# f[0] must be 0
def polyExp(f):
    assert f[0] == 0
    g = [1]
    m,r = 1,len(f)
    while m < r:
        h = [-x+y for x,y in zip_longest(polyLog(g),f[:2*m+1],fillvalue=0)]
        h[0] += 1
        g = nnt.polymul(g,h)
        m *= 2
    return g[:r]
    

def perfInv():
    print("--perf Inversion")
    import random
    from time import perf_counter as time
    N = 2*10**4
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

def testLog():
    print("--test log")
    import random
    N = 100
    f = [random.randint(0,MOD-1) for _ in range(N)]
    g = [random.randint(0,MOD-1) for _ in range(N)]
    f[0] = 1
    g[0] = 1
    logf = polyLog(f)
    logg = polyLog(g)
    fg = nnt.polymul(f,g)
    logfg = polyLog(fg)
    for x,y in zip(polyAdd(logf,logg), logfg):
        if x != y:
            print('Fail')
            break
    else:
        print('OK')

def testExp():
    print("---test exp")
    import random
    N = 100
    f = [random.randint(0,MOD-1) for _ in range(N)]
    g = [random.randint(0,MOD-1) for _ in range(N)]
    f[0] = 0
    g[0] = 0
    expf = polyExp(f)
    expg = polyExp(g)
    expf_g = polyExp(polyAdd(f,g))
    expfexpg = nnt.polymul(expf,expg)
    for x,y in zip(expf_g, expfexpg):
        if x != y:
            print('Fail')
            break
    else:
        print('OK')

def testDiff():
    print("--test Diff")
    f = [2,3,4,5]
    ans = [3,8,15]
    res = polyDiff(f)
    print(res==ans)

def testDiv():
    print("--test Division")
    import random
    N = 5
    M = random.randint(1,N)
    f = [random.randint(0,MOD-1) for _ in range(N)]
    g = [random.randint(0,MOD-1) for _ in range(M)]
    q,r = polyDiv(f,g)
    nnt = NNT()
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

    N = 2*10**5
    M = N//2
    f = [random.randint(0,MOD-1) for _ in range(N)]
    g = [random.randint(0,MOD-1) for _ in range(M)]

    start=time()
    q,r=polyDiv(f,g)
    print(f"{time()-start}") 


if __name__=='__main__':
    testInv()
    testDiff()
    testDiv()
    testLog()
    testExp()
    #perfInv()
    #perfDiv()

