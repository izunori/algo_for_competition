from collections import defaultdict, deque
from itertools import accumulate
from algo_ManberMyers import ManberMyers
import array as ar
def SA_IS(S):
    if type(S) is str:
        S = list(map(ord, S))
    if len(S) == 1:
        return [1,0]
    comp = {x:i for i,x in enumerate(sorted(set(S)))}
    S = ar.array('i',[comp[s] for s in S])
    N,K = len(S),len(comp)
    ls = ar.array('b',[0]*N+[1])
    for i in range(N-2,-1,-1):
        ls[i] = ls[i+1] if S[i] == S[i+1] else (S[i] < S[i+1]) # 0:S, 1:L
    lms = [i+1 for i in range(N+1) if not ls[i] and ls[i+1]]
    M = len(lms)
    def induced_sort(lms):
        rank = ar.array('i',[-1]*(N+1))
        rank[0] = N
        d2 = [1]+[0]*K
        for s in S:
            d2[s] += 1
        d2 = list(accumulate(d2))
        d2[-1] = 1
        d3,d4 = d2[:],d2[:]
        for i in lms[::-1]:
            s = S[i] if i < N else -1
            d2[s] -= 1
            rank[d2[s]] = i
        for k in range(N+1):
            i = rank[k]
            if i > -1 and ls[i-1] == 0:
                s = S[i-1]-1
                rank[d3[s]] = i-1
                d3[s] += 1
        for k in range(N,-1,-1):
            i = rank[k]
            if i > 0 and ls[i-1] == 1:
                s = S[i-1]
                d4[s] -= 1
                rank[d4[s]] = i-1
        return rank
    rank = induced_sort(lms)
    lms_subs = {N:-1}
    for i in range(M-1):
        lms_subs[lms[i]] = S[lms[i]:lms[i+1]+1]
    lms2 = [i for i in rank if i > 0 and not ls[i-1] and ls[i]]
    nums = [0]
    for i in range(M-1):
        if lms_subs[lms2[i]] == lms_subs[lms2[i+1]]:
            nums.append(nums[-1])
        else:
            nums.append(nums[-1]+1)
    m = {x:n for x,n in  zip(lms2,nums)}
    res = SA_IS([m[i] for i in lms])
    new_lms = [lms[i] for i in res[1:]]
    return list(induced_sort(new_lms))

def greedy(S):
    N = len(S)
    temp = [(S[i:],i) for i in range(N+1)]
    _, res = zip(*sorted(temp))
    return list(res)

def test():
    print("--test")
    S = 'mmiissiissiippii'
    print(SA_IS(S))
    print(greedy(S))

def test_random():
    import random
    N = 1000
    M = 100
    for _ in range(M):
        S = "".join([chr(97+random.randint(0,1)) for _ in range(N)])
        ans = greedy(S)
        res = SA_IS(S)
        if ans != res:
            print("failed:", S)
            print("ans:", ans)
            print("res:", res)
            exit()
    print("ok")

def perf():
    print("--perf")
    import random
    from time import perf_counter as time
    N = 2*10**5
    M = 26
    S = "".join([chr(97+random.randint(0,M)) for _ in range(N)])

    start=time()
    SA_IS(S)
    print(f"SA_IS : {time()-start}") 

    start=time()
    ManberMyers(S)
    print(f"MM    : {time()-start}") 

    if N <= 10**4:
        start=time()
        greedy(S)
        print(f"greedy: {time()-start}") 

if __name__=='__main__':
    test()
    test_random()
    for _ in range(10):
        perf()

