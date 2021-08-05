def rollingHash(S, m, b=10**9+7, h=2**61-1):
    A = list(map(ord,S))
    temp = 0
    for a in A[:m]:
        temp = (temp * b + a) % h
    res = [temp]
    bm = pow(b,m,h)
    for a, ma in zip(A[m:],A):
        temp = (temp*b - ma*bm + a) % h 
        res.append(temp)
    return res 

def test():
    S = 'abracatabra'
    table = rollingHash(S, 3)
    T = 'tab'
    hs = rollingHash(T,3)[0]
    print(hs in table, True)

def perf():
    from time import perf_counter as time
    S = 'a'*(10**5)
    start = time()
    rollingHash(S,100)
    print(f"{(time()-start)*1000}ms")

if __name__=='__main__':
    test()
    perf()
