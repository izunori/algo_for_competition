#include"./dprint.h"

constexpr int HASH_SIZE = 1<<22;
constexpr int HASH_MASK = HASH_SIZE-1;
struct fastHash{
    int scnt = 1;
    vec<ull> data = vec<ull>(HASH_SIZE, 0ull);
    vec<int> stamp = vec<int>(HASH_SIZE, 0);

    void clear(){
        scnt++;
    }
    bool insert(ull x) {
        uint i = x & HASH_MASK;
        while(stamp[i] == scnt && data[i] != x){
            i = (i+1) & HASH_MASK;
        }
        if(stamp[i] == scnt) return false;
        stamp[i] = scnt;
        data[i] = x;
        return true;
    }

    bool contains(ull x){
        uint i = x & HASH_MASK;
        while(stamp[i] == scnt){
            if(data[i] == x) return true;
            i = (i+1) & HASH_MASK;
        }
        return false;
    }
};


int main(){
}
