//#pragma GCC optimize("O3,inline")
//#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")
//#pragma GCC optimize("unroll-loops")
//#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,tune=native")
//#pragma GCC target("movbe")
//#pragma GCC target("aes,pclmul,rdrnd")
#include<iostream>
#include<fstream>
#include<vector>
#include<string>
#include<tuple>
#include<chrono>
#include<map>
#include<set>
#include<algorithm>
#include<queue>
#include<random>
#include<numeric>
#include<functional>
#include<stack>
#include<cassert>
#include<cmath>
#include<cstring>
#include<unordered_set>
#include<unordered_map>
#include<ranges>
#include<bitset>
#include<bit>

#define rep(i, n) for (int i = 0; i < (int)n; i++)
#define reps(i, s, n) for (int i = s; i < (int)n; i++)
#define repv(x, v) for (const auto& x : v)
#define rep2(i,j,n) for (int i = 0; i < (int)n; i++) for (int j = 0; j < (int)n; j++)
#define rep3(i,j,k,n) for (int i = 0; i < (int)n; i++) for (int j = 0; j < (int)n; j++) for (int k= 0; k < (int)n; k++)
#define all(v) v.begin(),v.end()

template<typename T>
using vec = std::vector<T>;
template<typename T>
using vec2 = vec<vec<T>>;
template<typename T>
using vec3 = vec<vec2<T>>;
using ull = unsigned long long;
using ll = long long;
template<typename T>
using t2 = std::tuple<T, T>;
using i2 = std::pair<int,int>;
template<typename T>
using t3 = std::tuple<T, T, T>;
using i3 = t3<int>;
using clk = std::chrono::steady_clock;

template<int k>
const double p10_k = std::pow(10, k);

// global

constexpr size_t L = 64;
constexpr size_t BIT_SIZE = L*L;
auto right_guard = std::bitset<BIT_SIZE>();
auto left_guard = std::bitset<BIT_SIZE>();
auto upper_guard = std::bitset<BIT_SIZE>();
auto lower_guard = std::bitset<BIT_SIZE>();

constexpr bool local = true;
std::map<std::string, std::string> LOG;

std::random_device rnd;
std::mt19937 mt(rnd());
std::uniform_real_distribution<> rand01(0.0, 1.0);

clk::time_point start_time;
std::ofstream ofstr; // result file

// utils

template<typename T> void print(const T& v){ std::cerr << v; }
template<typename... T> void print(const std::tuple<T...>& tp);
template<typename T>
void print(const std::pair<T,T>& p){
    std::cerr << "(";
    print(p.first);
    std::cerr << " ";
    print(p.second);
    std::cerr << ")";
}
template<typename T>
void print(const std::vector<T>& vs){
    std::cerr << "[";
    rep(i, vs.size()){
        if(i > 0) print(" ");
        print(vs[i]);
    }
    std::cerr << "]";
}
template<typename TupType, size_t... I>
void print(const TupType& tp, std::index_sequence<I...>){
    std::cerr << "(";
    (..., (print(I==0? "" : " "), print(std::get<I>(tp))));
    std::cerr << ")";
}
template<typename... T>
void print(const std::tuple<T...>& tp){
    print(tp, std::make_index_sequence<sizeof...(T)>());
}
template<class T, class... A> void print(const T& first, const A&... rest) { print(first); print(" "); print(rest...); }
template<class... T>
void dprint(const T&... rest){
    if(!local) return;
    std::cerr << "# ";
    print(rest...);
    std::cerr << "\n";
}

double getElapsed(const clk::time_point& start, const clk::time_point& end){
    return (std::chrono::duration<double, std::milli>(end-start)).count() / 1000;
}

template<typename T>
T sum(const vec<T>& v){
    T res = 0;
    for(const auto x: v) res += x;
    return res;
}

template<typename T>
std::tuple<size_t,T> argmax(const vec<T>& v){
    T mx = std::numeric_limits<T>::lowest();
    size_t mi = 0;
    const int vsize = v.size();
    rep(i,vsize){
        if(mx < v[i]){
            mx = v[i]; mi = i;
        }
    }
    return {mi, mx};
}

template<typename T>
std::tuple<size_t,T> argmin(const vec<T>& v){
    T mx = std::numeric_limits<T>::max();
    size_t mi = 0;
    const int vsize = v.size();
    rep(i,vsize){
        if(mx > v[i]){
            mx = v[i]; mi = i;
        }
    }
    return {mi, mx};
}

