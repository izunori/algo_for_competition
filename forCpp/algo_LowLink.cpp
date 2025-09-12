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

struct LowLink{
    vec2<int>& g; // assume connected, 0,...,n-1, non-directd
    vec<int> in_work, ord, low, par, visited;
    vec<int> joints;

    LowLink(vec2<int>& g):g(g){
        in_work.assign(g.size(), 0);
        ord.assign(g.size(), -1);
        low.assign(g.size(), 0);
        par.assign(g.size(), -1);
        visited.assign(g.size(), 0);
        joints = vec<int>(g.size(), false);

        vec<int> st(1,0); // root: 0
        in_work[0] = true;
        int cnt = 0;
        while(!st.empty()){
            int v = st.back();
            st.pop_back();
            if(v < 0){
                v = -v;
                low[v] = ord[v];
                bool is_joint = false;
                for(const auto nv : g[v]){
                    if(!in_work[nv]){ // to leafs
                        if(!is_joint && (ord[v] <= low[nv])) is_joint = true;
                        if(low[nv] < low[v]) low[v] = low[nv];
                    } else if (par[v] != nv){ // to the root
                        if(low[v] > ord[nv]) low[v] = ord[nv];
                    }
                }
                if(is_joint) joints[v] = true;
                in_work[v] = false;
                continue;
            }
            if(visited[v]) continue;
            ord[v] = cnt++;
            in_work[v] = true;
            visited[v] = true;
            if(v > 0) st.push_back(-v);
            for(const auto nv : g[v]){
                if(visited[nv]) continue;
                par[nv] = v;
                st.push_back(nv);
            }
        }
        cnt = 0;
        for(const auto nv : g[0]){
            if(par[nv] == 0){
                ++cnt;
                if(cnt == 2){
                    joints[0] = true;
                    break;
                }
            }
        }
    }
    bool is_joint(int v){
        return joints[v];
    }
    bool is_bridge(int v, int u){
        return (ord[u] < low[v] || ord[v] < low[u]);
    }
};

int main(){
    //vec2<int> g{{1,4},{0,2,3},{1,3},{1,2},{0,5},{4}}; // [0,1,4]
    vec2<int> g{{1,4},{0,2,4},{1,3},{2},{0,1}}; // [1,2]
    //vec2<int> g{{1,3},{0,2},{1,3},{0,2}}; // []
    //vec2<int> g{{1,2,3,4},{0,2},{0,1},{0,4},{0,3}}; // []
    auto link = LowLink(g);
    dprint("ord",link.ord);
    dprint("low",link.low);
    dprint(link.joints);
    rep(v, g.size()){
        for(int u : g[v]){
            dprint(v,u,link.is_bridge(u,v));
        }
    }
}
