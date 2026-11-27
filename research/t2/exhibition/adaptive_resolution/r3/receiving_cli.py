"""Fresh, offline exact finite-model calculation; not a live controller."""
import argparse,json
from fractions import Fraction as F
from receiving_channel import *

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--q',nargs=2,type=int,default=[2,2]);p.add_argument('--word',default='0001');p.add_argument('--budget',type=int,default=2)
    p.add_argument('--error',type=F,default=F(0));p.add_argument('--target',choices=('upstream','peak','system'),default='upstream')
    p.add_argument('--infinite-receiving',action='store_true');a=p.parse_args()
    if any(x not in range(3) for x in a.q) or len(a.word)>4 or set(a.word)-{'0','1'} or not 0<=a.budget<=4 or not 0<=a.error<=F(1,2):p.error('q 0..2, binary word length<=4, budget 0..4, error 0..1/2')
    if a.infinite_receiving and a.error:p.error('no noisy infinite comparison implemented')
    m=Model(False) if a.infinite_receiving else ChannelModel(a.error);b=initial(tuple(a.q),a.word)
    cls=SystemPlanner if a.target=='system' else Planner;peak=4 if a.target=='peak' else 0
    r={n:cls(m,peak,modes=ms).report(b,a.budget) for n,ms in [('free',(0,)),('word',(0,1,2)),('receiving',(0,3)),('joint',(0,1,2,3))]}
    best=min(({'calendar':c,'report':cls(m,peak,calendar=c).report(b,a.budget)} for c in calendars(3,a.budget)),key=lambda x:(F(x['report']['cost']),x['calendar']))
    assert F(best['report']['cost'])>=F(r['joint']['cost'])
    print(json.dumps({'model':'synthetic laboratory only','target':a.target,'q':a.q,'word':a.word,'budget':a.budget,'error':str(a.error),'finite':not a.infinite_receiving,'vector_names':['upstream_S','upstream_L','stage_max','whole_system_stock','exits','credits','acquisitions'],'policies':r,'best_calendar':best,'calendar_gain':str(F(best['report']['cost'])-F(r['joint']['cost']))},indent=2))
if __name__=='__main__':main()
