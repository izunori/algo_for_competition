# 2 sec = N <= 22 in pypy3
def fastMoebiusOnSet(A):
    N = len(A)
    S = [0]*2**N
    for i in range(N):
        S[1<<i] = A[i]
    for i in range(N):
        k = 1<<i
        for j in range(2**N):
            if not k & j:
                S[k|j] += S[j]
    return S

def test():
    A = [1,10,100,1000]
    S = fastMoebiusOnSet(A)
    print(S)

def perf():
    from time import perf_counter as time
    A = [10**i for i in range(22)]
    start = time()
    S = fastMoebiusOnSet(A)
    print(f"{time() - start}")
    print(S[-1])
    

if __name__=='__main__':
    test()
    perf()
