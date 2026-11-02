from dataclasses import dataclass
@dataclass(frozen=True)
class Scenario:
    main:int
    side:int
    @property
    def total(self):return self.main+self.side

def observation(s):
    return (s.total,min(s.total,12))

def outcome(s,g):
    if not 0<=g<=12:raise ValueError("green split")
    completed=min(s.main,g)+min(s.side,12-g)
    return completed,s.total-completed

def optima(s):
    best=max(outcome(s,g)[0] for g in range(13))
    return [g for g in range(13) if outcome(s,g)[0]==best]

def witness():
    a,b=Scenario(10,2),Scenario(2,10)
    assert observation(a)==observation(b)
    assert set(optima(a)).isdisjoint(optima(b))
    return {"observed":observation(a),"policy_A":optima(a),"policy_B":optima(b)}

if __name__=="__main__":
    print(witness())
