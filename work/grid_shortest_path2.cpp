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

constexpr size_t L = 128;
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


uint32_t bfs2d(const vec2<int>& field, const i2& s, const i2& t){
    constexpr uint32_t inf = 1<<30;
    static const vec<i2> dirs = {{1,0},{0,1},{-1,0},{0,-1}};
    static std::deque<i2> dq;
    dq.clear();
    dq.emplace_back(s);
    static vec2<uint32_t> dist(L, vec<uint32_t>(L, inf));
    rep(i,L) std::ranges::fill(dist[i], inf);
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

uint32_t bfs1d(const vec2<int>& graph, const int s, const int t){
    constexpr uint32_t inf = 1<<30;
    static std::deque<int> dq;
    dq.clear();
    dq.push_back(s);
    static vec<uint32_t> dist(L*L);
    std::ranges::fill(dist, inf);
    dist[s] = 0;
    while(!dq.empty()){
        const auto v = dq.front();
        dq.pop_front();
        if(v==t) break;
        for(const auto nv : graph[v]){
            if(dist[v] + 1 < dist[nv]){
                dist[nv] = dist[v] + 1;
                dq.push_back(nv);
            }
        }
    }
    return dist[t];
}

vec2<int> make1dGraph(vec2<int>& field){
    size_t size = field.size();
    vec2<int> result(size * size);
    static const vec<i2> dirs = {{1,0},{0,1},{-1,0},{0,-1}};
    rep(x,size){
        rep(y,size){
            int v = size*x + y;
            for(const auto& [dx,dy] : dirs){
                int nx = x + dx;
                int ny = y + dy;
                if(nx < 0 || size <= nx || ny < 0 || size <= ny) continue;
                if(field[nx][ny]) continue;
                int nv = size*nx + ny;
                result[v].push_back(nv);
            }
        }
    }
    return result;
}

std::bitset<BIT_SIZE> makeBitBoard(const vec2<int>& field){
    std::bitset<BIT_SIZE> result;
    size_t size = field.size();
    rep(x, size){
        rep(y, size){
            if(field[x][y] == 1){
                result.set(x * size + y);
            }
        }
    }
    return result;
}

void printBitBoard(const std::bitset<BIT_SIZE>& bitboard, size_t size){
    if(!local) return;
    std::cerr << "BitBoard (" << size << "x" << size << "):\n";
    rep(x, size){
        rep(y, size){
            size_t pos = x * size + y;
            std::cerr << (bitboard.test(pos) ? '#' : '.');
        }
        std::cerr << "\n";
    }
    std::cerr << "\n";
}

uint32_t bfsBitBoard(const std::bitset<BIT_SIZE>& free_bit_board, int s, int t, size_t size){

    if(s==t) return 0;

    static auto current = std::bitset<BIT_SIZE>();
    static auto next = std::bitset<BIT_SIZE>();
    current.reset();
    current[s] = true;
    
    rep(d,BIT_SIZE){
        next = current;
        next |= (current&right_guard)<<1;
        next |= (current&left_guard)>>1;
        next |= (current>>size);
        next |= (current<<size);
        next &= free_bit_board;
        if(current == next){
            break;
        }
        if(next[t]) return d+1;
        std::swap(current, next);
    }
    return 1<<30;
}

int main(){
    vec<vec<int>> field(L, vec<int>(L, 0));
    const vec<i2> dirs{{1,0},{0,1},{-1,0},{0,-1}};
    rep(i,5){
        int x = randint(L);
        int y = randint(L);
        const auto [dx,dy] = dirs[randint(dirs.size())];
        while(0<=x && x < L && 0<= y && y < L){
            if(field[x][y] == 1) break;
            field[x][y] = 1;
            x += dx; y += dy;
        }
    }
    for(const auto row : field) dprint(row);

    rep(x,L){
        rep(y,L){
            int v = L*x + y;
            if(y < L-1) right_guard.set(v);
            if(0 < y) left_guard.set(v);
            if(0 < x) upper_guard.set(v);
            if(x < L-1) lower_guard.set(v);
        }
    }

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
    auto bit_board = makeBitBoard(field);
    auto free_bit_board = bit_board;
    free_bit_board.flip();
    vec2<int> sols(3);
    rep(i,3) sols[i].reserve(M);
    vec<ll> hash(3);

    rep(i,2){
    {
        auto start_time = clk::now();
        for(const auto& [start, end] : queries){
             int d = bfs2d(field, start, end);
             //sols[0].push_back(d);
             hash[0] += d;
        }
        auto end_time = clk::now();
        dprint("elapsed:", getElapsed(start_time, end_time));
    }
    {
        vec<uint32_t> dist;
        auto start_time = clk::now();
        for(const auto& [start, end] : queries1d){
            int d =bfs1d(graph, start, end);
            //sols[1].push_back(d);
            hash[1] += d;
        }
        auto end_time = clk::now();
        dprint("elapsed:", getElapsed(start_time, end_time));
    }
    {
        vec<uint32_t> dist;
        auto start_time = clk::now();
        for(const auto& [start, end] : queries1d){
            int d = bfsBitBoard(free_bit_board, start, end, L);
            //sols[2].push_back(d);
            hash[2] += d;
        }
        auto end_time = clk::now();
        dprint("elapsed:", getElapsed(start_time, end_time));
    }
    }
    //rep(i,3){
    //    dprint(sols[i]);
    //}
    dprint(hash);
    
    return 0;
}
