from time import perf_counter as time
import pypyjit
import array as ar
pypyjit.set_param('max_unroll_recursion=-1')
MOD = 998244353

# ntt
# 119*2^23+1 = 119*8388608+1
class NNT:
    def __init__(self):
        if MOD != 998244353:
            assert "mod must be 998244353 in my nnt"
        self.maxK = 21
        self.maxL = 2**self.maxK # 2**21 > 10**6
        # 31**(2**23) = 1 mod 998244353
        self.ws = [pow(31,2**i,MOD) for i in range(23,-1,-1)]
        self.iws = [pow(w,MOD-2,MOD) for w in self.ws]
    def nnt(self,A): # len(A) = 2**k
        n = len(A)
        if n == 1:return
        k = n.bit_length()-1
        r = 1<<(k-1)
        for w in self.ws[k:1:-1]:
            for i in range(0,n,2*r):
                wi = 1
                for j in range(r):
                    A[i+j],A[i+j+r],wi = (A[i+j]+A[i+j+r])%MOD,(A[i+j]-A[i+j+r])*wi%MOD,wi*w%MOD
            r = r//2
        for i in range(0,n,2): # expand for performance (take modulo in innt)
            A[i],A[i+1] = (A[i]+A[i+1]),(A[i]-A[i+1])
    def innt(self,A): # len(A) = 2**k
        n = len(A)
        if n == 1:return
        k = (n-1).bit_length()
        for i in range(0,n,2): # expand for performance
            A[i],A[i+1] = (A[i]+A[i+1]),(A[i]-A[i+1])
        r = 2
        for w in self.iws[2:k+1]:
            for i in range(0,n,2*r):
                wi = 1
                for j in range(r):
                    A[i+j],A[i+j+r],wi = (A[i+j]+A[i+j+r]*wi)%MOD,(A[i+j]-A[i+j+r]*wi)%MOD,wi*w%MOD
            r = r*2
        ni = pow(n, MOD-2, MOD)
        for i in range(n):
            A[i] = A[i]*ni%MOD

    def polymul(self,f,g):
        if len(f)+len(g) <= 512 or min(len(f),len(g)) <= 32:
            return self.polymul_simple(f,g)
        else:
            return self.polymul_nnt(f,g)
    def polymul_nnt(self,f,g):
        nf = len(f)
        ng = len(g)
        m = nf+ng-1
        k = (m-1).bit_length()
        n = 2**k
        f = ar.array('i',[x % MOD for x in f]+[0]*(n-nf))
        g = ar.array('i',[x % MOD for x in g]+[0]*(n-ng))
        self.nnt(f)
        self.nnt(g)
        for i,(x,y) in enumerate(zip(f,g)):
            f[i] = x*y%MOD
        self.innt(f)
        return list(f)[:m]

    # for validation
    def polymul_simple(self,f,g):
        n,m = len(f),len(g)
        ans = [0]*(n+m-1)
        for i in range(n):
            for j in range(m):
                ans[i+j] = (ans[i+j]+f[i]*g[j]) % MOD
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
    print("--perf--")
    from time import perf_counter as time
    import random
    N = 10**6
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
    nnt = NNT()
    N = 512
    #for r in range(10):
        #r = 2**r
    for r in range(0,N,N//10):
        nf = N-r
        ng = r
        f = [random.randint(0,MOD-1) for i in range(nf)]
        g = [random.randint(0,MOD-1) for i in range(ng)]

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
    print("--test--")
    MOD = 998244353
    from time import perf_counter as time
    import random
    K = 10
    N0 = random.randint(1,K)
    N1 = random.randint(1,K)
    M = MOD
    f = [random.randint(0,M) for i in range(N0)]
    g = [random.randint(0,M) for i in range(N1)]
    f = [1]
    g = [1,2]
    nnt = NNT()
    fg = nnt.polymul_nnt(f,g)
    ans = nnt.polymul_simple(f,g)
    if fg == ans:
        print('OK')
    else:
        print('NG')
        print("f,g=",f,g)
        print("fg,ans=",fg,ans)

if __name__=='__main__':
    test_polymul()
    test_perf()
    #test_perf_compare()

