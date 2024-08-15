#include"./dprint.h"


template<typename T>
class SegmentTree{
public:
    size_t N;
    vec<T> data;
    std::function<T(T,T)> op;
    T e;
    size_t L;

    SegmentTree(std::vector<T> v, std::function<T(T,T)> op, T e):op(op),e(e){
        N = v.size();
        L = std::bit_ceil(N);
        data = vec<T>(L, e);
        data.insert(data.end(), v.begin(), v.end());
        data.insert(data.end(), L-N, e);
        for(int i = L-1; i > 0; i--){
            data[i] = op(data[i<<1], data[(i<<1)+1]);
        }
    }

    void set(int i, T val){
        i += L;
        data[i] = val;
        i >>= 1;
        while(i > 0){
            data[i] = op(data[i<<1], data[(i<<1)+1]);
            i >>= 1;
        }
    }

    T get(int i, int j){
        i += L; j += L;
        T s = e;
        while(j-i > 0){
            if(i&1){
                s = op(s, data[i]); i++;
            } else {
                s = op(s, data[j-1]), j--;
            }
            i >>= 1; j >>= 1;
        }
        return s;
    }
};

void test(){
    vec<int> v{1,2,3,4,5,6,7};

    auto add = [](int x, int y){return x+y;};
    auto seg = SegmentTree<int>(v, add, 0);

    int n = v.size();
    dprint(seg.get(0,n));
    dprint(seg.data);
    seg.set(0,10);
    dprint(seg.data);
    dprint(seg.get(0,n));
}

int main(){
    test();
    return 0;
}
