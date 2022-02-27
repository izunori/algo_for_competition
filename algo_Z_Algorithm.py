def z_algorithm(S):
    N = len(S)
    Z = [0]*N
    Z[0] = N
    i,j = 1,0
    while i < N:
        while i+j < N and S[j] == S[i+j]:
            j += 1
        Z[i] = j
        if j == 0:
            i += 1
            continue
        k = 1
        while k+Z[k] < j:
            Z[i+k] = Z[k]
            k += 1
        i += k
        j -= k
    return Z

def test():
    print(z_algorithm('hhhggg'),(6,2,1,0,0,0))
    print(z_algorithm('hhhhhh'),(6,5,4,3,2,1))
    print((16,0,4,0,2,0,0,0,8,0,4,0,2,0,0,0))
    print(z_algorithm('momomosumomomosu'))
    print((16,0,4,0,2,0,0,0,6,0,6,0,4,0,2,0))
    print(z_algorithm('momomosumomomomo'))
    print((16,0,4,0,2,0,0,0,4,0,2,0,0,0,0,0))
    print(z_algorithm('momomohimomokusa'))
    import random
    N = 10**4
    M = 1
    S = [random.randint(0,M) for _ in range(N)]
    ans = []
    for i in range(N):
        j = 0
        for (s,t) in zip(S,S[i:]):
            if s == t:
                j += 1
            else:
                break
        ans.append(j)
    for s,t in zip(ans, z_algorithm(S)):
        if s != t:
            print('NG')
            break
    else:
        print('OK')

def perf():
    import random
    from time import perf_counter as time
    N = 10**5
    M = 0
    S = [random.randint(0,M) for _ in range(N)]
    start = time()
    z_algorithm(S)
    print(f"{time()-start}")
        
if __name__=='__main__':
    test()
    perf()
