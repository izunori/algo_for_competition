import random
from operator import mul
from itertools import accumulate, starmap
from time import perf_counter as time

def tupleSortSlow(l):
    cs = [{x:i for i,x in enumerate(sorted(set(s)))} for s in list(zip(*l))]
    ls = list(accumulate(map(len,cs[-2::-1]),mul))[::-1]+[1]
    key = lambda x : sum(starmap(lambda v,c,p:c[v]*p, zip(x,cs,ls)))
    l.sort(key = key)

def tupleSort(l):
    mxs = list(map(lambda x : max(x)+1, list(zip(*l))[1:]))
    ls = list(accumulate(mxs[::-1],mul))[::-1]+[1]
    l.sort(key = lambda x : sum(starmap(mul, zip(x,ls))))

def comp(S):
    comp = {x:i for i,x in enumerate(sorted(set(S)))}
    return [comp[s] for s in S], comp

def perf():
    N = 2*10**5
    M1 = 2*10**5
    M2 = 2*10**5
    M3 = 2*10**5
    samples = [(random.randint(0,M1),random.randint(0,M2),random.randint(0,M3)) for i in range(N)]

    ss1 = samples[:]
    start = time()
    ss1.sort()
    print(f"{time() - start}")

    ss2 = samples[:]
    start = time()
    tupleSortSlow(ss2)
    print(f"{time() - start}")
    print(ss2 == ss1)

    ss3 = samples[:]
    start = time()
    tupleSort(ss3)
    print(f"{time() - start}")
    print(ss3 == ss1)

if __name__=='__main__':
    perf()
