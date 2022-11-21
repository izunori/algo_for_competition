#include<iostream>
#include<vector>
#include<algorithm>
#include<random>
#include<chrono>

#define PRINT(text) (std::cout << (text) << std::endl);
#define VPRINT(vec) for(const auto& x:vec){std::cout << x << ' ';};std::cout << std::endl;

using ll = long long;

template<typename T>
constexpr T powMod(T p, T n, T m){
    T res = 1ll;
    while(n){
        if(n&1) res = (res*p)%m;
        p = (p*p)%m;
        n >>= 1;
    }
    return res;
}

template<typename T>
const int bitLength(T i){
    int res = 0;
    while(i){
        i >>= 1;
        res++;
    }
    return res;
}

template<typename T>
constexpr int getFactor(T i){
    int res = 0;
    while((i&1)==0){
        res += 1;
        i >>= 1;
    }
    return res;
}

//constexpr long long MOD = 998244353;
//const long long K = 119;
//const long long M = 23;
//const long long Q = 31;
constexpr long long MOD = 167772161;
constexpr long long K = 5;
constexpr long long M = 25;
constexpr long long IK = powMod(K,MOD-2,MOD);
constexpr long long IK2 = (IK*IK)%MOD;
constexpr long long Q = 17;
constexpr long long K2 = (K*K)%MOD;
constexpr long long mask = (1<<M)-1;

