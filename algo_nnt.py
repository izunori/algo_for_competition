from time import perf_counter as time
import pypyjit
pypyjit.set_param('max_unroll_recursion=-1')

# ntt
# 119*2^23+1 = 119*8388608+1
class NNT:
    def __init__(self, MOD=998244353):
        self.MOD = MOD
        if self.MOD != 998244353:
            assert "mod must be 998244353 in my nnt"
        self.maxK = 19
        self.maxL = 2**self.maxK # 2**19 > 4*10**5
        self.ws = [31] # 31**(2**23) = 1 mod 998244353
        for i in range(24):
            self.ws.append(pow(self.ws[-1],2,self.MOD))
        self.ws.reverse() # ws[i]**(2**i) = 1 mod
        self.iws = [pow(31,self.MOD-2,self.MOD)]
        for i in range(24):
            self.iws.append(pow(self.iws[-1],2,self.MOD))
        self.iws.reverse()
        self.rev = [0]*self.maxL
        for i in range(1,self.maxL):
            if self.rev[i]:
                continue
            b,rb = 1,1<<(self.maxK-1)
            j = 0
            for _ in range(self.maxK):
                if (i&b):
                   j = j|rb
                b,rb = b<<1,rb>>1
            self.rev[i],self.rev[j] = j,i
    def nnt(self,A,k,tws):
        n = len(A)
        step = self.maxL // (2**k)
        res = [A[i] for i in self.rev[::step]]
        r = 1
        for w in tws[2:k+2]:
            for l in range(0,n,r*2):
                wi = 1
                for i in range(l,l+r):
                    x = (res[i] + res[i+r]*wi) % self.MOD
                    y = (-x + 2*res[i]) % self.MOD
                    res[i],res[i+r] = x,y
                    wi = (wi*w) % self.MOD
            r <<= 1
        return res
    def polymul(self,f,g):
        nf = len(f)
        ng = len(g)
        m = nf+ng-1
        f = [x % self.MOD for x in f]
        g = [x % self.MOD for x in g]
        k = (m-1).bit_length()
        l = 2**k
        f = f+[0]*(l-nf)
        g = g+[0]*(l-ng)
        def _polymul(u,v,k):
            U = self.nnt(u, k, self.ws)
            V = self.nnt(v, k, self.ws)
            UV = self.nnt([(u*v)%self.MOD for u,v in zip(U,V)], k, self.iws)
            l = 2**k
            il = pow(l, self.MOD-2, self.MOD)
            return [(x*il)%self.MOD for x in UV]
        return _polymul(f,g,k)[:m]

def polymul_old(f,g,MOD = 998244353):
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

def test_perf():
    from time import perf_counter as time
    import random
    MOD = 998244353
    N = 2*10**5
    M = MOD # looks good in <= 2*10**6
    f = [random.randint(0,M) for i in range(N)]
    g = [random.randint(0,M) for i in range(N)]
    nnt = NNT()
    start = time()
    fg = nnt.polymul(f,g)
    print(f'{time()-start}s')
    start = time()
    fg = polymul_old(f,g)
    print(f'{time()-start}s')


def test_polymul():
    MOD = 998244353
    from time import perf_counter as time
    import random
    N = 1000
    M = MOD # looks good in <= 2*10**6
    random.seed(0)
    f = [random.randint(0,M) for i in range(N)]
    g = [random.randint(0,M) for i in range(N)]
    nnt = NNT()
    start = time()
    fg = nnt.polymul(f,g)
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
    test_perf()

