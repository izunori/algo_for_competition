#pragma GCC target("avx2")
#pragma GCC optimize("O3")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,tune=native")
#include<iostream>
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

#define rep(i, n) for (int i = 0; i < (int)n; i++)
#define rep2(i,j,n) for (int i = 0; i < (int)n; i++) for (int j = 0; j < (int)n; j++)
#define rep3(i,j,k,n) for (int i = 0; i < (int)n; i++) for (int j = 0; j < (int)n; j++) for (int k= 0; k < (int)n; k++)
#define all(v) v.begin(),v.end()

template<typename T>
using vec = std::vector<T>;
template<typename T>
using vec2 = vec<vec<T>>;
using ll = long long;
template<typename T>
using t2 = std::tuple<T, T>;
using i2 = t2<int>;
template<typename T>
using t3 = std::tuple<T, T, T>;
using clk = std::chrono::system_clock;

template<int k>
const double p10_k = std::pow(10, k);

// global

constexpr bool local = false;
std::map<std::string, std::string> LOG;

std::random_device rnd;
std::mt19937 mt(rnd());
std::uniform_real_distribution<> rand01(0.0, 1.0);

clk::time_point start_time;

// utils

template<typename T>
void print(const T& v){
    std::cout << v;
}
template<typename... T>
void print(const std::tuple<T...>& tp);
template<typename T>
void print(const std::vector<T>& vs){
    std::cout << "[";
    rep(i, vs.size()){
        if(i > 0) print(" ");
        print(vs[i]);
    }
    std::cout << "]";
}
template<typename TupType, size_t... I>
void print(const TupType& tp, std::index_sequence<I...>){
    std::cout << "(";
    (..., (print(I==0? "" : " "), print(std::get<I>(tp))));
    std::cout << ")";
}
template<typename... T>
void print(const std::tuple<T...>& tp){
    print(tp, std::make_index_sequence<sizeof...(T)>());
}
template<class T, class... A> void print(const T& first, const A&... rest) { print(first); print(" "); print(rest...); }

template<class... T>
void dprint(const T&... rest){
    std::cout << "# ";
    print(rest...);
    std::cout << "\n";
}

template<typename T>
void vprint(std::vector<T>& vs){
    for(const auto& v : vs){
        std::cout << v << " ";
    }
    std::cout << std::endl;
}

double getElapsed(clk::time_point& start, clk::time_point& end){
    return (std::chrono::duration<double, std::milli>(end-start)).count() / p10_k<3>;
}

vec<int> range(int n){
    vec<int> v(n);
    std::iota(all(v), 0);
    return v;
}

uint32_t xorShift() {
  static uint32_t y = 2463534242;
  y = y ^ (y << 13); y = y ^ (y >> 17);
  return y = y ^ (y << 5);
}

