#pragma GCC optimize("O3,inline")
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,tune=native")
#pragma GCC target("movbe")
#pragma GCC target("aes,pclmul,rdrnd")
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
#include<Eigen/Dense>

int _index = 0;

template<typename T>
class Mat{
public:
    int id = 0;
    int r,c;
    //vec2<T> data;
    //T** data = nullptr;
    T* buf = nullptr;
    Mat(int r, int c):r(r),c(c){
        id = _index;
        _index++;
        //dprint("create", id, this);
        buf = (T*)std::calloc((r*c), sizeof(T));
        //data = (T**)std::malloc(r * sizeof(T*));
        //rep(i,r) data[i] = buf + i * c;
    }
    Mat(Mat && rhs){
        //dprint("Move");
        r = rhs.r; c = rhs.c;
        buf = rhs.buf; rhs.buf = nullptr;
        //data = rhs.data; rhs.data = nullptr;
    }
    Mat& operator=(Mat&& rhs){
        r = rhs.r; c = rhs.c;
        //dprint("substitute", this, &rhs, r, c);
        buf = rhs.buf;
        //data = rhs.data;
        rhs.buf = nullptr;
        //rhs.data = nullptr;
        return *this;
    }
    Mat(const Mat &rhs){
        r = rhs.r; c = rhs.c;
        //dprint("copy", this, &rhs, r, c);
        buf = (T*)std::malloc((r*c) * sizeof(T));
        std::memcpy(buf, rhs.buf, (r*c)*sizeof(T));
        //data = (T**)std::malloc(r * sizeof(T*));
        //rep(i,r) data[i] = buf + i * c;
    }
    ~Mat(){
        if(buf != nullptr){
            dprint("destroy", id, this, buf);
            std::free(buf);
            buf = nullptr;
        }
        //if(data != nullptr){
        //    std::free(data);
        //    data = nullptr;
        //}
    }
    Mat prod(const Mat& rhs){
        Mat res(r, rhs.c);
        //dprint("prod", &res);
        rep(x,r){
            rep(i,c){
                rep(y,rhs.c){
                    res.buf[x*rhs.c + y] += buf[c*x+ i] * rhs.buf[rhs.c * i + y];
                }
            }
        }
        return res;
    }
    T& operator()(const int x, const int y){
        return buf[x*c + y];
    }

};

int main(){
    using Eigen::MatrixXd;

    int M = 1000;
    int Q = 1;
    Eigen::MatrixXd m = MatrixXd::Random(M,M);
    Eigen::MatrixXd m2 = MatrixXd::Random(M,M);
    {
        auto m3 = m;

        auto start_time = clk::now();
        rep(i,Q){
            m3 = m3 * m2;
        }
        auto end_time = clk::now();

        dprint(m3(0,0));
        dprint(getElapsed(start_time, end_time));
    }

    {
        Mat<double> mm(M,M);
        Mat<double> mm2(M,M);
        rep2(x,y,M) mm(x,y) = m(x,y);
        rep2(x,y,M) mm2(x,y) = m2(x,y);

        auto mm3 = mm;

        auto start_time = clk::now();
        rep(i,Q){
            mm3 = mm3.prod(mm2);
        }
        auto end_time = clk::now();

        dprint(mm3(0,0));
        dprint(getElapsed(start_time, end_time));
    }

    return 0;
}
