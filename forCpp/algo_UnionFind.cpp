#include<vector>
#include<iostream>
class UnionFind{
public:
    int n;
    std::vector<int> parent;
    std::vector<int> rank;
    UnionFind(int n):n(n){
        parent = std::vector<int>(n);
        rank = std::vector<int>(n,1);
        for(int i = 0; i < n; i++){
            parent[i] = i;
        }
    }
    int root(int x){
        if(x==parent[x]){
            return x;
        }
        int rt = root(parent[x]);
        parent[x] = rt;
        return rt;
    }
    bool find(int x, int y){
        return parent[x] == parent[y];
    }
    bool unit(int x, int y){
        int rx = root(x);
        int ry = root(y);
        if(rx == ry) return false;
        if(rank[rx] > rank[ry]){
            parent[y] = rx;
        } else if (rank[rx] < rank[ry]){
            parent[x] = ry;
        } else {
            parent[x] = ry;
            rank[ry] += 1;
        }
        return true;
    }
};

int main(){
    auto uf = UnionFind(10);
    uf.unit(0,8);
    uf.unit(0,7);
    uf.unit(1,5);
    std::cout << uf.find(7,8) << std::endl;
    std::cout << uf.find(1,8) << std::endl;
    std::cout << uf.find(1,5) << std::endl;
}

