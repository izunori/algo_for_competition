from collections import defaultdict, deque
def ManberMyers(S, conv=ord):
    N = len(S)
    d = defaultdict(list)
    for i,s in enumerate(S):
        d[conv(s)].append(i)
    rank = [0]*N
    i = 0
    tbd = deque([])
    for k in sorted(d.keys()):
        for t in d[k]:
            rank[t] = i
        i += len(d[k])
        if len(d[k]) > 1:
            tbd.append((d[k],1))
    while tbd:
        target, l = tbd.popleft()
        d = defaultdict(list)
        for t in target:
            nt = rank[t+l] if t+l < N else -1
            d[nt].append(t)
        i = 0
        for k in sorted(d.keys()):
            for t in d[k]:
                rank[t] += i
            i += len(d[k])
            if len(d[k]) > 1:
                tbd.append((d[k],l*2))
    result = [0]*N
    for i,r in enumerate(rank):
        result[r] = i
    return result

# very slow
def ManberMyers2(S, conv = ord):
    N = len(S)
    def ranking(L):
        temp = [(x,i) for i,x in enumerate(L)]
        temp.sort()
        result = [0]*len(temp)
        px = temp[0][0]
        index = 0
        for x,i in temp:
            index += (px != x)
            result[i] = index
            px = x
        return result
    rank = ranking(conv(s) for i,s in enumerate(S))

    k = 1
    def follow(i):
        return rank[i+k] if i+k<N else -1
    while k <= N:
        rank = ranking((rank[i],follow(i)) for i,s in enumerate(rank))
        k *= 2
    result = [(rank[i],S[i:]) for i in range(N)]
    result.sort()
    _, result = zip(*result)
    return result

def for_test(S):
    N = len(S)
    temp = [(S[i:],i) for i in range(N)]
    _, res = zip(*sorted(temp))
    return list(res)

def test():
    S = 'abracadabra'
    res = ManberMyers(S)
    res2 = for_test(S)
    print(res)
    print(res2)
    print(res == res2)
    S = 'a'*20
    res = ManberMyers(S)
    res2 = for_test(S)
    print(res)
    print(res2)
    print(res == res2)

def perf():
    from time import perf_counter as time
    import string
    import random

    N = 10**4
    S = "".join(random.choices(string.ascii_letters, k=N))
    #S = "a"*N

    start = time()
    r = ManberMyers(S)
    print(f'{time()-start}s')

    start = time()
    r2 = for_test(S)
    print(f'{time()-start}s')

if __name__=='__main__':
    test()
    perf()