uint32_t randint(uint32_t size){
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

void initialize(){
}
void deconstruct(){
}

int N = 3000;
int Q = 10000000;
int M = 1000;

using tint = int;
using ti2 = std::tuple<tint, tint>;

struct st{
    tint a;
    tint b;
    st(int a, int b):a(a),b(b){};
};

void useTwoVec(vec<tint> va, vec<tint> vb, vec<i2>& squery){
    dprint("-- use two vector");
    auto start = clk::now();
    for(const auto& [i,j] : squery){
        std::swap(va[i], va[j]);
        std::swap(vb[i], vb[j]);
    }
    auto end = clk::now();
    dprint("swap:", getElapsed(start,end));
    start = clk::now();
    for(const auto& [i,j] : squery){
        va[i] += 1;
        vb[j] -= 1;
    }
    end = clk::now();
    dprint("operation:", getElapsed(start,end));
    int k = 0;
    start = clk::now();
    for(const auto& [i,j] : squery){
        k += va[i];
        k -= vb[j];
    }
    end = clk::now();
    dprint("access:", getElapsed(start,end), k);
}

void useLongVec(vec<tint> va, vec<tint> vb, vec<i2>& squery){
    vec<tint> v;
    rep(i,va.size()){
        v.push_back(va[i]);
        v.push_back(vb[i]);
    }
    dprint("-- use long vector");
    auto start = clk::now();
    for(const auto& [i,j] : squery){
        std::swap(v[2*i], v[2*j]);
        std::swap(v[2*i+1], v[2*j+1]);
    }
    auto end = clk::now();
    dprint("swap:", getElapsed(start,end));
    start = clk::now();
    for(const auto& [i,j] : squery){
        v[2*i] += 1;
        v[2*j+1] -= 1;
    }
    end = clk::now();
    dprint("operation:", getElapsed(start,end));
    int k = 0;
    start = clk::now();
    for(const auto& [i,j] : squery){
        k += v[2*i];
        k -= v[2*j+1];
    }
    end = clk::now();
    dprint("access:", getElapsed(start,end), k);
}

void useStructVec(vec<tint> va, vec<tint> vb, vec<i2>& squery){
    vec<st> v;
    rep(i,va.size()){
        v.emplace_back(st(va[i], vb[i]));
    }
    dprint("-- use struct vector");
    auto start = clk::now();
    for(const auto& [i,j] : squery){
        std::swap(v[i], v[j]);
    }
    auto end = clk::now();
    dprint("swap:", getElapsed(start,end));
    start = clk::now();
    for(const auto& [i,j] : squery){
        v[i].a += 1;
        v[j].b -= 1;
    }
    end = clk::now();
    dprint("operation:", getElapsed(start,end));
    int k = 0;
    start = clk::now();
    for(const auto& [i,j] : squery){
        k += v[i].a;
        k -= v[j].b;
    }
    end = clk::now();
    dprint("access:", getElapsed(start,end), k);
}
void useTuple(vec<tint> va, vec<tint> vb, vec<i2>& squery){
    vec<ti2> v;
    rep(i, va.size()) v.emplace_back(va[i], vb[i]);
    dprint("-- use Tuple");
    auto start = clk::now();
    for(const auto& [i,j] : squery){
        std::swap(v[i], v[j]);
    }
    auto end = clk::now();
    dprint("swap:", getElapsed(start,end));
    start = clk::now();
    for(const auto& [i,j] : squery){
        std::get<0>(v[i]) += 1;
        std::get<1>(v[j]) -= 1;
    }
    end = clk::now();
    dprint("operation:", getElapsed(start,end));
    int k = 0;
    start = clk::now();
    for(const auto& [i,j] : squery){
        k += std::get<0>(v[i]);
        k -= std::get<1>(v[j]);
    }
    end = clk::now();
    dprint("access:", getElapsed(start,end), k);
}

void useArray(vec<tint> va, vec<tint> vb, vec<i2>& squery){
    tint v[N][2];
    rep(i, va.size()){
        v[i][0] = va[i];
        v[i][1] = vb[i];
    }
    dprint("-- use Array");
    auto start = clk::now();
    for(const auto& [i,j] : squery){
        std::swap(v[i], v[j]);
    }
    auto end = clk::now();
    dprint("swap:", getElapsed(start,end));
    start = clk::now();
    for(const auto& [i,j] : squery){
        v[i][0] += 1;
        v[j][1] -= 1;
    }
    end = clk::now();
    dprint("operation:", getElapsed(start,end));
    int k = 0;
    start = clk::now();
    for(const auto& [i,j] : squery){
        k += v[i[0];
        k -= v[j][1];
    }
    end = clk::now();
    dprint("access:", getElapsed(start,end), k);
}
// main

int main(){
    initialize();
    vec<tint> va,vb;
    rep(i,N){
        va.push_back(randint(M));
        vb.push_back(randint(M));
    }
    vec<i2> squery;
    rep(i,Q){
        squery.emplace_back(randint(N), randint(N));
    }
    rep(i, 10){
        useTwoVec(va, vb, squery);
        useLongVec(va, vb, squery);
        useStructVec(va, vb, squery);
        useTuple(va, vb, squery);
        useArray(va, vb, squery);
        dprint("");
    }
    deconstruct();
    return 0;
}
