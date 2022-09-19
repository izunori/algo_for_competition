MOD = 10**9 + 7
num = 200000
fact = [1] * (num+1)
ifact = [1] * (num+1)

for i in range(1,num+1):
    fact[i] = (fact[i-1] * i) % MOD
ifact[-1] = pow(fact[-1],MOD-2,MOD)
for i in range(1,num+1)[::-1]:
    ifact[i-1] = (ifact[i] * i)% MOD

def nCr(n,r):
    if r > n:
        return 0
    return (((fact[n] * ifact[r])%MOD) * ifact[n-r]) % MOD

def notAdjacentList(bs):
    n = len(bs)
    m = sum(bs)
    dp,ndp = [0]*m, [0]*m
    dp[0] = 1
    gap = 1
    for i in range(n):
        b = bs[i]
        for k in range(1,min(gap,b)+1): # insert
            s = nCr(b-1,k-1)
            for ad in range(gap-i): # adjacent
                rest = gap-ad
                inc_ad = b-k
                for dec_ad in range(min(k,ad)+1): # insert and split
                    ndp[ad+inc_ad-dec_ad] += dp[ad] * s * nCr(ad,dec_ad) * nCr(rest,k-dec_ad)
        gap += b
        dp,ndp = ndp,dp
        for i in range(m):
            ndp[i] = 0
    return dp[0]


def test():
    from itertools import permutations
    bs = [2,2,2,2,2]
    cs = "".join(str(i)*n for i,n in enumerate(bs))
    ans = set()
    for p in permutations(cs):
        for s,ns in zip(p,p[1:]):
            if s == ns:
                break
        else:
            ans.add(''.join(p))
    print(len(ans))
    print(notAdjacentList(bs))
    
if __name__=='__main__':
    test()




