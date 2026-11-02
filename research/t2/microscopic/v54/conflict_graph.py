"""T2 v5.4: abstract movement-conflict event audit, not surveyed intersection safety."""
from itertools import combinations
MOVES=('main_through','main_exit','main_outflow','side_merge','side_exit')
CONFLICTS=frozenset(frozenset(p) for p in combinations(MOVES,2))
STAGES={'main':('main_through','main_exit','main_outflow'),'turn':('main_exit',),'side':('side_merge','side_exit'),'all_red':()}
def compatible(movements):
    m=set(movements)
    return len(m)==len(movements) and m<=set(MOVES) and all(not e<=m for e in CONFLICTS)
def audit_crossings(rows,dt=.5):
    if dt<=0:raise ValueError('dt')
    groups={}
    for row in rows:
        j=int(row['junction']);movement=row['movement'];phase=row['phase']
        if j not in range(3) or movement not in MOVES:raise ValueError('unknown movement or junction')
        if movement not in STAGES.get(phase,()):raise AssertionError('movement disallowed in phase')
        tick=round(row['t_s']/dt)
        groups.setdefault((j,tick),[]).append(movement)
    for key,m in groups.items():
        if not compatible(m):raise AssertionError(f'conflicting crossing at {key}')
    return {'crossings':len(rows),'junction_ticks':len(groups),'conflicting_ticks':0}
