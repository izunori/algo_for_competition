class Trie:
    def __init__(self):
        self.top = {}
    def add(self, word):
        v = self.top
        for s in word[:-1]:
            if not s in v:
                v[s] = [{},0]
            v = v[s][0]
        s = word[-1]
        if not s in v:
            v[s] = [{}, 1]
        else:
            v[s][1] += 1
    def exist(self, word):
        v = self.top
        for s in word[:-1]:
            if not s in v:
                return 0
            v = v[s][0]
        s = word[-1]
        if not s in v:
            return 0
        else:
            return v[s][1]

class TrieP:
    # manage 0 <= x < P
    def __init__(self, P):
        self.P = P
        self.data = [[0]*(P+1)]
        self.cnt = 0
    def add(self, word):
        v = self.data[0]
        for s in word:
            if not v[s]:
                self.cnt += 1
                self.data.append([0]*(self.P+1))
                v[s] = self.cnt
            v = self.data[v[s]]
        v[self.P] += 1
    def exist(self, word):
        v = self.data[0]
        for s in word:
            if not v[s]:
                return 0
            v = self.data[v[s]]
        return v[self.P]

def test():
    import random
    N = 100
    M = 10
    P = 26
    samples = [[random.randint(0,P) for i in range(random.randint(1,M))] for j in range(N)]
    trie = Trie()
    triep = TrieP(P+1)
    for sample in samples:
        trie.add(sample)
        triep.add(sample)
    samples2 = [[random.randint(0,P) for i in range(random.randint(1,M))] for j in range(N)]
    for sample in samples2:
        print(trie.exist(sample), triep.exist(sample), sample in samples)

def perf():
    import random
    from time import perf_counter as time
    N = 2*10**4
    M = 100
    P = 2
    samples = [[random.randint(0,P) for i in range(random.randint(1,M))] for j in range(N)]
    trie = Trie()
    start = time()
    for sample in samples:
        trie.add(sample)
    print(f"{time() - start}")

    trie = TrieP(P+1)
    start = time()
    for sample in samples:
        trie.add(sample)
    print(f"{time() - start}")

if __name__=='__main__':
    test()
    perf()
