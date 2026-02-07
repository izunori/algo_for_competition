
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
inv = [1] * (num+1)

for i in range(1,num+1):
    fact[i] = (fact[i-1] * i) % MOD
ifact[-1] = pow(fact[-1],MOD-2,MOD)
for i in range(1,num+1)[::-1]:
    ifact[i-1] = (ifact[i] * i)% MOD
    inv[i] = (ifact[i] * fact[i-1]) % MOD

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

# 1st Starling number on N
memo = {0:[1], 1:[0,1]}
def findS(n):
    if n in memo:
        return memo[n]
    t = n//2
    if t*2 == n:
        f = findS(t)
        sf = shift(f,t)
        return nnt.polymul(f,sf)
    else:
        f = findS(t)
        sf = shift(f,t)
        r = nnt.polymul(f,sf)
        l = len(r)
        return [((n-1) * r[i] + (r[i-1] if i > 0 else 0))%MOD for i in range(l)] + [1]
    
