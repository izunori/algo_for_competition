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
#include"dprint.h"

int N = 10;

int index(int x, int y){
    return x*N + y;
}
i2 pos(int i){
    return {i/N, i%N};
}

int h(int v){
    // sholt be 0 <= h(v) <= true h(v)
    const auto [x,y] = pos(v);
    int nx = N/2;
    int ny = N/2;
    return (std::abs(x-nx) + std::abs(y-ny))/2;
}

int cost(int v, int nv){
    const auto [x,y] = pos(v);
    const auto [nx,ny] = pos(nv);
    return std::abs(x-nx) + std::abs(y-ny);
}

int main(){
    vec2<int> graph(N*N, vec<int>());
    vec<i2> dir{{1,0},{0,1},{-1,0},{0,-1}};
    rep(x,N){
        rep(y,N){
            int i = index(x,y);
            for(const auto& [dx,dy] : dir){
                int nx = x+dx;
                int ny = y+dy;
                if(!(0<=nx && nx < N && 0 <= ny && ny < N)) continue;
                int ni = index(nx,ny);
                graph[i].push_back(ni);
            }
        }
    }

    // open: generated (neighbors of expanded(closed) nodes)
    // closed: expanded (already searched)
    //         If you find more efficient path, closed will be open.
    // neither: to be.
    // if cost is already 1 => variable array for each f value.
    vec<bool> isClose(N*N,false);
    int inf = 99;
    vec<int> f(N*N,inf);
    std::priority_queue<i2,vec<i2>,std::greater<i2>> open;
    int s = index(0,0);
    int t = index(N/2,N/2);
    f[s] = h(s);
    open.emplace(f[s],s);
    vec<int> parent(N*N,-1);
    while(!open.empty()){
        const auto [fv,v] = open.top();
        dprint(fv,v);
        open.pop();
        if(f[v] < fv || isClose[v]) continue;
        if(v == t) break;
        isClose[v] = true;
        for(const auto nv : graph[v]){
            int fnv = (f[v] - h(v)) + cost(v,nv) + h(nv);
            open.emplace(fnv, nv);
            if(fnv < f[nv]){
                f[nv] = fnv;
                parent[nv] = v;
                if(isClose[nv]){
                    isClose[nv] = false;
                }
            }
        }
    }

    dprint(f[t] - h(t));
    rep(x,N){
        rep(y,N){
            std::cout << f[index(x,y)] - h(index(x,y)) << " ";
        }
        std::cout << std::endl;
    }
}
