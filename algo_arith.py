import heapq
import time
from collections import defaultdict


# prime factorization 
def sieve_Eratosthenes(n):
    f = [True]*(n+1)
    f[0] = False
    f[1] = False
    m = int(n**0.5+1)
    for i in range(2,m):
        if f[i]:
            for j in range(i*i,n+1, i):
                f[j] = False
    return f

def getPrimeLists(n):
    table = sieve_Eratosthenes(n)
    return [x for x in range(2,n+1) if table[x]]

def primeFactorization(n):
    res = defaultdict(int)
    m = int(n**0.5)
    for i in range(2,m+1):
        while n % i == 0:
            n = n//i
            res[i] += 1
    if n > 1:
        res[n] = 1
    return res

def divisors(n):
    ls = []
    for i in range(1,int(n**0.5)+1):
        if n % i == 0:
            ls.append(i)
            ls.append(n//i)
    ls = sorted(list(set(ls)))
    return ls

def powMemo(N,M,MOD):
    memo = [[0]*(M+1) for i in range(N+1)]
    for n in range(1,N+1):
        t = 1
        memo[n][0] = t
        for m in range(1,M+1):
            t = (t*n)%MOD
            memo[n][m] = t
    memo[0][0] = 1
    return memo

if __name__=='__main__':
    #print(sieve_Eratosthenes(10))
    #print(primeFactorization(24))
    MOD = 9982
    memo = powMemo(10,10,MOD)
    for i in range(10):
        for j in range(10):
            print(pow(i,j,MOD))
            print(memo[i][j])



