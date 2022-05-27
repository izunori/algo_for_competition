#include<iostream>
#include<vector>
#include<algorithm>
#include<random>
#include<chrono>
#define PRINT(text) (std::cout << (text) << std::endl);
#define VPRINT(vec) for(const auto& x:vec){std::cout << x << ' ';};

template<typename T>
T powMod(T p, T n, T m){
    T res = 1ll;
    while(n){
        if(n&1) res = (res*p)%m;
        p = (p*p)%m;
        n >>= 1;
    }
    return res;
}

template<typename T>
int bitLength(T i){
    int res = 0;
    while(i){
        i >>= 1;
        res++;
    }
    return res;
}

class NTT{
    using ll = long long;
    public:
    const ll MOD = 998244353;
    const ll K = 119;
    const ll M = 23;
    const ll Q = 31;
    std::vector<ll> ws = std::vector<ll>(M+1);
    std::vector<ll> iws = std::vector<ll>(M+1);

    NTT(){
        for(ll i = 0; i < M+1; i++){
            ws[i] = powMod(Q, 1ll<<(M-i), MOD);
            iws[i] = powMod(ws[i], MOD-2, MOD);
        }
    };
    void ntt(std::vector<ll>& A){
        if(A.size() == 1) return;
        int n = A.size();
        int k = bitLength(n-1);
        int r = 1<<(k-1);
        int s = 0;
        for(int m = k; m > 0; m--){
            for(int l = 0; l < n; l+=2*r){
                ll wi = 1;
                for(int i = 0; i < r; i++){
                    s = (A[l+i]+A[l+i+r])%MOD;
                    A[l+i+r] = (A[l+i]-A[l+i+r])*wi%MOD;
                    A[l+i] = s;
                    wi = wi*ws[m]%MOD;
                }
            }
            r /= 2;
        }
    }
    void intt(std::vector<ll>& A){
        if(A.size() == 1) return;
        ll n = A.size();
        int k = bitLength(n-1);
        int r = 1;
        int s = 0;
        for(int m = 1; m < k+1; m++){
            for(int l = 0; l < n; l+=2*r){
                ll wi = 1;
                for(int i = 0; i < r; i++){
                    s = (A[l+i]+A[l+i+r]*wi)%MOD;
                    A[l+i+r] = (A[l+i]-A[l+i+r]*wi)%MOD;
                    A[l+i] = s;
                    wi = wi*iws[m]%MOD;
                }
            }
            r *= 2;
        }
        ll ni = powMod(n, MOD-2, MOD);
        for(int i = 0; i < n; i++){
            A[i] = A[i]*ni%MOD;
            if(A[i]<0) A[i] += MOD;
        }
    }
    void polymul(std::vector<ll>& f, std::vector<ll>& g) {
        int nf = f.size();
        int ng = g.size();
        int m = nf+ng-1;
        int n = 1<<bitLength(m-1);
        for(int i = 0; i < nf; i++){
            f[i] = f[i]%MOD;
        }
        for(int i = 0; i < ng; i++){
            g[i] = g[i]%MOD;
        }
        f.resize(n, 0);
        g.resize(n, 0);
        ntt(f);
        ntt(g);
        for(int i = 0; i < n; i++){
            f[i] = f[i]*g[i]%MOD;
        }
        intt(f);
    }

};

int main(){
    NTT ntt = NTT();
    std::vector<long long> f = {1,2,3};
    std::vector<long long> g = {4,5,6};
    ntt.polymul(f,g);
    VPRINT(f);
    int N = 1000000;
    int M = 100;
    int MOD = 998244353;
    std::mt19937 e;
    std::uniform_int_distribution<long long> d(0, MOD-1);
    for(int i = 0; i < M; i++){
        f.resize(N);
        g.resize(N);
        for(int j = 0; j < N; j++){
            f[j] = d(e);
            g[j] = d(e);
        }
        auto start = std::chrono::system_clock::now();
        ntt.polymul(f,g);
        auto end = std::chrono::system_clock::now();
        auto dur = end - start;
        auto nsec = std::chrono::duration_cast<std::chrono::nanoseconds>(dur).count();
        PRINT((double)nsec/(1000000000));
    }
}
