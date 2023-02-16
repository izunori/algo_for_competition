def MoSort(lr):
    l,r = zip(*lr)
    mx = max(max(l),max(r))
    block = mx // int(len(lr)**0.5)
    def val(x):
        n = x[0]//block
        return 2 * n * mx + (-1 if n&1 else 1)*x[1]
    lr.sort(key = val)

def perf():
    import random
    from time import perf_counter as time
    N = 2*10**5
    M = 2*10**5
    lr = [sorted([random.randint(0,M), random.randint(0,M)]) for _ in range(N)]
    start=time()
    lr = MoSort(lr)
    print(f"{time()-start}") 

def test():
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

if __name__=='__main__':
    #test()
    perf()



