"""Independent H08F implementation (external review). Exact Fractions, belief DP, policy evaluation by recursion on
exact posterior beliefs (valid because the nominal law equals the true law here)."""
import sys, json, time
from fractions import Fraction as Q
from functools import lru_cache
from collections import Counter, defaultdict
from itertools import product
from math import gcd
A=(0,1); BUDGET=2
def words(n): return [w for k in range(n+1) for w in product(A,repeat=k)]
def norm(c):
    g=0
    for v in c.values(): g=gcd(g,v)
    return tuple(sorted((x,v//g) for x,v in c.items()))
def mass(b): return sum(v for _,v in b)
def obs(x,m):
    s,l,w=x
    return (s,l,w.count(0),w.count(1)) if m==0 else (w[:1] if m==1 else w)
def split(b,m):
    d=defaultdict(Counter)
    for x,n in b: d[obs(x,m)][x]+=n
    return {k:(sum(c.values()),norm(c)) for k,c in d.items()}
def add(v,u,w): return tuple(a+w*b for a,b in zip(v,u))
def obj(v): return v[0]+v[1]

class Ctx:
    def __init__(s,caps,L,c=Q(1,16),h=4):
        s.caps,s.L,s.c,s.h=caps,L,Q(c),h
        s.price=(Q(0),s.c/4,s.c)
        s.support=[(a,b,w) for a in range(caps[0]+1) for b in range(caps[1]+1) for w in words(L)]
        @lru_cache(None)
        def step(x,a):
            q=[x[0],x[1]]; w=list(x[2])
            for _ in range(BUDGET):
                if q[a]: q[a]-=1
            for _ in range(BUDGET):
                if not w or q[w[0]]==caps[w[0]]: break
                q[w.pop(0)]+=1
            return sum(q)+len(w), tuple((q[0],q[1],tuple(w+[i])) for i in A)
        s.step=step
        @lru_cache(None)
        def fq(x,h,a):
            r,ch=step(x,a)
            return Q(r) if h==1 else Q(r)+sum(Q(1,2)*min(fq(y,h-1,i) for i in A) for y in ch)
        s.fq=fq
    def evaluate(s,policy):
        """policy in free head_always full_always head_if full_if adaptive adaptive_full adaptive_eq qmdp"""
        step,price,fq=s.step,s.price,s.fq
        def modes(b,h):
            if policy=='free': return (0,)
            if policy=='head_if': return (1 if len(split(b,1))>1 else 0,)
            if policy=='full_if': return (2 if len(split(b,2))>1 else 0,)
            if policy=='adaptive': return (0,1,2)
            q0,q1=b[0][0][0],b[0][0][1]
            if policy=='adaptive_full':
                return (0,1,2) if (q0==s.caps[0] and q1==s.caps[1]) else (0,)
            if policy=='adaptive_eq':
                return (0,1,2) if Q(q0,s.caps[0])==Q(q1,s.caps[1]) else (0,)
            if policy=='qmdp':
                n=mass(b); vals=[]
                for m in range(3):
                    parts=[(n,b)] if m==0 else list(split(b,m).values())
                    t=price[m]
                    for nn,bb in parts:
                        t+=Q(nn,n)*min(sum(Q(k,mass(bb))*fq(x,h,a) for x,k in bb) for a in A)
                    vals.append(t)
                return (min(range(3),key=lambda m:(vals[m],m)),)
        @lru_cache(None)
        def sense(b,h):
            best=None
            for m in modes(b,h):
                v=(Q(0),price[m],Q(m==1),Q(m==2)); n=mass(b)
                parts=[(n,b)] if m==0 else list(split(b,m).values())
                for nn,bb in parts: v=add(v,control(bb,h),Q(nn,n))
                if best is None or obj(v)<obj(best[1]): best=(m,v)
            return best
        @lru_cache(None)
        def control(b,h):
            n=mass(b); cands=[]
            for a in A:
                nxt=Counter(); imm=0
                for x,m in b:
                    r,ch=step(x,a); imm+=m*r
                    for y in ch: nxt[y]+=m
                cands.append((a,imm,nxt))
            if policy=='qmdp':
                a=min(A,key=lambda a:(sum(Q(k,n)*fq(x,h,a) for x,k in b),a))
                cands=[cands[a]]
            best=None
            for a,imm,nxt in cands:
                v=(Q(imm,n),Q(0),Q(0),Q(0))
                if h>1:
                    for nn,bb in split(tuple(nxt.items()),0).values(): v=add(v,sense(bb,h-1)[1],Q(nn,2*n))
                if best is None or obj(v)<obj(best): best=v
            return best
        out={}
        b0=tuple((x,1) for x in s.support)
        for k,(n,bb) in split(b0,0).items(): out[k]=(n,sense(bb,s.h)[1])
        return out

def summarize(cv):
    N=sum(n for n,_ in cv.values()); v=(Q(0),)*4
    for n,x in cv.values(): v=add(v,x,Q(n,N))
    return v
