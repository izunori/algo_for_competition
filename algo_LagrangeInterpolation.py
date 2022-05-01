from algo_nnt import NNT
from algo_MultiPointEval import multiPointEval
from collections import deque
def LaglangeInterporation(xs,ys,MOD=998244353):
    nnt = NNT()
    res = [[(-x)%MOD,1] for x in xs]
    while len(res) > 1:
        nres = []
        while res:
            if len(res) > 1:
                nres.append(nnt.polymul(res.pop(),res.pop()))
            else:
                nres.append(res.pop())
        res = nres
    g = res[0]
    dg = [(i*a)%MOD for i,a in enumerate(g[1:],1)]
    dgxs = multiPointEval(dg,xs)
    a = [(y*pow(dgx,MOD-2,MOD)%MOD) for y,dgx in zip(ys,dgxs)]
    res = [([n],[-x,1]) for n,x in zip(a,xs)]
    while len(res) > 1:
        nres = []
        res.reverse()
        while res:
            if len(res) > 1:
                a0,d0 = res.pop()
                a1,d1 = res.pop()
                na0 = nnt.polymul(a0,d1)
                na1 = nnt.polymul(a1,d0)
                na = [(s+t)%MOD for s,t in zip(na0,na1)]
                nres.append((na, nnt.polymul(d0,d1)))
            else:
                nres.append(res.pop())
        res = nres
    return res[0][0]

class LaglangeInterporationWithArith:
    def __init__(self,xs,ys,MOD=998244353):
        self.xs = xs
        self.ys = ys
        self.MOD = MOD
        n = len(xs)
        a = (xs[1]-xs[0])
        fact = [1]
        for i in range(1,n):
            fact.append((fact[-1]*i)%MOD)
        self.ds = []
        an1 = pow(a,n-1,MOD)
        sign = 1 if n&1 else -1
        for i in range(n):
            t = sign*an1*fact[i]*fact[n-i-1]
            self.ds.append(pow(t,MOD-2,MOD))
            sign *= -1
    def get(self,c):
        nom,MOD = 1,self.MOD
        for x in self.xs:
            nom = (nom*(c-x))%MOD
        ns = [nom*pow(c-x,MOD-2,MOD) for x in self.xs]
        res = 0
        for t in ((((y*n)%MOD)*d)%MOD for y,n,d in zip(self.ys,ns,self.ds)):
            res = (res+t)%MOD
        return res

def poly(x,g,MOD=998244353):
    res = 0
    nx = 1
    for a in g:
        res += a*nx
        nx *= x
    return res % MOD

def test():
    MOD = 998244353
    xs = [0,-1,-3,1,23]
    f = lambda x: 2-3*x+x**2+10*x**3+x**4
    ys = [f(x)%MOD for x in xs]
    print(ys)
    g = LaglangeInterporation(xs,ys)
    print(g)
    print([poly(x,g) for x in xs])

def testArith():
    MOD = 998244353
    xs = [0,2,4,6]
    f = lambda x: 2-3*x+x**2+10*x**3
    ys = [f(x)%MOD for x in xs]
    lag = LaglangeInterporationWithArith(xs,ys)
    print(f(10),lag.get(10))
    print(f(-10)%MOD,lag.get(-10))


def perf():
    import random
    from time import perf_counter as time
    MOD = 998244353
    N = 10
    f = [random.randint(0,MOD-1) for _ in range(N)]
    xs = [random.randint(0,MOD-1) for _ in range(N)]
    ys = [poly(x,f) for x in xs]
    start = time()
    LaglangeInterporation(xs,ys)
    print(f"{time() - start}")

if __name__=='__main__':
    #test()
    #perf()
    testArith()

