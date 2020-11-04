from algo_bit import BIT

def inversion(A):
    # compress
    kinds = sorted(set(A))
    nk = len(kinds)
    order = {v:i for i,v in enumerate(kinds)}
    data = [0]*nk
    bit = BIT(data, lambda x,y : x+y, 0)
    res = []
    for i,a in enumerate(A):
        ind = order[a]
        res.append(i - bit.get(ind))
        bit.add(ind,1)
    return sum(res)

def test():
    A = [8,3,9,7]
    print(inversion(A),3)
    A = [1,10**9,3,3,2]
    print(inversion(A),5)
    A = [-10,0,10]
    print(inversion(A),0)

def perf():
    import random
    from time import perf_counter as time
    N = 10**5
    A = [random.randint(0,10**9) for i in range(N)]
    start = time()
    inversion(A)
    print(f"{(time()-start)*1000}ms")

if __name__=='__main__':
    test()
    #perf()