class NTT{
    public:

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
        for(int m = k; m > 0; m--){
            for(int l = 0; l < n; l+=2*r){
                ll wi = 1;
                for(int i = 0; i < r; i++){
                    ll s = (A[l+i]+A[l+i+r])%MOD;
                    A[l+i+r] = (A[l+i]-A[l+i+r])*wi%MOD;
                    A[l+i] = s;
                    wi = wi*ws[m]%MOD;
                }
            }
            r >>= 1;
        }
        for(int i = 0; i < n; i++){
            A[i] = A[i] % MOD;
            if(A[i]<0) A[i] += MOD;
        }
    }
    void intt(std::vector<ll>& A){
        if(A.size() == 1) return;
        ll n = A.size();
        int k = bitLength(n-1);
        int r = 1;
        for(int m = 1; m < k+1; m++){
            for(int l = 0; l < n; l+=2*r){
                ll wi = 1;
                for(int i = 0; i < r; i++){
                    ll s = (A[l+i]+A[l+i+r]*wi)%MOD;
                    A[l+i+r] = (A[l+i]-A[l+i+r]*wi)%MOD;
                    A[l+i] = s;
                    wi = wi*iws[m]%MOD;
                }
            }
            r <<= 1;
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

class NTTRed{
    public:

    std::vector<ll> ws = std::vector<ll>(M+1);
    std::vector<ll> iws = std::vector<ll>(M+1);
    std::vector<ll> wsik2 = std::vector<ll>(M+1);
    std::vector<ll> iwsik2 = std::vector<ll>(M+1);

    NTTRed(){
        for(ll i = 0; i < M+1; i++){
            ws[i] = powMod(Q, 1ll<<(M-i), MOD);
            wsik2[i] = ws[i]*IK2%MOD;
            iws[i] = powMod(ws[i], MOD-2, MOD);
            iwsik2[i] = iws[i]*IK2%MOD;
        }
    };
    const long long k_red(const long long c){
        return K*(c&mask) - (c>>M);
    }
    const long long k_red_2x(const long long c){
        return (K2*(c&mask)) - (K*((c>>M)&mask)) + (c>>(M*2));
    }
    void ntt(std::vector<ll>& A){
        if(A.size() == 1) return;
        int n = A.size();
        int k = bitLength(n-1);
        int r = 1<<(k-1);
        ll kik = powMod(IK,(long long)k,MOD);
        for(int i = 0; i < n; i++){
            A[i] = A[i]*kik%MOD;
            if(A[i]<0) A[i] += MOD;
        }
        for(int m = k; m > 0; m--){
            for(int l = 0; l < n; l+=2*r){
                ll wi = IK;
                for(int i = 0; i < r; i++){
                    ll s = k_red(A[l+i]+A[l+i+r]);
                    A[l+i+r] = k_red_2x((A[l+i]-A[l+i+r])*wi);
                    A[l+i] = s;
                    wi = k_red_2x(wi*wsik2[m]);
                }
            }
            r >>= 1;
        }
        for(int i = 0; i < n; i++){
            A[i] = A[i] % MOD;
            if(A[i]<0) A[i] += MOD;
        }
    }
    void intt(std::vector<ll>& A){
        if(A.size() == 1) return;
        ll n = A.size();
        int k = bitLength(n-1);
        int r = 1;

        ll kik2 = powMod(IK2,(long long)k,MOD);
        for(int i = 0; i < n; i++){
            A[i] = A[i]*kik2%MOD;
        }

        for(int m = 1; m < k+1; m++){
            for(int l = 0; l < n; l+=2*r){
                ll wi = 1;
                for(int i = 0; i < r; i++){
                    ll s = k_red_2x(A[l+i]+A[l+i+r]*wi);
                    A[l+i+r] = k_red_2x(A[l+i]-A[l+i+r]*wi);
                    A[l+i] = s;
                    //wi = wi*iws[m]%MOD;
                    wi = k_red_2x(wi*iwsik2[m]);
                }
            }
            r <<= 1;
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

std::vector<long long> greedy(std::vector<long long>& f, std::vector<long long>& g){
    int n1 = f.size();
    int n2 = g.size();
    int m = n1 + n2 - 1;
    auto fg = std::vector<long long>(m);
    for(int i = 0; i < n1; i++){
        for(int j = 0; j < n2; j++){
            fg[i+j] += f[i]*g[j];
            fg[i+j] %= MOD;
        }
    }
    return fg;
}

void test(){
    NTT ntt = NTT();
    NTTRed ntt_red = NTTRed();
    //int N = 10;
    //int M = 100;
    //std::mt19937 e;
    //std::uniform_int_distribution<long long> d(0, MOD-1);

    //auto f = std::vector<long long>(N);
    //auto f2 = std::vector<long long>(N);
    //auto g = std::vector<long long>(N);
    //for(int j = 0; j < N; j++){
    //    f[j] = d(e);
    //    f2[j] = d(e);
    //    g[j] = d(e);
    //}
    std::vector<long long> f = {1,2,3};
    std::vector<long long> f2 = {1,2,3};
    std::vector<long long> g = {4,5,6};
    std::vector<long long> g2 = {4,5,6};
    auto fg = greedy(f,g);
    VPRINT(fg);
    ntt.polymul(f,g);
    VPRINT(f);
    ntt_red.polymul(f2,g2);
    VPRINT(f2);
}

int main(){
    NTT ntt = NTT();
    NTTRed ntt_red = NTTRed();
    int N = 1000000;
    int M = 100;
    std::mt19937 e;
    auto f = std::vector<long long>(N);
    auto g = std::vector<long long>(N);
    auto f2 = std::vector<long long>(N);
    auto g2 = std::vector<long long>(N);
    for(int i = 0; i < M; i++){
        f.resize(N);
        g.resize(N);
        f2.resize(N);
        g2.resize(N);
        std::uniform_int_distribution<long long> d(0, MOD-1);
        for(int j = 0; j < N; j++){
            long long x = d(e);
            long long y = d(e);
            f[j] = x;
            f2[j] = x;
            g[j] = y;
            g2[j] = y;
        }
        auto start = std::chrono::system_clock::now();
        ntt.polymul(f,g);
        auto end = std::chrono::system_clock::now();
        auto dur = end - start;
        auto nsec = std::chrono::duration_cast<std::chrono::nanoseconds>(dur).count();
        PRINT((double)nsec/(1000000000));

        auto start2 = std::chrono::system_clock::now();
        ntt_red.polymul(f2,g2);
        auto end2 = std::chrono::system_clock::now();
        auto dur2 = end2 - start2;
        auto nsec2 = std::chrono::duration_cast<std::chrono::nanoseconds>(dur2).count();
        PRINT((double)nsec2/(1000000000));
        for(int j = 0; j < N; j++){
            if(f[i] != f2[i]) PRINT("NG");
        }
    }
}
