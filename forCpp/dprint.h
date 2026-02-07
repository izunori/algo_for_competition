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

#define rep(i, n) for (int i = 0; i < (int)n; i++)
#define rep2(i,j,n) for (int i = 0; i < (int)n; i++) for (int j = 0; j < (int)n; j++)
#define rep3(i,j,k,n) for (int i = 0; i < (int)n; i++) for (int j = 0; j < (int)n; j++) for (int k= 0; k < (int)n; k++)
//#define all(v) v.begin(),v.end()

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
using i3 = t3<int>;
using clk = std::chrono::system_clock;
using i4 = std::tuple<int,int,int,int>;

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

double getElapsed(clk::time_point& start, clk::time_point& end){
    return (std::chrono::duration<double, std::milli>(end-start)).count() / 1000;
}

uint32_t xorShift() {
  static uint32_t y = 2463534242;
  y = y ^ (y << 13); y = y ^ (y >> 17);
  return y = y ^ (y << 5);
}

uint32_t randint(const uint32_t size){
    uint32_t a = xorShift();
    uint64_t m = (uint64_t)a * (uint64_t) size;
    return m >> 32;
}

bool randbool(){
    return xorShift() & 1;
}
