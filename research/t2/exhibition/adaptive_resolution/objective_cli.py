"""Compute a fresh finite laboratory decision from a given observation class."""
import argparse,json
from fractions import Fraction as F
from model import Config,Model,witness_belief
from objective import Objective,VectorDynamics
from objective_certificate import select_vector

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--q',nargs=2,type=int,default=(2,2));p.add_argument('--word',default='0001');p.add_argument('--weights',nargs=5,type=F,default=(1,1,4,0,1));p.add_argument('--budget',type=int,default=4);p.add_argument('--law',choices=['ideal','broad'],default='broad');p.add_argument('--max-depth',type=int,default=4);p.add_argument('--epsilon',type=F,default=F(0));p.add_argument('--schedule',nargs='+',type=int,default=(1,2,3,4));a=p.parse_args()
    if len(a.word)>6 or set(a.word)-{'0','1'}:p.error('binary word of length <=6')
    if not 0<=a.budget<=8:p.error('budget must be 0..8')
    c=Config(schedule=tuple(a.schedule),erasure=F(1,4) if a.law=='broad' else F(0),service='random' if a.law=='broad' else 'fixed',budget=a.budget);m=Model(c);m.validate((*a.q,a.word));b=witness_belief(tuple(a.q),a.word);result,_=select_vector(VectorDynamics(m),Objective(tuple(a.weights)),b,a.max_depth,a.epsilon)
    print(json.dumps({'model':'synthetic finite FIFO','q':a.q,'word_counts':[a.word.count('0'),a.word.count('1')],'law':a.law,'budget':a.budget,'weights':list(map(str,a.weights)),'schedule':a.schedule,'result':result},indent=2))
if __name__=='__main__':main()
