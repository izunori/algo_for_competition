from collections import defaultdict, deque
from algo_ManberMyers import ManberMyers
def SA_IS(S):
    if type(S) is str:
        S = list(map(ord, S))
    if len(S) == 1:
        return [1,0]
    comp = {x:i for i,x in enumerate(sorted(set(S)))}
    S = [comp[s] for s in S]
    N,K = len(S),len(comp)
    ls = [0]*N+[1]
    for i in range(N-2,-1,-1):
        ls[i] = ls[i+1] if S[i] == S[i+1] else (S[i] < S[i+1]) # 0:S, 1:L
    lms = [i+1 for i in range(N+1) if not ls[i] and ls[i+1]]
    M = len(lms)
    lms_subs = {N:-1}
    for i in range(M-1):
        lms_subs[lms[i]] = S[lms[i]:lms[i+1]+1]
    def induced_sort(lms):
        rank = [-1]*(N+1)
        rank[0] = N
        d = [0 for k in range(K+1)]
        for s in S:
            d[s] += 1
        d[-1] = 1
        d2 = [0 for k in range(K+1)]
        i = 0
        for s in range(-1,K):
            l = d[s]
            d2[s] = i+l
            i += l
        d3 = d2[:]
        d4 = d2[:]
        for i in lms[::-1]:
            s = S[i] if i < N else -1
            j = d2[s]
            rank[j-1] = i
            d2[s] -= 1
        for k in range(N+1):
            i = rank[k]
            if i == -1:
                continue
            if ls[i-1] == 0:
                s = S[i-1]
                j = d3[s-1]
                rank[j] = i-1
                d3[s-1] += 1
        for k in range(N,-1,-1):
            i = rank[k]
            if i > 0 and ls[i-1] == 1:
                s = S[i-1]
                j = d4[s]
                rank[j-1] = i-1
                d4[s] -= 1
        return rank
    rank = induced_sort(lms)
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
    return induced_sort(new_lms)
        
def for_test(S):
    N = len(S)
    temp = [(S[i:],i) for i in range(N+1)]
    _, res = zip(*sorted(temp))
    return list(res)

def test():
    print("--test")
    S = 'mmiissiissiippii'
    print(SA_IS(S))
    print(for_test(S))

    import random
    N = 100
    M = 100
    for _ in range(M):
        S = "".join([chr(97+random.randint(0,1)) for _ in range(N)])
        ans = for_test(S)
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
    N = 10*10**5
    S = "".join([chr(97+random.randint(0,26)) for _ in range(N)])

    start=time()
    SA_IS(S)
    print(f"{time()-start}") 

    start=time()
    ManberMyers(S)
    print(f"{time()-start}") 


if __name__=='__main__':
    test()
    perf()
    

