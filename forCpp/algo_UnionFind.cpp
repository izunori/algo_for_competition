#include<vector>
#include<iostream>
class UnionFind{
public:
    std::vector<int> buf;
    UnionFind(int n){
        buf = std::vector<int>(n, -1);
    }
    int root(int x){
        return (buf[x] < 0) ? x : buf[x] = root(buf[x]);
    }
    bool find(int x, int y){
        return root(x) == root(y);
    }
    bool unit(int x, int y){
        int rx = root(x);
        int ry = root(y);
        if(rx == ry) return false;
        if(rx > ry){ // y belongs to bigger group
            buf[ry] += buf[rx];
            buf[rx] = ry;
        } else {
            buf[rx] += buf[ry];
            buf[ry] = rx;
        }
        return true;
    }
};

class UnionFind2{
public:
    int n;
    std::vector<int> parent;
    std::vector<int> rank;
    UnionFind2(int n):n(n){
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
    std::cout << "1=" << uf.find(7,8) << std::endl;
    std::cout << "0=" << uf.find(1,8) << std::endl;
    std::cout << "1=" << uf.find(1,5) << std::endl;
}

