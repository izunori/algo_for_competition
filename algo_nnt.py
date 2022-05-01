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
    def nnt(self,A,k):
        return self._nnt(A,k,self.ws)
    def innt(self,A,k):
        return self._nnt(A,k,self.iws)
    def _nnt(self,A,k,tws): # len(A) = 2**k
        n = len(A)
        step = self.maxL // (2**k)
        res = [A[i] for i in self.rev[::step]]
        r,MOD = 1, self.MOD
        for w in tws[2:k+2]:
            for l in range(0,n,r*2):
                wi = 1
                for i in range(l,l+r):
                    t = res[i+r]*wi
                    res[i],res[i+r] = (res[i]+t)%MOD,(res[i]-t)%MOD
                    wi = (wi*w) % MOD
            r <<= 1
        return res
    def polymul(self,f,g):
        if len(f)+len(g) <= 256 or max(len(f),len(g)) <= 128:
            return self.polymul_simple(f,g)
        else:
            return self.polymul_nnt(f,g)
    def polymul_nnt(self,f,g):
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
            U = self.nnt(u, k)
            V = self.nnt(v, k)
            UV = self.innt([(u*v)%self.MOD for u,v in zip(U,V)], k)
            il = pow(2**k, self.MOD-2, self.MOD)
            return [(x*il)%self.MOD for x in UV]
        return _polymul(f,g,k)[:m]
    def polymul_simple(self,f,g):
        n,m = len(f),len(g)
        ans = [0]*(n+m-1)
        for i in range(n):
            for j in range(m):
                ans[i+j] = (ans[i+j]+f[i]*g[j]) % self.MOD
        return ans

    def _nnt_recur(self,A,k,tws):
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

def test_perf():
    from time import perf_counter as time
    import random
    MOD = 998244353
    N = 128
    M = MOD
    f = [random.randint(0,M-1) for i in range(N)]
    g = [random.randint(0,M-1) for i in range(N)]
    nnt = NNT()

    start = time()
    fg1 = nnt.polymul_nnt(f,g)
    print(f'nnt:{time()-start}s')

    if N < 2**14:
        start = time()
        fg1 = nnt.polymul_simple(f,g)
        print(f'grd:{time()-start}s')

def test_perf_compare():
    from time import perf_counter as time
    import random
    MOD = 998244353
    N = 2*10**5
    M = MOD # looks good in <= 2*10**6
    nnt = NNT()
    r = 128
    nf = N-r
    ng = r
    f = [random.randint(0,M-1) for i in range(nf)]
    g = [random.randint(0,M-1) for i in range(ng)]

    start = time()
    fg1 = nnt.polymul_nnt(f,g)
    t1=time()-start

    start = time()
    fg2 = nnt.polymul_simple(f,g)
    t2=time()-start
    if t1<t2:
        print(f"nnt:{nf},{ng},{t1,t2}")
    else:
        print(f"grd:{nf},{ng},{t1,t2}")

def test_polymul():
    MOD = 998244353
    from time import perf_counter as time
    import random
    N = 2*10**3
    M = MOD
    random.seed(0)
    f = [random.randint(0,M) for i in range(N)]
    g = [random.randint(0,M) for i in range(N)]
    nnt = NNT()
    start = time()
    fg = nnt.polymul(f,g)
    print(f'{time()-start}s')
    ans = nnt.polymul_simple(f,g)
    if fg == ans:
        print('OK')
    else:
        print('NG')

if __name__=='__main__':
    #test_polymul()
    test_perf() # JIT optimize
    test_perf() # JIT optimize
    test_perf() # JIT optimize
    test_perf() # JIT optimize
    test_perf()
    test_perf_compare()

