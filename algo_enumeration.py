
# Lucas's theorem
def nCrmod2(n,r):
    if r > n:
        return 0
    return (n&k)==k

MOD = 10**9 + 7
num = 200000
fact = [1] * (num+1)
ifact = [1] * (num+1)
# if you need inverse
#inv = [pow(i,MOD-2,MOD) for i in range(num+1)]

for i in range(1,num+1):
    fact[i] = (fact[i-1] * i) % MOD
ifact[-1] = pow(fact[-1],MOD-2,MOD)
for i in range(1,num+1)[::-1]:
    ifact[i-1] = (ifact[i] * i)% MOD

def nPr(n,r):
    if r > n:
        return 0
    return (fact[n] * ifact[n-r]) % MOD
def nCr(n,r):
    if r > n:
        return 0
    return (((fact[n] * ifact[r])%MOD) * ifact[n-r]) % MOD

# mod p pascal
def Lucus(n,p):
    def g(n):
        res = []
        while n:
            res.append(n%p)
            n //= p
        return res[::-1]
    np = g(n)
    L = len(np)
    ip = [0]*L
    res = []
    for _ in range(n+1):
        c = 1
        for a,b in zip(np,ip):
            c *= nCr(a,b) # normal nCr (without mod)
        res.append(c)

        ip[-1] += 1
        for d in range(L-1,-1,-1):
            if ip[d] < p:
                break
            ip[d] = 0
            ip[d-1] += 1
    return res

print(Lucus(5,3))
 

    
