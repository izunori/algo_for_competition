from collections import defaultdict, deque, Counter
def MoSort(lr):
    l,r,*v = zip(*lr)
    mx = max(max(l),max(r))
    block = mx // int(len(lr)**0.5)
    if block == 0:
        return
    def val(x):
        n = x[0]//block
        return 2 * n * mx + (-1 if n & 1 else 1) * x[1]
    lr.sort(key = val)

def perf_sort():
    import random
    from time import perf_counter as time
    N = 2*10**5
    M = 2*10**5
    lr = [sorted([random.randint(0,M), random.randint(0,M)]) for _ in range(N)]
    start=time()
    lr = MoSort(lr)
    print(f"{time()-start}") 

def plot():
    import random
    import matplotlib.pyplot as plt
    N = 100
    M = 100
    lr = [sorted([random.randint(0,M), random.randint(0,M)]) for _ in range(N)]
    MoSort(lr)
    for i in range(N):
        l,r = lr[i]
        plt.plot((l,r),(i,i),c='b')
    plt.show()

def test():
    import random
    from time import perf_counter as time

    N = 2*10**5
    M = 2*10**5
    Q = 2*10**3

    A = [random.randint(1,M) for _ in range(N)]
    LR = [sorted(random.sample(range(N), 2)) for _ in range(Q)]
    LR = [(l,r+1) for l,r in LR] # [l,r)

    start=time()
    ans = []
    for l,r in LR:
        cnt = set()
        for i in range(l,r):
            cnt.add(A[i])
        ans.append(len(cnt))
    print(f"{time()-start}") 

    start=time()
    LRI = [(l,r,i) for i,(l,r) in enumerate(LR)]
    MoSort(LRI)
    submit = [-1]*Q
    cnt = defaultdict(int)
    pl,pr = 0,0
    for l,r,j in LRI:
        if l < pl:
            for i in range(l,pl):
                cnt[A[i]] += 1
                if cnt[A[i]] == 0:
                    del cnt[A[i]]
        else:
            for i in range(pl,l):
                cnt[A[i]] -= 1
                if cnt[A[i]] == 0:
                    del cnt[A[i]]
        if pr < r:
            for i in range(pr,r):
                cnt[A[i]] += 1
                if cnt[A[i]] == 0:
                    del cnt[A[i]]
        else:
            for i in range(r,pr):
                cnt[A[i]] -= 1
                if cnt[A[i]] == 0:
                    del cnt[A[i]]
        submit[j] = len(cnt)
        pl,pr = l,r
    print(f"{time()-start}") 

    if ans == submit:
        print("OK")
    else:
        print("NG")
        print(A)
        print(LR)
        exit()
    print("ans:",ans[:10])
    print("sub:",submit[:10])
    
if __name__=='__main__':
    #plot()
    perf_sort()
    test()



