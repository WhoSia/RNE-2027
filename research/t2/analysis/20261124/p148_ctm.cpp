// P148: integer two-cell model, not calibrated CTM or SUMO.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <string>
struct State { int e,u,d,z; };
struct Flow { State next; int in,move,out; };
Flow step(State s,int U,int D,int a,int sink,int green) {
    int in=std::min({s.e+a,U-s.u,2});
    int move=green*std::min({s.u,D-s.d,2});
    int out=std::min({s.d,sink,2});
    State n{s.e+a-in,s.u+in-move,s.d+move-out,s.z+out};
    assert(n.e>=0 && n.u>=0 && n.u<=U && n.d>=0 && n.d<=D);
    assert(n.e+n.u+n.d+n.z==s.e+s.u+s.d+s.z+a);
    assert(move>=0 && out>=0 && out<=sink && out<=s.d);
    assert((green && s.d!=D) || move==0);
    return {n,in,move,out};
}
void hash_row(std::uint64_t& h,const std::string& row) {
    for(unsigned char ch:row) { h^=ch; h*=UINT64_C(1099511628211); }
}
int main() {
    std::uint64_t h=UINT64_C(14695981039346656037), count=0;
    for(int U=1;U<=6;++U) for(int D=1;D<=6;++D)
    for(int e=0;e<=3;++e) for(int u=0;u<=U;++u) for(int d=0;d<=D;++d)
    for(int a=0;a<=2;++a) for(int sink=0;sink<=2;++sink) for(int g=0;g<=1;++g) {
        auto f=step({e,u,d,0},U,D,a,sink,g); auto n=f.next;
        std::ostringstream row;
        row<<U<<','<<D<<','<<e<<','<<u<<','<<d<<','<<a<<','<<sink<<','<<g<<','
           <<n.e<<','<<n.u<<','<<n.d<<','<<n.z<<','<<f.in<<','<<f.move<<','<<f.out<<'\n';
        hash_row(h,row.str()); ++count;
    }
    std::cout<<"invariants,"<<count<<','<<h<<'\n';
    for(int D=1;D<=6;++D) for(int p:{4,8}) for(int phi=0;phi<p;++phi) {
        State s{0,0,0,0}; int cost=0,denied=0;
        for(int t=0;t<200;++t) {
            int g=(t+phi)%p<p/2;
            denied+=g && s.u>0 && s.d==D;
            s=step(s,6,D,t<24,t%8<4?2:0,g).next;
            cost+=s.e+s.u+s.d;
        }
        assert(s.z==24 && s.e+s.u+s.d==0);
        std::cout<<"run,"<<D<<','<<p<<','<<phi<<','<<cost<<','<<denied<<','<<s.z<<'\n';
    }
}
