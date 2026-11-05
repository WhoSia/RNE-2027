"""Strict OSM restriction relation subset (research only; never assume missing facts legal).

Supports one from WAY, one via NODE, one to WAY; optional except;
no_* / only_*; restricted fixed weekday time condition. Unsupported relations
are returned as unresolved, not silently ignored or approved.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import re
from zoneinfo import ZoneInfo

TURNS={'left','right','straight','uturn'}
DAYS={'Mo':0,'Tu':1,'We':2,'Th':3,'Fr':4,'Sa':5,'Su':6}
MODE_MAP={'motorcar':'passenger','motor_vehicle':'passenger','hgv':'hgv','bus':'bus','psv':'bus',
          'bicycle':'bicycle','foot':'pedestrian','motorcycle':'motorcycle','emergency':'emergency'}

@dataclass(frozen=True)
class Relation:
    relation_id: str
    from_way: str
    via_node: str
    to_way: str
    restriction: str
    except_modes: frozenset[str]
    modes: frozenset[str] | None
    window: tuple[frozenset[int],int,int] | None
    source: str

@dataclass(frozen=True)
class Inspection:
    relations: tuple[Relation,...]
    unresolved: tuple[dict,...]

def _window(text):
    # Deliberately narrow subset: (Mo-Fr 07:00-09:00), no holiday/solar/weight expressions.
    m=re.fullmatch(r'\(?(Mo|Tu|We|Th|Fr|Sa|Su)(?:-(Mo|Tu|We|Th|Fr|Sa|Su))?\s+(\d\d):(\d\d)-(\d\d):(\d\d)\)?',text.strip())
    if not m:raise ValueError('conditional syntax not understood')
    lo,hi,sh,sm,eh,em=m.groups();start=int(sh)*60+int(sm);end=int(eh)*60+int(em)
    if int(sh)>23 or int(eh)>23 or int(sm)>59 or int(em)>59 or start==end:raise ValueError('invalid time interval')
    a=DAYS[lo];b=DAYS[hi] if hi else a
    days=frozenset((a+i)%7 for i in range(((b-a)%7)+1))
    return (days,start,end)

def _parse_one(x):
    rid=str(x['id']);tags=x.get('tags',{})
    if tags.get('type')!='restriction':raise ValueError('not restriction')
    members=x['members']
    def one(role,typ):
        items=[str(m['ref']) for m in members if m.get('role')==role and m.get('type')==typ]
        if len(items)!=1:raise ValueError(f'unsupported {role} members')
        return items[0]
    a=one('from','way');b=one('to','way');v=one('via','node')
    if any(m.get('role')=='via' and m.get('type')!='node' for m in members):raise ValueError('via-way not implemented')
    keys=[k for k in tags if k.startswith('restriction')]
    plain=[k for k in keys if not k.endswith(':conditional')]
    conditional=[k for k in keys if k.endswith(':conditional')]
    if len(plain)+len(conditional)!=1:raise ValueError('ambiguous/repeated restriction tags')
    key=(plain+conditional)[0];mode=None
    parts=key.split(':'); is_cond=parts[-1]=='conditional'
    if len(parts)>1 and parts[1]!='conditional':
        if parts[1] not in MODE_MAP:raise ValueError('unsupported vehicle qualifier')
        mode=frozenset([MODE_MAP[parts[1]]])
    value=tags[key];window=None
    if is_cond:
        m=re.fullmatch(r'(no|only)_(left_turn|right_turn|straight_on|u_turn)\s*@\s*(.+)',value.strip())
        if not m:raise ValueError('unsupported conditional restriction')
        restriction=f'{m.group(1)}_{m.group(2)}';window=_window(m.group(3))
    else:restriction=value
    if restriction not in {f'{p}_{t}' for p in ('no','only') for t in ('left_turn','right_turn','straight_on','u_turn')}:
        raise ValueError('unsupported restriction kind')
    raw=tags.get('except','');exc=[]
    for entry in filter(None,(v.strip() for v in raw.split(';'))):
        if entry not in MODE_MAP:raise ValueError('unknown exemption')
        exc.append(MODE_MAP[entry])
    return Relation(rid,a,v,b,restriction,frozenset(exc),mode,window,f'OSM relation:{rid}')

def ingest(relations):
    accepted=[];unresolved=[]
    for x in relations:
        try:accepted.append(_parse_one(x))
        except (ValueError,KeyError,TypeError,IndexError) as e:
            unresolved.append({'id':str(x.get('id','?')) if isinstance(x,dict) else '?','reason':str(e),
                               'status':'UNRESOLVED_NOT_AUTHORIZED'})
    return Inspection(tuple(accepted),tuple(unresolved))

def _active(win,instant,tz):
    if win is None:return True
    if instant.tzinfo is None:raise ValueError('aware timestamp required')
    local=instant.astimezone(ZoneInfo(tz));days,start,end=win
    now=local.hour*60+local.minute;day=local.weekday()
    if start<end:return day in days and start<=now<end
    return (day in days and now>=start) or (((day-1)%7) in days and now<end)

def evaluate(relations,from_way,via_node,to_way,mode,turn,instant,tz_name):
    if turn not in TURNS:raise ValueError('turn must be explicit')
    if mode not in set(MODE_MAP.values()):raise ValueError('unrecognized mode')
    if instant.tzinfo is None:raise ValueError('timezone missing')
    matched=[]
    for r in relations:
        if (r.from_way,r.via_node)!=(str(from_way),str(via_node)):continue
        if r.modes is not None and mode not in r.modes:continue
        if mode in r.except_modes or not _active(r.window,instant,tz_name):continue
        is_target=(r.to_way==str(to_way))
        action,target=r.restriction.split('_',1)
        turn_name={'left_turn':'left','right_turn':'right','straight_on':'straight','u_turn':'uturn'}[target]
        if action=='no' and is_target:
            if turn==turn_name:matched.append(r.source)
            else: return {'status':'UNKNOWN','reason':'geometry/relation turn type mismatch','evidence':[r.source]}
        if action=='only' and not is_target:matched.append(r.source)
    if matched:return {'status':'DENY','reason':'explicit OSM turn relation','evidence':sorted(set(matched))}
    return {'status':'UNKNOWN','reason':'no complete permission and regional law proof','evidence':[]}
