"""High-precision HPL evaluation for Note 49.

Uses polylog identities and a defining one-dimensional HPL integral rather
than the production power/log recurrence. Shares only the new ABDV rational
color decomposition, not the old HK expression. This is a numerical check.
"""
from functools import lru_cache
import mpmath as mp
from abdv_virtual_check import abdv_shapes

@lru_cache(maxsize=64)
def hpl_reference_values(x_real: float, dps: int=65):
    with mp.workdps(dps):
        x=mp.mpc(str(x_real),0); l=mp.log(x); lm=mp.log(1-x)
        p2,p3,p4=[mp.polylog(n,x) for n in (2,3,4)]
        n2,n3,n4=[mp.polylog(n,-x) for n in (2,3,4)]
        def f(u):
            if not u:return mp.mpc(0)
            t=x*u
            return x/(1-t)*(-mp.log(t)*mp.polylog(2,-t)+2*mp.polylog(3,-t))
        return {(0,):l,(1,):-lm,(0,0):l*l/2,(0,0,0):l**3/6,(0,0,0,0):l**4/24,
         (1,0):-l*lm-p2,(0,1,0):l*p2-2*p3,(0,-1,0):-l*n2+2*n3,
         (1,0,0):-l*l*lm/2-l*p2+p3,
         (0,1,0,0):l*l*p2/2-2*l*p3+3*p4,
         (0,-1,0,0):-l*l*n2/2+2*l*n3-3*n4,
         (0,0,-1,0):-l*n3+3*n4,(0,0,1,0):l*p3-3*p4,
         (1,0,0,0):-l**3*lm/6-l*l*p2/2+l*p3-p4,
         (1,0,-1,0):mp.quad(f,[0,mp.mpf('.25'),1])}

def reference_coefficients(r: float,scale: float=1.,scheme: str='MSbar',dps: int=65):
    if not 0<r<=.08 or scale<=0 or scheme not in ('MSbar','OS'):raise ValueError('invalid domain')
    with mp.workdps(dps):
        rr=mp.mpf(str(r));sc=mp.mpf(str(scale))
        x=-4*rr/(1+mp.sqrt(1-4*rr))**2
        # Get reference HPLs at the same exact float argument as production for
        # individual-HPL comparisons. Full coefficient uses high-precision x.
        def HH(w):
            z=mp.mpc(x,0);l=mp.log(z);lm=mp.log(1-z)
            if all(a==0 for a in w):return l**len(w)/mp.factorial(len(w))
            p2,p3,p4=[mp.polylog(n,z) for n in (2,3,4)]
            n2,n3,n4=[mp.polylog(n,-z) for n in (2,3,4)]
            vals={(1,):-lm,(1,0):-l*lm-p2,(0,1,0):l*p2-2*p3,
            (0,-1,0):-l*n2+2*n3,(1,0,0):-l*l*lm/2-l*p2+p3,
            (0,1,0,0):l*l*p2/2-2*l*p3+3*p4,
            (0,-1,0,0):-l*l*n2/2+2*l*n3-3*n4,
            (0,0,-1,0):-l*n3+3*n4,(0,0,1,0):l*p3-3*p4,
            (1,0,0,0):-l**3*lm/6-l*l*p2/2+l*p3-p4}
            if w in vals:return vals[w]
            if w==(1,0,-1,0):
                def fun(u):
                    if not u:return mp.mpc(0)
                    t=z*u
                    return z/(1-t)*(-mp.log(t)*mp.polylog(2,-t)+2*mp.polylog(3,-t))
                return mp.quad(fun,[0,mp.mpf('.25'),1])
            raise ValueError('HPL not requested by ABDV')
        # One HPL value per word, cached at this precise argument.
        table={}
        def H(w):
            if w not in table:table[w]=HH(w)
            return table[w]
        Fa,Fb,Ga=abdv_shapes(mp.mpc(x,0),H,mp.zeta(2),mp.zeta(3))
        F0=-4*rr*(2-(1-4*rr)*H((0,0)))
        cf=mp.mpf(4)/3
        F2=Fa+Fb*(mp.log(rr/sc**2) if scheme=='MSbar' else cf)
        return {'F':complex(-mp.mpf(3)/4*F0),'G':complex(-mp.mpf(3)/2*(cf*F2+3*Ga))}
