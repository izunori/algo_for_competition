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

template<typename T>
class Mat{
    public:
    T r,c;
    vec2<T> data;
    Mat(int r, int c):r(r),c(c){
        data = vec2<T>(r, vec<T>(c));
    }
    Mat prod(Mat& rhs){
        Mat res(r, rhs.c);
        rep(x,r){
            rep(y,rhs.c){
                rep(i,c){
                    res.data[x][y] += data[x][i] * rhs.data[i][y];
                }
            }
        }
        return res;
    }
};

int main(){
    using Eigen::MatrixXd;

    int M = 1000;
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
