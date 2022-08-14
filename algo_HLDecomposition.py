from algo_Tour import *
def HLDecomposition(g,s=1):
    N = len(g)
    nch = [0]*(N+1)
    mnv = [-1]*(N+1)
    tour = TourFromLeaf(g,s)
    # depth, parentが必要
    for v,pv in tour:
        nch[v] += 1
        nch[pv] += nch[v]
        if nch[mnv[pv]] < nch[v]:
            mnv[pv] = v
    data,visited = [],[False]*(N+1)

    



def test():
    uv = [[1,2],[2,3],[1,4],[4,5],[4,6],[6,7],[7,8],[6,9]]
    g = [[] for _ in range(10)]
    for s,t in uv:
        g[s].append(t)
        g[t].append(s)
    HLDecomposition(g)


if __name__=='__main__':
    test()