vec<int> range(const int n){
    vec<int> v(n);
    std::iota(all(v), 0);
    return v;
}

uint32_t xorShift() {
  static uint32_t y = 2463534242;
  y = y ^ (y << 13); y = y ^ (y >> 17);
  return y = y ^ (y << 5);
}

uint32_t randint(const uint32_t size){
    uint32_t a = mt();
    uint64_t m = (uint64_t)a * (uint64_t) size;
    return m >> 32;
}

vec<int> sample(int mx, int num){
    vec<int> res;
    while(res.size() < num){
        res.emplace_back(randint(mx));
        std::sort(all(res));
        auto unique_end = std::unique(all(res));
        res.erase(unique_end, res.end());
    }
    return res;
}

int randbool(){
    return mt() & 1;
}

template<typename T>
vec<int> getOrderOf(vec<T>& v){
    auto res = range(v.size());
    std::sort(all(res),
        [&](int x, int y){return v[x] < v[y];}
    );
    return res;
}

// functions
const int LOG_TABLE_SIZE = 1 << 14;
double log_table[LOG_TABLE_SIZE];
inline double log_rand() {
    static int idx = 0;
    if (idx == LOG_TABLE_SIZE) {
        idx = 0;
    }
    return log_table[idx++];
}

void initialize(){
    if(local){
        ofstr = std::ofstream("./result.txt");
        std::ios_base::sync_with_stdio(false);
        std::cin.tie(0);
        auto original_buf = std::cout.rdbuf();
        std::cout.rdbuf(ofstr.rdbuf());
    }
    start_time = clk::now();
    for (int i = 0; i < LOG_TABLE_SIZE; i++) {
        log_table[i] = log(rand01(mt));
    }
}
void deconstruct(){
}

// main


uint32_t bfs2d(const vec2<int>& field, const i2& s, const i2& t){
    uint32_t inf = 1<<30;
    static const vec<i2> dirs = {{1,0},{0,1},{-1,0},{0,-1}};
    std::deque<i2> dq;
    dq.emplace_back(s);
    vec2<uint32_t> dist(L, vec<uint32_t>(L, inf));
    const auto& [sx,sy] = s;
    const auto& [tx,ty] = t;
    dist[sx][sy] = 0;
    while(!dq.empty()){
        const auto [x,y] = dq.front();
        dq.pop_front();
        if(x == tx && y == ty) break;
        for(const auto& [dx,dy] : dirs){
            int nx = x + dx;
            int ny = y + dy;
            if(nx < 0 || L <= nx || ny < 0 || L <= ny) continue;
            if(field[nx][ny]) continue;
            if(dist[x][y] + 1 < dist[nx][ny]){
                dist[nx][ny] = dist[x][y] + 1;
                dq.emplace_back(nx,ny);
            }
        }
    }
    return dist[tx][ty];
}

uint32_t Dijkstra(const vec2<i2>& graph, const int s, const int t){
    uint32_t inf = 1<<30;
    std::priority_queue<i2, vec<i2>, std::greater<i2>> hq;
    hq.emplace(0, s);
    vec<uint32_t> dist(L*L, inf);
    dist[s] = 0;
    while(!hq.empty()){
        const auto [c,v] = hq.top();
        hq.pop();
        if(v==t) break;
        if(dist[v] < c) continue;
        for(const auto [nv,dc] : graph[v]){
            if(dist[v] + dc < dist[nv]){
                dist[nv] = dist[v] + dc;
                hq.emplace(dist[nv], nv);
            }
        }
    }
    return dist[t];
}

template< typename T >
struct RadixHeap
{
  using uint = unsigned;
  std::vector< std::pair< uint, T > > v[33];
  uint size, last;

  RadixHeap() : size(0), last(0) {}

  bool empty() const { return size == 0; }

  inline int getbit(int a)
  {
    return a ? 32 - __builtin_clz(a) : 0;
  }

  void push(uint key, const T &value)
  {
    ++size;
    v[getbit(key ^ last)].emplace_back(key, value);
  }

  std::pair< uint, T > pop()
  {
    if(v[0].empty()) {
      int idx = 1;
      while(v[idx].empty()) ++idx;
      last = std::min_element(std::begin(v[idx]), std::end(v[idx]))->first;
      for(auto &p : v[idx]) v[getbit(p.first ^ last)].emplace_back(p);
      v[idx].clear();
    }
    --size;
    auto ret = v[0].back();
    v[0].pop_back();
    return ret;
  }
};

