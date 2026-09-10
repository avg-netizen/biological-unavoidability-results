"""Independent graph/path controls for the classification proof in 44j.

Finite barriers are measurements, not the infinite proof. Periodic positive
controls test that the construction does not accidentally prohibit all targets.
"""
from itertools import product
from math import isqrt
from pathlib import Path
import json


def r(s,v):
    return s(v//2) ^ (v%2)


def outgoing(s,u):
    # Direct transcription from the two incoming edges in the proof.
    for v in [u+1,u+2]:
        if v>=2:
            yield v,r(s,v) ^ (v-u-1)


def barrier_interval(s,start,limit):
    lo=hi=start
    for k in range(limit):
        a=s(k)
        lo=lo+1+(r(s,lo+1)!=a)
        hi=hi+1+(r(s,hi+2)!=a)
        if lo>hi:return k+1
    return None


def main():
    targets={
        'Thue_Morse':lambda k:k.bit_count()%2,
        'powers_of_two_indicator':lambda k:int(k>0 and k&(k-1)==0),
        'mechanical_sqrt2_minus1':lambda k:isqrt(2*(k+1)**2)-isqrt(2*k*k)-1,
    }
    axiom_checks=0
    for s in targets.values():
        for v in range(2,1024):
            incoming=[(u,a) for u in [v-2,v-1] for w,a in outgoing(s,u) if w==v]
            assert len(incoming)==2 and {a for u,a in incoming}=={0,1}
            assert all(u<v for u,a in incoming)
            axiom_checks+=1
        assert list(outgoing(s,0))==[(2,1-r(s,2))]
        assert all(len(list(outgoing(s,u)))==2 for u in range(1,1024))
    # Direct set-of-vertices DP versus the separately implemented interval update.
    transition_checks=0
    for s in targets.values():
        for start in range(64):
            states={start};lo=hi=start
            for k in range(512):
                new=set()
                for u in states:
                    for v,a in outgoing(s,u):
                        if a==s(k):
                            assert v>=2*(k+1)
                            assert 0<=v-2*(k+1)<=u-2*k<=start
                            new.add(v)
                            transition_checks+=1
                lo=lo+1+(r(s,lo+1)!=s(k))
                hi=hi+1+(r(s,hi+2)!=s(k))
                assert new==set(range(lo,hi+1))
                states=new
                if not states:break
    barriers={name:[barrier_interval(s,i,16384) for i in range(256)] for name,s in targets.items()}
    assert all(x is not None for x in barriers['Thue_Morse'])
    # Pure periodic controls have an explicit step-two path from vertex 2p-1.
    periodic_controls=0
    for p in range(1,7):
        for word in product([0,1],repeat=p):
            s=lambda k,w=word:w[k%len(w)]
            for k in range(128):
                u=2*k+2*p-1
                assert (u+2,s(k)) in list(outgoing(s,u))
            periodic_controls+=1
    # Eventually periodic controls: lift the periodic tail, then restore prefix
    # by the unique incoming parent of each prescribed label.
    prefixed_controls=0
    for prefix in product([0,1],repeat=3):
        for period in product([0,1],repeat=3):
            s=lambda k,p=prefix,w=period:p[k] if k<len(p) else w[(k-len(p))%len(w)]
            anchor=2*len(prefix)+2*len(period)-1
            rev=[anchor]
            for a in reversed(prefix):
                v=rev[-1]
                rev.append(v-1 if r(s,v)==a else v-2)
            path=list(reversed(rev))+[anchor+2*j for j in range(1,129)]
            for k,(u,v) in enumerate(zip(path,path[1:])):
                assert (v,s(k)) in list(outgoing(s,u))
            prefixed_controls+=1
    # A three-letter lift: project 2 to1 and 0,1 to0.
    pi=lambda a:int(a==2)
    s=targets['Thue_Morse']
    lifted_incoming=0
    for v in range(2,128):
        for b in range(3):
            incoming=[((u,a),a) for u in [v-2,v-1] for w,c in outgoing(s,u)
                      if w==v for a in range(3) if pi(a)==c]
            assert len(incoming)==3 and {a for u,a in incoming}=={0,1,2}
            lifted_incoming+=1
    result={'status':'PASS','binary_nonroot_axiom_checks':axiom_checks,
            'matching_transitions_checked':transition_checks,
            'pure_periodic_positive_controls':periodic_controls,
            'prefixed_periodic_positive_controls':prefixed_controls,
            'three_letter_lift_vertices':lifted_incoming,
            'barriers_by_start':barriers,
            'barrier_summary':{name:{'starts':len(bs),'terminated':sum(x is not None for x in bs),
                'maximum_observed':max(x for x in bs if x is not None)} for name,bs in barriers.items()},
            'scope':'Finite controls; all-start avoidance is proved in44j and binary core formalized in44l.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='barriers_by_start'},indent=2))


if __name__=='__main__':main()
