from collections import defaultdict, deque
def stronglyConnectedComponent(g, N):
    visited = [False]*(N+1)
    order = []
    def dfs(s):
        visited[s] = True
        for ns in g[s]:
            if not visited[ns]:
                dfs(ns)
        order.append(s)
    for i in range(1,N+1):
        if not visited[i]:
            dfs(i)
    ig = defaultdict(list)
    for k,vs in g.items():
        for v in vs:
            ig[v].append(k)
    visited = [False]*(N+1)
    order.reverse()
    #print(order)
    res = []
    def dfs2(s,comp):
        visited[s] = True
        for ns in ig[s]:
            if not visited[ns]:
                dfs2(ns,comp)
        comp.append(s)
    for s in order:
        if visited[s]:
            continue
        comp = []
        dfs2(s,comp)
        res.append(comp)
    return res

# non recursive (maybe work)
def stronglyConnectedComponent2(g, N):
    visited = [False]*(N+1)
    order = []
    for s in range(1,N+1):
        if visited[s]:
            continue
        st = [s]
        while st:
            v = st.pop()
            if v < 0:
                order.append(-v)
                continue
            if visited[v]:
                continue
            visited[v] = True
            st.append(-v)
            for nv in g[v]:
                if not visited[nv]:
                    st.append(nv)
    ig = defaultdict(list)
    for k,vs in g.items():
        for v in vs:
            ig[v].append(k)
    visited = [False]*(N+1)
    order.reverse()
    res = []
    for s in order:
        if visited[s]:
            continue
        comp = []
        st = [s]
        while st:
            v = st.pop()
            if v < 0:
                comp.append(-v)
                continue
            if visited[v]:
                continue
            visited[v] = True
            st.append(-v)
            for nv in ig[v]:
                if not visited[nv]:
                    st.append(nv)
        res.append(comp)
    return res

def test():
    #sample = [(1,2),(2,3),(3,4),(4,2),(3,5),(5,6),(6,5),(4,7),(7,8),(8,9),(9,7),(7,10),(10,9),(9,11),(12,11)]
    import random
    N = 10
    M = 20
    sample = [(random.randint(1,N),random.randint(1,N)) for i in range(M)]
    #sample = [(2,4),(4,5),(5,4),(3,5),(2,3),(2,4)]
    print(sample)
    g = defaultdict(list)
    for u,v in sample:
        g[u].append(v)
    print(g)
    res = stronglyConnectedComponent(g, N)
    res2 = stronglyConnectedComponent2(g, N)
    print(res)
    print(res2)

if __name__=='__main__':
    test()






