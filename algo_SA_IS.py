from collections import defaultdict, deque
from algo_ManberMyers import ManberMyers
def SA_IS(S):
    if len(S) == 1:
        return [1,0]
    N = len(S)
    ls = [1]*(N+1)
    ls[-2] = 0
    ss = ['']+sorted(set(S))
    for i in range(N-2,-1,-1):
        if S[i] < S[i+1]:
            ls[i] = 1 # S
        elif S[i] > S[i+1]:
            ls[i] = 0 # L
        else:
            ls[i] = ls[i+1]
    lms = []
    for i in range(N+1):
        if ls[i] == 0 and ls[i+1] == 1:
            lms.append(i+1)
    lms_subs = {N:''}
    for i,j in zip(lms,lms[1:]):
        lms_subs[i] = S[i:j+1]

    def induced_sort(lms):
        rank = [-1]*(N+1)
        rank[0] = N
        d = defaultdict(lambda:[0,0])
        for s,x in zip(S,ls):
            d[s][x] += 1
        d[''][1] = 1
        d2 = defaultdict(lambda:[-1,-1])
        i = 0
        for s in ss:
            for x in range(2):
                l = d[s][x]
                d2[s][x] = [i,i+l,i+l]
                i += l
        for i in lms[::-1]:
            s = S[i] if i < N else ''
            j = d2[s][1][1]
            rank[j-1] = i
            d2[s][1][1] -= 1
        for k in range(N+1):
            i = rank[k]
            if i == -1:
                continue
            if ls[i-1] == 0:
                s = S[i-1]
                j = d2[s][0][0]
                rank[j] = i-1
                d2[s][0][0] += 1
        for k in range(N,-1,-1):
            i = rank[k]
            if i > 0 and ls[i-1] == 1:
                s = S[i-1]
                j = d2[s][1][2]
                rank[j-1] = i-1
                d2[s][1][2] -= 1
        return rank
    rank = induced_sort(lms)
    lms2 = []
    for i in rank:
        if i > 0 and ls[i-1] == 0 and ls[i] == 1:
            lms2.append(i)
    nums = [0]
    for i,j in zip(lms2,lms2[1:]):
        if lms_subs[i] == lms_subs[j]:
            nums.append(nums[-1])
        else:
            nums.append(nums[-1]+1)
    m = {x:n for x,n in  zip(lms2,nums)}
    nxt = [m[i] for i in lms]
    res = SA_IS(nxt)
    new_lms = [lms[i] for i in res[1:]]
    return induced_sort(new_lms)
        
def for_test(S):
    N = len(S)
    temp = [(S[i:],i) for i in range(N+1)]
    _, res = zip(*sorted(temp))
    return list(res)

def test():
    print("--test")
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
    import random
    from time import perf_counter as time
    N = 2*10**5
    S = "".join([chr(97+random.randint(0,1)) for _ in range(N)])

    start=time()
    SA_IS(S)
    print(f"{time()-start}") 

    start=time()
    ManberMyers(S)
    print(f"{time()-start}") 


if __name__=='__main__':
    #S = 'mmiissiissiippii'
    #T = list(map(ord, S))
    #res = SA_IS(S)
    #print(res)
    #print(for_test(S))
    test()
    perf()
    

