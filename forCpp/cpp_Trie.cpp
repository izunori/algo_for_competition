#include"dprint.h"
struct Trie {
    struct Node {
        std::array<int, 26> next;
        int count = 0;
        Node() { next.fill(-1); }
    };

    std::vector<Node> nodes{1};

    void add(std::string_view word) {
        int v = 0;
        for (char c : word) {
            int k = c - 'A';
            if (nodes[v].next[k] == -1) {
                int u = nodes.size();
                nodes[v].next[k] = u;
                nodes.emplace_back();
            }
            v = nodes[v].next[k];
        }
        ++nodes[v].count;
    }

    int exist(std::string_view word) const {
        int v = 0;
        for (char c : word) {
            v = nodes[v].next[c - 'A'];
            if (v == -1) return 0;
        }
        return nodes[v].count;
    }
};

int main() {
    std::mt19937 rng(42);

    auto randint = [&](int l, int r) {
        return std::uniform_int_distribution<int>(l, r)(rng);
    };

    // test()
    {
        constexpr int N = 1000, M = 10, P = 25;

        std::vector<std::string> samples, samples2;

        auto generate = [&]() {
            std::string s;
            int len = randint(1, M);
            for (int i = 0; i < len; ++i)
                s += char('A' + randint(0, P));
            return s;
        };

        for (int i = 0; i < N; ++i) samples.push_back(generate());
        for (int i = 0; i < N; ++i) samples2.push_back(generate());

        Trie trie;
        for (auto& s : samples) trie.add(s);

        for (auto& s : samples2) {
            int a = trie.exist(s);
            int b = std::count(samples.begin(), samples.end(), s);
            std::cout << a << " " << b << '\n';
            assert(a == b);
        }
    }

    // perf()
    {
        constexpr int N = 20000, M = 100, P = 2;

        std::vector<std::string> samples;

        for (int i = 0; i < N; ++i) {
            std::string s;
            int len = randint(1, M);
            for (int j = 0; j < len; ++j)
                s += char('A' + randint(0, P));
            samples.push_back(std::move(s));
        }

        Trie trie;

        auto start = std::chrono::steady_clock::now();

        for (auto& s : samples)
            trie.add(s);

        auto end = std::chrono::steady_clock::now();

        std::cout << "Time: "
                  << std::chrono::duration<double>(end - start).count()
                  << " sec\n";
    }
}
