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
    T** data = nullptr;
    T* buf = nullptr;
    Mat(int r, int c):r(r),c(c){
        id = _index;
        _index++;
        //dprint("create", id, this);
        buf = (T*)std::malloc((r*c) * sizeof(T));
        data = (T**)std::malloc(r * sizeof(T*));
        rep(i,r) data[i] = buf + i * c;
    }
    Mat(Mat && rhs){
        //dprint("Move");
        r = rhs.r; c = rhs.c;
        buf = rhs.buf; rhs.buf = nullptr;
        data = rhs.data; rhs.data = nullptr;
    }
    Mat& operator=(Mat&& rhs){
        r = rhs.r; c = rhs.c;
        //dprint("substitute", this, &rhs, r, c);
        buf = rhs.buf;
        data = rhs.data;
        rhs.buf = nullptr;
        rhs.data = nullptr;
        return *this;
    }
    Mat(const Mat &rhs){
        r = rhs.r; c = rhs.c;
        //dprint("copy", this, &rhs, r, c);
        buf = (T*)std::malloc((r*c) * sizeof(T));
        std::memcpy(buf, rhs.buf, (r*c)*sizeof(T));
        data = (T**)std::malloc(r * sizeof(T*));
        rep(i,r) data[i] = buf + i * c;
    }
    ~Mat(){
        //dprint("destroy", id, this, buf);
        if(buf != nullptr){
            std::free(buf);
            buf = nullptr;
        }
        if(data != nullptr){
            std::free(data);
            data = nullptr;
        }
    }
    Mat prod(const Mat& rhs){
        Mat res(r, rhs.c);
        //dprint("prod", &res);
        rep(x,r){
            rep(y,rhs.c){
                T t = 0;
                rep(i,c){
                    t += data[x][i] * rhs.data[i][y];
                }
                res.data[x][y] = t;
            }
        }
        return res;
    }
};

int main(){
    using Eigen::MatrixXd;

    int M = 200;
    int Q = 10;
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
        rep2(x,y,M) mm.data[x][y] = m(x,y);
        rep2(x,y,M) mm2.data[x][y] = m2(x,y);

        auto mm3 = mm;

        auto start_time = clk::now();
        rep(i,Q){
            mm3 = mm3.prod(mm2);
        }
        auto end_time = clk::now();

        dprint(mm3.data[0][0]);
        dprint(getElapsed(start_time, end_time));
    }

    return 0;
}
