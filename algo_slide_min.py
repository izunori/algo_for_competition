from collections import deque
# memo : faster than using two deque
def slide_min(A, k, full=False):
    if full:
        A += [10**18]*(k-1)
    dq = deque([])
    res = []
    for i,a in enumerate(A):
        while dq and a <= dq[-1][1]:
            dq.pop()
        dq.append((i,a))
        while dq[0][0] < i-k+1:
            dq.popleft()
        res.append(dq[0][1])
    if not full:
        res = res[k-1:]
    return res

def test():
    A = [0,1,4,3,5,2,6,7,9,10]
    print(0,1,3,2,2,2,6,7)
    print(slide_min(A,3))
    A = [0,1,2,3,4,5]
    print(slide_min(A,3))
    print(slide_min(A,3,True))

def perf():
    import random
    from time import perf_counter as time
    N = 10**5
    K = 10**3
    M = 10**3
    A = [random.randint(0,M) for i in range(N)]
    start = time()
    slide_min(A,K)
    print(f"{(time()-start)*1000}ms")

if __name__=='__main__':
    test()
    #perf()



