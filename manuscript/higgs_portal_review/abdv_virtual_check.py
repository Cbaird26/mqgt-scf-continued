"""Independent transcription of Aglietti/Bonciani/Degrassi/Vicini hep-ph/0611266v3.

Equations (6),(11)-(15),(27)-(30), fermion contribution only. Own HPL
power/log series, no Harlander/Kant or Note-44 coefficient imports.
Not a full NLO decay, real-emission evaluator, or observable certificate.
"""
from __future__ import annotations
import cmath
import math
from functools import lru_cache
from fractions import Fraction
import numpy as np

@lru_cache(maxsize=512)
def _coefficients(word: tuple[int,...], nmax: int):
    """Exact rational coefficients c[n,k] of x^n log(x)^k from HPL kernels."""
    if not word:
        return {(0,0):Fraction(1)}
    a,tail=word[0],word[1:]
    prev=_coefficients(tail,nmax)
    out={}
    def add(n,k,v): out[n,k]=out.get((n,k),Fraction(0))+v
    for (n,k),v in prev.items():
        if a==0:
            if n==0:
                add(0,k+1,v/Fraction(k+1))
                continue
            powers=[(n,v)]
        else:
            powers=[(m,v*((-1)**(m-n-1) if a==-1 else 1))
                    for m in range(n+1,nmax+1)]
        for m,c in powers:
            for j in range(k+1):
                add(m,k-j,c*((-1)**j)*Fraction(math.factorial(k),math.factorial(k-j)*m**(j+1)))
    return {p:v for p,v in out.items() if v}

@lru_cache(maxsize=512)
def _array(word,nmax):
    arr=np.zeros((nmax+1,len(word)+1))
    for (n,k),v in _coefficients(word,nmax).items(): arr[n,k]=float(v)
    arr.setflags(write=False)
    return arr

def hpl(word: tuple[int,...], x: complex, terms: int=48) -> complex:
    """Standard HPL kernels 1/x,1/(1-x),1/(1+x) on 0<|x|<=.1.

    This is convergent special-function evaluation, not a physical mass expansion.
    Negative-real argument uses the upper timelike boundary log(-u+i0).
    """
    word=tuple(word); z=complex(x)
    if len(word)>4 or any(type(a) is not int or a not in (-1,0,1) for a in word):
        raise ValueError('weight <=4 and letters -1,0,1 required')
    if type(terms) is not int or not 16<=terms<=128:
        raise ValueError('16<=terms<=128 required')
    if not all(math.isfinite(v) for v in (z.real,z.imag)) or not 0<abs(z)<=.1:
        raise ValueError('0<abs(x)<=.1 required')
    if not word:return 1+0j
    L=cmath.log(z)
    powers=np.array([L**k for k in range(len(word)+1)])
    co=_array(word,terms)@powers
    return complex(np.polynomial.polynomial.polyval(z,co))


def abdv_shapes(x, H, z2, z3):
    """Separately transcribed color structures; H takes a word tuple.

    Fa,Fb are (12),(13); H1=(14); CA=(28) using H2=(30).
    Does not reuse the HK rational expression or its special-function evaluator.
    """
    d=x-1
    H1=(9*z2*z2/10+2*z3*H((0,))+z2*H((0,0))+H((0,0,0,0))/4
        +7*H((0,1,0,0))/2-2*H((0,-1,0,0))
        +4*H((0,0,-1,0))-H((0,0,1,0)))
    Fa=(36*x/d**2-4*x*(1-14*x+x*x)/d**4*z3-4*x*(1+x)/d**3*H((0,))
        -8*x*(1+9*x+x*x)/d**4*H((0,0))
        +2*x*(3+25*x-7*x*x+3*x**3)/d**5*H((0,0,0))
        +4*x*(1+2*x+x*x)/d**4*(z2*H((0,))+4*H((0,-1,0))-H((0,1,0)))
        +4*x*(5-6*x+5*x*x)/d**4*H((1,0,0))
        -8*x*(1+x+x*x+x**3)/d**5*H1)
    Fb=(-12*x/d**2-6*x*(1+x)/d**3*H((0,))
        +6*x*(1+6*x+x*x)/d**4*H((0,0)))
    H2=(4*z2*z2/5+2*z3+3*z3*H((0,))/2+3*z3*H((1,))
        +z2*H((1,0))+(1+2*z2)*H((0,0))/4
        -2*H((1,0,0))+H((0,0,-1,0))+H((0,0,0,0))/4
        +2*H((1,0,-1,0))-H((1,0,0,0)))
    Ga=4*x/d**2*(3+x*(1+8*x+3*x*x)/d**3*H((0,0,0))
                   -2*(1+x)**2/d**2*H2+z3-H((1,0,0)))
    return Fa,Fb,Ga

