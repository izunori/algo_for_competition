#include "dprint.h"

std::mt19937 mt(0);
std::uniform_real_distribution<double> uni(0, 1);

struct Slot{
    double p = 0.0;
    Slot(double p):p(p){
    }

    double play(){
        double q = uni(mt);
        return q < p ? 1.0 : 0.0;
    }
};

template<typename T>
size_t argmax(vec<T>& v){
    auto itr = std::max_element(v.begin(), v.end());
    return std::distance(v.begin(), itr);
}


int main(){

    int N = 4;
    int T = 2000;
    vec<Slot> slots{0.6, 0.65, 0.7, 0.71};

    vec<int> cnt(N, 0);
    vec<double> reward(N, 0.0);
    rep(n,N){
        cnt[n]++;
        reward[n] += slots[n].play();
    }
    vec<double> ucb(N, 0.0);
    for(int t = N+1; t < T; t++){
        rep(n,N){
            double logt = std::log((double)t);
            ucb[n] = reward[n] / cnt[n] + std::sqrt(logt / (2*cnt[n]));
        }
        int index = argmax(ucb);
        cnt[index]++;
        reward[index] += slots[index].play();
        dprint("ite:", t);
        dprint("cnt:", cnt);
        dprint("rew:", reward);
    }


    return 0;
}
