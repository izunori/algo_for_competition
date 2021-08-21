import cmath
import numpy as np

# use numpy
def polymul(f,g):
    f = np.array(f)
    g = np.array(g)
    nf = len(f)
    ng = len(g)
    m = nf+ng-1
    l = 2**((m-1).bit_length())
    def _polymul(u,v,l):
        U = np.fft.rfft(u, l)
        V = np.fft.rfft(v, l)
        UV = np.fft.irfft(U*V, l)
        return np.rint(np.real(UV)).astype(np.int64)
    k = 10**3
    f1 = f // k
    f0 = f % k
    g1 = g // k
    g0 = g % k
    r2 = _polymul(f1, g1, l)
    r0 = _polymul(f0, g0, l)
    r1 = r0+r2-_polymul(f1-f0, g1-g0, l)
    return (r2*(k**2) + r1*k + r0)[:m]

# not use numpy
def polymul2(f,g):
    nf = len(f)
    ng = len(g)
    m = nf+ng-1
    l = 2**((m-1).bit_length())
    f = f+[0]*(l-nf)
    g = g+[0]*(l-ng)
    def _fft(A,n):
        # n must be the power of 2
        if n == 1:
            return A
        w = cmath.rect(1, 2*cmath.pi/n)
        A0 = A[::2]
        A1 = A[1::2]
        n2 = n//2
        B0 = _fft(A0, n2)
        B1 = _fft(A1, n2)
        res = [0]*n
        for i,(b0,b1) in enumerate(zip(B0,B1)):
            res[i] = b0 + b1 * (w**i)
            res[i+n2] = b0 - b1 * (w**i)
        return res
    def _polymul(u,v,l):
        U = _fft(u, l)
        V = _fft(v, l)
        UV = _fft([(u*v).conjugate() for u,v in zip(U,V)] ,l) # ifft part
        return [int(uv.real+0.5)//l for uv in UV]
    k = 10**3
    f1 = [a // k for a in f]
    f0 = [a % k for a in f]
    g1 = [a // k for a in g]
    g0 = [a % k for a in g]
    r2 = _polymul(f1,g1,l)
    r0 = _polymul(f0,g0,l)
    r1 = [x+y-z for x,y,z in zip(r0,r2,_polymul([a-b for a,b in zip(f1,f0)],[a-b for a,b in zip(g1,g0)], l))]
    res = [x*(k**2) + y * k + z for x,y,z in zip(r2,r1,r0)]
    return res[:m]

# ntt
# UNDER CONSTRUCTION
def polymul3(f,g,MOD = 998244353):
    nf = len(f)
    ng = len(g)
    m = nf+ng-1
    k = (m-1).bit_length()
    l = 2**k
    if MOD != 998244353:
        assert "False"
    ws = [31]
    for i in range(24):
        ws.append(pow(ws[-1],2,MOD))
    ws.reverse()
    iws = []
    for w in ws:
        iws.append(pow(w,MOD-2,MOD))
    f = f+[0]*(l-nf)
    g = g+[0]*(l-ng)
    def _fft(A,k,ws):
        if k == 0:
            return A
        w = ws[k+1]
        A0 = A[::2]
        A1 = A[1::2]
        n2 = 1<<(k-1)
        B0 = _fft(A0, k-1, ws)
        B1 = _fft(A1, k-1, ws)
        res = [0]*(1<<k)
        for i,(b0,b1) in enumerate(zip(B0,B1)):
            res[i] = (b0 + b1 * (w**i)) % MOD
            res[i+n2] = (b0 - b1 * (w**i)) % MOD
        return res
    def _polymul(u,v,k):
        U = _fft(u, k, ws)
        V = _fft(v, k, ws)
        UV = _fft([(u*v)%MOD for u,v in zip(U,V)], k, iws)
        l = 2**k
        il = pow(l, MOD-2, MOD)
        return [(x*il)%MOD for x in UV]
    return _polymul(f,g,k)[:m]

def test_polymul():
    from time import perf_counter as time
    N = 10**4
    M = 20**6 # looks good in <= 20**6
    f = np.random.randint(M, size=N)
    g = np.random.randint(M, size=N)
    start = time()
    fg = polymul(f,g)
    print(f'{time()-start}s')
    ans = np.convolve(f,g)
    print(np.all(fg==ans))

def test2():
    from time import perf_counter as time
    N = 10000
    M = 20**6 # looks good in <= 20**6
    f = np.random.randint(M, size=N).tolist()
    g = np.random.randint(M, size=N).tolist()
    start = time()
    fg1 = polymul(f,g)
    print(f'{time()-start}s')

    start = time()
    fg2 = polymul2(f,g)
    print(f'{time()-start}s')

    start = time()
    MOD = 998244353
    fg3 = polymul3(f,g,MOD)
    print(f'{time()-start}s')
    for x,y in zip(fg1,fg3):
        print(x%MOD,y,(x%MOD)==y)


if __name__=='__main__':
    #test_polymul()
    test2()
