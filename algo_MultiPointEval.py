from algo_nnt import NNT
from algo_Poly import *

def multiPointEval(f, xs, MOD=998244353):
    n = len(xs)
    l = 2**(n-1).bit_length()
    def simpleProd(xs):
        n = len(xs)
        l = 2**(n-1).bit_length()
        res = [[-x,1] for x in xs]+[[1,0] for _ in range(l-n)]
        nnt = NNT()
        for i in range(0,2*l-2,2):
            res.append(nnt.polymul(res[i],res[i+1]))
        return res
    tree = simpleProd(xs)
    res = [0]*(2*l)
    root = tree.pop()
    _,r = polyDiv(f, root)
    res = [r]
    i = 0
    while tree:
        f = res[i]
        right = tree.pop()
        left = tree.pop()
        _,r = polyDiv(f, right)
        res.append(r)
        _,r = polyDiv(f, left)
        res.append(r)
        i += 1
    res = [x[0] for x in res[-1:-n-1:-1]]
    return res

def test():
    MOD = 998244353
    f = [1,2,3,2,5]
    xs = [-1,-2,-3]
    ys = multiPointEval(f, xs, MOD)
    def F(x):
        res,xn = 0,1
        for a in f:
            res = (res+a*xn)%MOD
            xn *= x
        return res
    print("result : ",ys)
    print("ans :" ,[F(x) for x in xs])

def perf():
    import random
    from time import perf_counter as time
    MOD = 998244353
    N = 100
    M = 10
    f = [random.randint(0,MOD-1) for _ in range(N)]
    xs = [random.randint(0,MOD-1) for _ in range(M)]
    start = time()
    multiPointEval(f, xs)
    print(f"{time() - start}")

if __name__ == '__main__':
    test()
    perf()