@lru_cache(maxsize=32768)
def coefficients(r: float, scale: float=1., scheme: str='MSbar', terms: int=48) -> dict:
    """F normalized heavy-limit=1; G cross-section finite virtual numerator.

    r=m^2/Q^2. scale=mu/Q. 'OS' applies source Eq.(15) at same numerical
    mass argument, not a full physical parameter-prescription change.
    """
    if not math.isfinite(r) or not 0<r<=.08:
        raise ValueError('r in (0,.08] required')
    if not math.isfinite(scale) or scale<=0:raise ValueError('positive finite scale')
    if scheme not in ('MSbar','OS'):raise ValueError('MSbar or OS required')
    beta=math.sqrt(1-4*r); x=complex(-4*r/(1+beta)**2,0.)
    H=lambda w:hpl(w,x,terms)
    Fa,Fb,Ga=abdv_shapes(x,H,math.pi**2/6,1.2020569031595942854)
    cf=4/3; ca=3
    F0=-4*r*(2-(1-4*r)*H((0,0)))
    F=-.75*F0
    F2=Fa+Fb*(math.log(r/(scale*scale)) if scheme=='MSbar' else cf)
    G=-1.5*(cf*F2+ca*Ga)
    return {'F':F,'G':G,'Fa':Fa,'Fb':Fb,'Ga':Ga,'x':x}


def masses(Q: float,scale: float=1.,scheme: str='MSbar') -> tuple[float,float]:
    """Frozen inherited running or auxiliary pole inputs, not new fitted masses."""
    import heavy_quark_thermal as h
    if not math.isfinite(Q) or not 20<=Q<=80 or not math.isfinite(scale) or not .5<=scale<=2:
        raise ValueError('Q in [20,80] and mu/Q in [.5,2] required')
    if scheme=='MSbar':return tuple(h.running_mass(q,scale*Q) for q in ('b','c'))
    if scheme=='OS':
        return tuple(m*(1+h.alpha_s(mu)/math.pi*(4/3+math.log(mu*mu/(m*m))))
                     for m,mu in ((h.MB_AT_10,10.),(h.MC_AT_3,3.)))
    raise ValueError('scheme must be MSbar or OS')


def current(Q: float,scale: float=1.,scheme: str='MSbar',component: str='coherent') -> float:
    """Matched mass-dependent finite virtual current only, GeV^2.

    No universal production pi^2 term, integrated subtraction, real terms,
    total NLO rate or normalization certification is supplied by this function.
    """
    import heavy_quark_thermal as h
    mb,mc=masses(Q,scale,scheme)
    b=coefficients((mb/Q)**2,scale,scheme)
    c=coefficients((mc/Q)**2,scale,scheme)
    vb=(b['G']*b['F'].conjugate()).real
    vc=(c['G']*c['F'].conjugate()).real
    vi=(b['G']*c['F'].conjugate()+c['G']*b['F'].conjugate()).real
    vals={'bb':vb,'cc':vc,'bc':vi,'coherent':vb+vc+vi}
    if component not in vals:raise ValueError('unknown component')
    return Q*Q/9*(h.alpha_s(scale*Q)/math.pi)**3*vals[component]


def thermal(T:float,pair:str,scale:float=1.,scheme:str='MSbar',component:str='coherent',method:str='w'):
    """Finite-window MB virtual contribution using unchanged inherited kernel."""
    import heavy_quark_thermal as h
    return h.thermal_from_weight(T,pair,lambda Q:current(Q,scale,scheme,component),h.W_CUT,method)


def complete_physical_rate(*args,**kwargs):
    raise NotImplementedError('virtual cross-check only: real-emission normalization and full decay remain separate')
