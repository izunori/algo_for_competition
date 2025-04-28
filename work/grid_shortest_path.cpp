#pragma GCC optimize("O3,inline")
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,tune=native")
#pragma GCC target("movbe")
#pragma GCC target("aes,pclmul,rdrnd")
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
using clk = std::chrono::system_clock;

template<int k>
const double p10_k = std::pow(10, k);

// global

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
    std::cerr << "(" << p.first << " " << p.second << ")";
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

constexpr int L = 100;
constexpr int M = 10000;
constexpr int inf = 1<<30;
const vec<i2> dirs{{1,0},{0,1},{-1,0},{0,-1}};

std::uniform_int_distribution<int> dist(0, L-1);

void bfs2D(vec<std::pair<i2,i2>>& sts, vec<int>& ans){
    auto start_time = clk::now();

    rep(m,M){
        const auto& [s,t] = sts[m];
        const auto& [sx,sy] = s;
        const auto& [tx,ty] = t;
        std::deque<i2> dq;
        dq.emplace_back(sx,sy);
        vec2<int> dist(L, vec<int>(L, inf));
        dist[sx][sy] = 0;
        while(!dq.empty()){
            const auto [x,y] = dq.front();
            dq.pop_front();
            if(x == tx && y == ty){
                break;
            }
            for(const auto& [dx,dy] : dirs){
                int nx = x+dx;
                int ny = y+dy;
                if(nx < 0 || L <= nx || ny < 0 || L <= ny) continue;
                if(dist[x][y] + 1 < dist[nx][ny]){
                    dist[nx][ny] = dist[x][y] + 1;
                    dq.emplace_back(nx,ny);
                }
            }
        }
        assert(dist[tx][ty] == ans[m]);
    }
    auto end_time = clk::now();
    double elapsed = getElapsed(start_time, end_time);
    dprint("bfs2D:", elapsed);
}

void bfs1D(vec<std::pair<i2,i2>>& sts, vec<int>& ans){
    auto start_time = clk::now();

    vec<i2> sts1d;
    for(const auto& [s,t] : sts){
        const auto& [sx,sy] = s;
        const auto& [tx,ty] = t;
        sts1d.emplace_back(sx*L + sy, tx*L + ty);
    }
    vec2<int> graph(L*L);
    rep(x,L){
        rep(y,L){
            int v = x*L + y;
            for(const auto& [dx,dy] : dirs){
                int nx = x+dx;
                int ny = y+dy;
                if(nx < 0 || L <= nx || ny < 0 || L <= ny) continue;
                int nv = nx*L + ny;
                graph[v].push_back(nv);
            }
        }
    }

    rep(m,M){
        const auto& [s,t] = sts1d[m];
        std::deque<int> dq;
        dq.emplace_back(s);
        vec<int> dist(L*L, inf);
        dist[s] = 0;
        while(!dq.empty()){
            const auto v = dq.front();
            dq.pop_front();
            if(v == t){
                break;
            }
            for(const auto nv : graph[v]){
                if(dist[v] + 1 < dist[nv]){
                    dist[nv] = dist[v] + 1;
                    dq.emplace_back(nv);
                }
            }
        }
        assert(dist[t] == ans[m]);
    }
    auto end_time = clk::now();
    double elapsed = getElapsed(start_time, end_time);
    dprint("bfs1D:", elapsed);
}

int main(){
    std::vector<std::pair<i2,i2>> sts;
    for(int m : std::views::iota(0,M)){
        int sx = dist(mt);
        int sy = dist(mt);
        int tx = dist(mt);
        int ty = dist(mt);
        sts.emplace_back(i2{sx,sy},i2{tx,ty});
    }
    vec<int> ans;
    for(const auto& [s,t] : sts){
        const auto& [sx,sy] = s;
        const auto& [tx,ty] = t;
        ans.push_back(std::abs(sx-tx) + std::abs(sy-ty));
    }
    bfs2D(sts, ans);
    bfs1D(sts, ans);
    
    deconstruct();
    return 0;
}
