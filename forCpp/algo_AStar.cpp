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
using i3 = t3<int>;
using clk = std::chrono::system_clock;
using i4 = std::tuple<int,int,int,int>;

template<typename T>
using vec = std::vector<T>;

int N = 100;

class AStar{

};


int index(int x, int y){
    return x*N + y;
}

int main(){
    vec2<int> g(N, vec<int>());
    vec<i2> dir{{1,0},{0,1},{-1,0},{0,-1}};
    rep(x,N){
        rep(y,N){
            int i = index(x,y);
            for(const auto& [dx,dy] : dir){
                int nx = x+dx;
                int ny = y+dy;
                if(!(0<=nx && nx < N && 0 <= ny && ny < N)) continue;
                int ni = index(nx,ny);
                g[i].push_back(ni);
            }
        }
    }
}
