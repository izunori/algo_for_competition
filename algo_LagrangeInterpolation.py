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

def test():
    MOD = 998244353
    xs = [0,-1,-3,1,23]
    f = lambda x: 2-3*x+x**2+10*x**3+x**4
    ys = [f(x)%MOD for x in xs]
    print(ys)
    g = LaglangeInterporation(xs,ys)
    print(g)
    def h(x):
        res = 0
        nx = 1
        for a in g:
            res += a*nx
            nx *= x
        return res % MOD
    print([h(x) for x in xs])

if __name__=='__main__':
    test()



