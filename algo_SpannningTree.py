import heapq as hq
# MST (Minumum Spanning Tree)

# cost : key:(v,nv) value:int
def Prim(g,cost):
    h = []
    N = len(g.keys())
    visited = [False]*(N+1)
    visited[1] = True
    v = 1
    for nv in g[v]:
        hq.heappush(h, (cost[(v,nv)], (v,nv)))
    res = []
    d = 0
    while True:
        c, (v,nv) = hq.heappop(h)
        if visited[nv]:
            continue
        res.append((v,nv))
        d += c
        if len(res) == N-1:
            break
        visited[nv] = True
        for nnv in g[nv]:
            if not visited[nnv]:
                hq.heappush(h, (cost[(nv,nnv)], (nv,nnv)))
    return res, d

def test():
    pass

if __name__=='__main__':
    test()
