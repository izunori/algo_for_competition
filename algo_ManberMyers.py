from collections import defaultdict, deque
import array as ar
def ManberMyers(S, conv=ord):
    N = len(S)
    d = defaultdict(list)
    for i,s in enumerate(S):
        d[conv(s)].append(i)
    rank = [0]*(N+1)
    i = 1 # offset for empty
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
    result = [0]*(N+1)
    for i,r in enumerate(rank):
        result[r] = i
    return result

def ManberMyers3(S, conv=ord):
    N = len(S)
    d = defaultdict(list)
    for i,s in enumerate(S):
        d[conv(s)].append(i)
    rank = ar.array('i',[0]*(N+1))
    i = 1 # offset for empty
    tbd = deque([])
    for k in sorted(d.keys()):
        for t in d[k]:
            rank[t] = i
        i += len(d[k])
        if len(d[k]) > 1:
            tbd.append((d[k],1))
    while tbd:
        target, l = tbd.popleft()
        if len(target) == 2:
            x,y = target
            nx = rank[x+l] if x+l < N else -1
            ny = rank[y+l] if y+l < N else -1
            if nx==ny:
                tbd.append(((x,y),l*2))
            elif nx < ny:
                rank[y] += 1
            else:
                rank[x] += 1
            continue
        d = defaultdict(list)
        for t in target:
            nt = rank[t+l] if t+l < N else -1
            d[nt].append(t)
        i = 0
        for k in sorted(d.keys()):
            if i > 0:
                for t in d[k]:
                    rank[t] += i
            i += len(d[k])
            if len(d[k]) > 1:
                tbd.append((d[k],l*2))
    result = ar.array('i',[0]*(N+1))
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
    temp = [(S[i:],i) for i in range(N+1)]
    _, res = zip(*sorted(temp))
    return list(res)

def LongestCommonPrefixArray(S, sa):
    N = len(S)
    rank = [0]*(N+1)
    for i,s in enumerate(sa):
        rank[s] = i
    s0 = 0
    s1 = sa[rank[0]-1]
    h = 0
    for i in range(N-s1):
        if S[i+s0]==S[i+s1]:
            h += 1
        else:
            break
    lcp = [h]
    for i in range(1,N):
        h = max(0,h-1)
        s0 = i+h
        s1 = sa[rank[i]-1]+h
        for i in range(N-s1):
            if S[i+s0]==S[i+s1]:
                h += 1
            else:
                break
        lcp.append(h)
    result = [0]*N
    for i,l in enumerate(lcp):
        result[rank[i]-1] = l
    return result

def test_sa():
    import random
    import string
    N = 8
    M = 10000
    for _ in range(M):
        S = "".join([chr(97+random.randint(0,1)) for _ in range(N)])
        res = list(ManberMyers(S))
        res2 = for_test(S)
        if res != res2:
            print("failed:",S)
            print(res)
            print(res2)
            exit()

def perf_sa():
    from time import perf_counter as time
    import string
    import random
    print("--perf")

    N = 2*(10**5)

    S = "".join(random.choices(string.ascii_letters, k=N))
    start = time()
    sa = ManberMyers(S)
    print(f'random: {time()-start}s')

    S = "a"*N
    start = time()
    sa = ManberMyers(S)
    print(f'all a : {time()-start}s')

    T = "".join([chr(97+random.randint(0,1)) for _ in range(N//2)])
    T = T+T
    start = time()
    sa = ManberMyers(T)
    print(f'4 times: {time()-start}s')

def test_lcp():
    S = 'abracadabra'
    res = ManberMyers3(S)
    res2 = for_test(S)
    lcp = LongestCommonPrefixArray(S, res)

    print(res)
    print(res2)
    print(lcp)
    print([0, 1, 4, 1, 1, 0, 3, 0, 0, 0, 2])
    print(res == res2)
    print(lcp == [0, 1, 4, 1, 1, 0, 3, 0, 0, 0, 2])

    S = 'a'*20+'b'*20
    res = ManberMyers(S)
    res2 = for_test(S)
    lcp = LongestCommonPrefixArray(S, res)
    print(res)
    print(res2)
    print(lcp)
    print(res == res2)

def perf_lcp():
    S = "".join(random.choices(string.ascii_letters, k=N))
    sa = ManberMyers(S)

    start = time()
    lcp = LongestCommonPrefixArray(S,sa)
    r2 = for_test(S)
    print(f'lcp: {time()-start}s')


if __name__=='__main__':
    test_sa()
    perf_sa()