uint32_t DijkstraByRadixHeap(const vec2<i2>& graph, const int s, const int t){
    uint32_t inf = 1<<30;
    RadixHeap<int> hq;
    hq.push(0, s);
    vec<uint32_t> dist(L*L, inf);
    dist[s] = 0;
    while(!hq.empty()){
        const auto [c,v] = hq.pop();
        if(v==t) break;
        if(dist[v] < c) continue;
        for(const auto [nv,dc] : graph[v]){
            if(dist[v] + dc < dist[nv]){
                dist[nv] = dist[v] + dc;
                hq.push(dist[nv], nv);
            }
        }
    }
    return dist[t];
}

struct KQueue{
    vec2<int> qs;
    int max_size;
    int size = 0;
    KQueue(int max_size):max_size(max_size){
        qs = vec2<int>(max_size);
    }
    void push(int c, int s){
        qs[c].push_back(s);
        size++;
    }
    i2 pop(){
        size--;
        rep(c,max_size){
            if(!qs[c].empty()){
                int res = qs[c].back();
                qs[c].pop_back();
                return {c,res};
            }
        }
    }
    bool empty(){
        return size == 0;
    }
};

uint32_t DijkstraByKBFS(const vec2<i2>& graph, const int s, const int t){
    uint32_t inf = 1<<30;
    auto kq = KQueue(1000);
    kq.push(0, s);
    vec<uint32_t> dist(L*L, inf);
    dist[s] = 0;
    while(!kq.empty()){
        const auto [c,v] = kq.pop();
        if(v==t) break;
        if(dist[v] < c) continue;
        for(const auto [nv,dc] : graph[v]){
            if(dist[v] + dc < dist[nv]){
                dist[nv] = dist[v] + dc;
                kq.push(dist[nv], nv);
            }
        }
    }
    return dist[t];
}

vec2<i2> make1dGraph(vec2<int>& field){
    size_t size = field.size();
    vec2<i2> result(size * size);
    static const vec<i2> dirs = {{1,0},{0,1},{-1,0},{0,-1}};
    rep(x,size){
        rep(y,size){
            int v = size*x + y;
            for(const auto& [dx,dy] : dirs){
                int nx = x + dx;
                int ny = y + dy;
                if(nx < 0 || size <= nx || ny < 0 || size <= ny) continue;
                int nv = size*nx + ny;
                result[v].emplace_back(nv, field[nx][ny]);
            }
        }
    }
    return result;
}

int main(){
    vec<vec<int>> field(L, vec<int>(L, 0));
    const vec<i2> dirs{{1,0},{0,1},{-1,0},{0,-1}};
    rep(x,L){
        rep(y,L){
            field[x][y] = randint(10);
        }
    }
    for(const auto row : field) dprint(row);


    constexpr int M = 10000;
    using Query = std::pair<i2,i2>;
    vec<Query> queries;
    vec<i2> queries1d;
    rep(i,M){
        int start_x, start_y, end_x, end_y;
        while(true){
            start_x = randint(L);
            start_y = randint(L);
            if(!field[start_x][start_y]) break;
        }
        while(true){
            end_x = randint(L);
            end_y = randint(L);
            if(!field[end_x][end_y]) break;
        }
        queries.emplace_back(i2{start_x, start_y}, i2{end_x, end_y});
        queries1d.emplace_back(L*start_x + start_y, L*end_x + end_y);
    }

    auto graph = make1dGraph(field);
    vec2<int> sols(3);
    rep(i,3) sols[i].reserve(M);

    {
        auto start_time = clk::now();
        for(const auto& [start, end] : queries1d){
             int d = Dijkstra(graph, start, end);
             sols[0].push_back(d);
        }
        auto end_time = clk::now();
        dprint("elapsed:", getElapsed(start_time, end_time));
    }
    {
        auto start_time = clk::now();
        for(const auto& [start, end] : queries1d){
             int d = DijkstraByRadixHeap(graph, start, end);
             sols[1].push_back(d);
        }
        auto end_time = clk::now();
        dprint("elapsed:", getElapsed(start_time, end_time));
    }
    {
        auto start_time = clk::now();
        for(const auto& [start, end] : queries1d){
             int d = DijkstraByRadixHeap(graph, start, end);
             sols[2].push_back(d);
        }
        auto end_time = clk::now();
        dprint("elapsed:", getElapsed(start_time, end_time));
    }
    //dprint(queries);
    //rep(i,3){
    //    rep(j,10){
    //        dprint(sols[i][j]);
    //    }
    //}
    
    return 0;
}
