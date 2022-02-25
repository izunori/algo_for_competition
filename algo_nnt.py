
# ntt
# 2^23 = 8388608
def polymul3(f,g,MOD = 998244353):
    nf = len(f)
    ng = len(g)
    f = [x % MOD for x in f]
    g = [x % MOD for x in g]
    m = nf+ng-1
    k = (m-1).bit_length()
    l = 2**k
    if MOD != 998244353:
        assert "False"
    ws = [31]
    for i in range(24):
        ws.append(pow(ws[-1],2,MOD))
    ws.reverse()
    iws = [pow(31,MOD-2,MOD)]
    for i in range(24):
        iws.append(pow(iws[-1],2,MOD))
    iws.reverse()
    f = f+[0]*(l-nf)
    g = g+[0]*(l-ng)
    def _fft(A,k,tws):
        if k == 0:
            return A
        w = tws[k+1]
        A0 = A[::2]
        A1 = A[1::2]
        n2 = 1<<(k-1)
        B0 = _fft(A0, k-1, tws)
        B1 = _fft(A1, k-1, tws)
        res = [0]*(1<<k)
        wi = 1
        for i,(b0,b1) in enumerate(zip(B0,B1)):
            res[i] = (b0 + b1 * wi) % MOD
            res[i+n2] = (-res[i]+2*b0) % MOD
            wi = (wi*w) % MOD
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
    MOD = 998244353
    from time import perf_counter as time
    import random
    N = 1000
    M = MOD # looks good in <= 2*10**6
    f = [random.randint(0,M) for i in range(N)]
    g = [random.randint(0,M) for i in range(N)]
    start = time()
    fg = polymul3(f,g)
    print(f'{time()-start}s')
    ans = []
    for i in range(2*N-1):
        t = 0
        for j in range(max(i-N+1,0),min(N-1,i)+1):
            t += f[j]*g[i-j]
        t %= MOD
        ans.append(t)
    for x,y in zip(fg,ans):
        if x != y:
            print(x,y)
            print('NG')
            break
    else:
        print('OK')

if __name__=='__main__':
    test_polymul()
