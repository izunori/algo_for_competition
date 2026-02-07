#include"dprint.h"

template<typename T>
struct fastVector{
    vec<T> v;
    size_t _size = 0;
    fastVector(int cap = 20){
        v = vec<T>(cap, 0);
    }
    void push_back(T x){
        v[_size] = x;
        _size++;
    }
    void eraseFirst(T x){
        auto it = std::find(v.begin(), v.begin() + _size, x);
        std::iter_swap(it, v.begin() + (_size - 1));
        _size--;
    }
    void clear(){
        _size = 0;
    }
    bool empty(){
        return _size == 0;
    }
    size_t size(){
        return _size;
    }
    bool contains(T x){
        return std::find(v.begin(),v.begin()+_size, x) != v.begin() + _size;
    }
    auto begin() { return v.begin(); }
    auto end()   { return v.begin() + _size; }
    auto begin() const { return v.begin(); }
    auto end()   const { return v.begin() + _size; }
};

template<typename T>
struct fastVector2{
    vec2<T> vs;
    vec<int> _sizes;
    fastVector(int len, int cap = 20){
        vs = vec<T>(len, vec<T>(cap, 0));
        _sizes = vec<int>(len, 0);
    }
    vec<T>& operator[](int n) {
        return vs[n];
    }
    void push_back(T x){
        v[_size] = x;
        _size++;
    }
    void clear(){
        _size = 0;
    }
    bool empty(){
        return _size == 0;
    }
    size_t size(){
        return _size;
    }
    bool contains(T x){
        return std::find(v.begin(),v.begin()+_size, x) != v.begin() + _size;
    }
    auto begin() { return v.begin(); }
    auto end()   { return v.begin() + _size; }
    auto begin() const { return v.begin(); }
    auto end()   const { return v.begin() + _size; }
};

template<typename T>
struct fastDeque{
    vec<T> buf;
    T r = 0;
    T l = 0;
    fastDeque(size_t size){
        buf = vec<T>(size, -1);
    }
    T front(){
        return buf[l];
    }
    void pop_front(){
        l++;
    }
    void push_back(T x){
        buf[r] = x;
        r++;
    }
    bool empty(){
        return l == r;
    }
    size_t size(){
        return r-l;
    }

    void clear(){
        l = 0;
        r = 0;
    }
};

int main(){
    int M = 10000000;
    int N = 100;
    vec<i2> qs;
    vec<int> temp;
    rep(m,M){
        if(temp.empty()){
            int v = randint(N);
            qs.emplace_back(0,v);
            temp.push_back(v);
        } else {
            if(temp.size() < 20 && randbool()){
                int v = randint(N);
                qs.emplace_back(0,v);
                temp.push_back(v);
            } else {
                int i = randint(temp.size());
                int v = temp[i];
                qs.emplace_back(1,v);
                temp.erase(temp.begin()+i);
            }
        }
    }
    
    {
        auto start_time = clk::now();
        fastVector<int> v(100);
        for(const auto [q,x] : qs){
            if(q==0){
                v.push_back(x);
            } else {
                v.eraseFirst(x);
            }
        }
        auto end_time = clk::now();
        dprint(getElapsed(start_time, end_time));
    }
    {
        auto start_time = clk::now();
        vec<int> v;
        for(const auto [q,x] : qs){
            if(q==0){
                v.push_back(x);
            } else {
                auto it = std::find(v.begin(), v.end(), x);
                if(it!= v.end()) v.erase(it);
            }
        }
        auto end_time = clk::now();
        dprint(getElapsed(start_time, end_time));
    }
}
