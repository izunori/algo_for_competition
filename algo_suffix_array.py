def ManberMyers(S, conv = ord):
    N = len(S)
    def sorted_index_of(L):
        temp = [(x,i) for i,x in enumerate(L)]
        temp.sort()
        result = [0]*N
        px = temp[0][0]
        index = 0
        for x,i in temp:
            index += (px != x)
            result[i] = index
            px = x
        return result
    rank = sorted_index_of(conv(s) for i,s in enumerate(S))

    k = 1
    def follow(i):
        return rank[i+k] if i+k<N else -1
    while k <= N:
        rank = sorted_index_of((rank[i],follow(i)) for i,s in enumerate(rank))
        k *= 2
    result = [(rank[i],S[i:]) for i in range(N)]
    result.sort()
    _, result = zip(*result)
    return result

def for_test(S):
    N = len(S)
    temp = [S[i:] for i in range(N)]
    return tuple(sorted(temp))

def test():
    S = 'abracadabra'
    res = ManberMyers(S)
    res2 = for_test(S)
    print(res == res2)

def perf():
    from time import perf_counter as time
    import string
    import random

    N = 10**4
    S = "".join(random.choices(string.ascii_letters, k=N))

    start = time()
    r = ManberMyers(S)
    print(f'{time()-start}s')

    start = time()
    r2 = for_test(S)
    print(f'{time()-start}s')

if __name__=='__main__':
    test()
    perf()
