from ext_h08f import *
# nominal base replay at (2,2), L4
C=Ctx((2,2),4)
for p in ('free','head_if','full_if','adaptive'):
    v=summarize(C.evaluate(p)); print(p,float(obj(v)),v[0],v[1],v[2],v[3])
v=summarize(C.evaluate('head_if')); print('head_if exact',obj(v)); 
assert abs(float(obj(summarize(C.evaluate('head_if'))))-10.813956093)<1e-8
assert abs(float(obj(summarize(C.evaluate('full_if'))))-10.840053763)<1e-8
assert abs(float(obj(summarize(C.evaluate('adaptive'))))-10.799283154)<1e-8
print('NOMINAL REPLAY PASS')
