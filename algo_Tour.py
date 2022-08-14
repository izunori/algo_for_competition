def TourFromLeaf(g,s=1):
    N = len(g)
    st,tour,p = [(s,-1)],[],[-1 for _ in range(N)]
    while st:
        v,pv = st.pop()
        if v < 0:
            tour.append((-v,pv))
            continue
        st.append((-v,pv))
        for nv in g[v]:
            if nv == p[v]:
                continue
            p[nv] = v
            st.append((nv,v))
    return tour

def test():
    g = [
            [],
            [2,3,7],
            [1,4,5],
            [6],
            [2],
            [2],
            [3],
            [1]
        ]
    print(TourFromLeaf(g))

if __name__=='__main__':
    test()



