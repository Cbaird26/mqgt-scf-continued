"""Note 48: common-decay candidate assembly and mixed-sector consistency audit.

All quantities are source-conditional.  The inherited Note-47 subtraction
normalization is a reconstruction, not an author-confirmed erratum.
This module must pass cross-sector checks before a completed rate is claimed.
"""
from __future__ import annotations
import math
from functools import lru_cache
import numpy as np
from scipy.special import roots_legendre
import heavy_quark_thermal as h
import gluon_loop_thermal as g
import bc_virtual_finite as v
import coherent_bc_rg as rg
import three_gluon_remainder as r3

LABELS = ('tt','bb','cc','tb','tc','bc')


def products(a):
    a=np.asarray(a)
    return np.stack([abs(a[0])**2, abs(a[1])**2, abs(a[2])**2,
                     2*(a[0]*a[1].conjugate()).real,
                     2*(a[0]*a[2].conjugate()).real,
                     2*(a[1]*a[2].conjugate()).real])


def masses(Q,scale=1.,scheme='MSbar'):
    return r3._hard(Q,scale,scheme)


def born_virtual(Q,scale=1.,scheme='MSbar'):
    ms=masses(Q,scale,scheme)
    fs=[1.+0j]; gs=[5.5+0j]
    for q in ('b','c'):
        r=(ms[q]/Q)**2
        f,df=rg.form_and_mass_derivative(r)
        G=v.hk_product(r)
        G+=2*df*math.log(scale*scale/r) if scheme=='MSbar' else -(8/3)*df
        fs.append(f);gs.append(G)
    F,G=np.array(fs),np.array(gs)
    virtual=np.array([(G[j]*F[j].conjugate()).real for j in range(3)]+[
       (G[i]*F[j].conjugate()+G[j]*F[i].conjugate()).real
       for i,j in ((0,1),(0,2),(1,2))])
    return products(F),virtual


def universal(Q,scale=1.,scheme='MSbar'):
    """Proposed gluonic-cut spectator matching, real heavy pairs excluded."""
    ms=masses(Q,scale,scheme)
    logs=sum(math.log(Q*Q/m**2) for m in ms.values())
    return 73/4-7*3/6-logs/3+(23/6)*2*math.log(scale)


def fg(t):
    t=np.asarray(t,float)
    f=np.empty(t.shape,complex);aux=np.empty_like(f)
    below=t<=1
    angle=np.arcsin(np.sqrt(t[below]))
    f[below]=angle**2
    aux[below]=np.sqrt((1-t[below])/t[below])*angle
    beta=np.sqrt(1-1/t[~below]);Z=np.log(t[~below])+2*np.log1p(beta)-1j*math.pi
    f[~below]=-.25*Z**2;aux[~below]=.5*beta*Z
    return f,aux


def offshell(t,z):
    """Published timelike triangle, with Note45-real quadratic endpoint."""
    if not math.isfinite(t) or t<=1: raise ValueError('requires timelike loop tau>1')
    z=np.asarray(z,float)
    if np.any(~np.isfinite(z)|(z<=0)|(z>=1)):raise ValueError('0<z<1 required')
    f,aux=[a.item() for a in fg(np.array(t))]
    fz,gz=fg(z*t);d=z-1
    out=-1.5/(t*d)*(1-2*z*(gz-aux)/d-(1+1/(t*d))*(fz-f))
    near=z>1-1e-3
    if np.any(near):
        b=math.sqrt(1-1/t);Z=complex(math.log(t)+2*math.log1p(b),-math.pi)
        fp=-Z/(2*t*b)
        fpp=-1/(2*t*t*b*b)+Z/(2*t*t*b)+Z/(4*t**3*b**3)
        fppp=1.5/(t**3*b*b)+.75/(t**4*b**4)-Z/(t**3*b)-Z/(t**4*b**3)-.375*Z/(t**5*b**5)
        edge=3/(4*t)*(1+(2*t-1)*fp)
        slope=-(1-fp)/(4*t)+(3*t-1)*fpp/4
        quad=(1-fp)/(8*t)+fpp/8+(4*t*t-t)*fppp/16
        out[near]=edge+d[near]*slope+d[near]**2*quad
    return out


@lru_cache(maxsize=128)
def pair_remainder(Q,scale=1.,scheme='MSbar',n=128):
    ms=masses(Q,scale,scheme); ts=[(Q/(2*ms[q]))**2 for q in ('b','c')]
    if type(n)is not int or not 16<=n<=256:raise ValueError('invalid node count')
    uu,ww=roots_legendre(n);uu=(uu+1)/2;ww=ww/2
    edges=sorted((0.,1/ts[0],1/ts[1],1.)); acc=np.zeros(6)
    F0=np.array([1,g.form_factor(ts[0]),g.form_factor(ts[1])]);B=products(F0)
    for lo,hi in zip(edges[:-1],edges[1:]):
        theta=math.pi*uu/2;z=lo+(hi-lo)*np.sin(theta)**2
        jac=(hi-lo)*math.pi*np.sin(theta)*np.cos(theta)
        A=np.stack([np.ones_like(z),offshell(ts[0],z),offshell(ts[1],z)])
        diff=products(A)-B[:,None]
        acc+=np.sum(ww*jac*(1-z)**3/z*diff,axis=1)
    # n_light/3 = 1: these six dimensionless terms directly enter the bracket.
    return acc


def shape(Q,x,y,scale=1.,scheme='MSbar'):
    ms=masses(Q,scale,scheme);x,y=np.broadcast_arrays(x,y);z=1-x-y
    ct=np.stack([x*x,-y*y,z*z,np.ones_like(x)])
    cb=r3.helicities((Q/ms['b'])**2,x,y)
    cc=r3.helicities((Q/ms['c'])**2,x,y)
    A3=np.sum(products(np.stack([ct,cb,cc])),axis=1)
    F=np.array([1,g.form_factor((Q/(2*ms['b']))**2),g.form_factor((Q/(2*ms['c']))**2)])
    B=products(F).reshape((6,)+(1,)*np.ndim(x))
    P=1+x**4+y**4+z**4
    return (A3-P*B)/(2*x*y*z)


@lru_cache(maxsize=128)
def three_remainder(Q,scale=1.,scheme='MSbar',n=32):
    ms=masses(Q,scale,scheme);u,w=r3.nodes(n)
    thresholds=sorted(4*(m/Q)**2 for m in ms.values())
    cuts=sorted({0.,1/3,*[a for a in thresholds if 0<a<1/3]})
    acc=np.zeros(6)
    for lo,hi in zip(cuts[:-1],cuts[1:]):
        for x,wx in zip(lo+(hi-lo)*u,(hi-lo)*w):
            yl,yh=x,(1-x)/2
            yc=sorted({yl,yh,*[a for a in thresholds if yl<a<yh],
                       *[1-x-a for a in thresholds if yl<1-x-a<yh]})
            for a,b in zip(yc[:-1],yc[1:]):
                th=math.pi*u/2;y=a+(b-a)*np.sin(th)**2
                wy=(b-a)*math.pi/2*np.sin(2*th)*w
                acc+=6*wx*np.sum(shape(Q,x,y,scale,scheme)*wy,axis=1)
    return acc


def hard_terms(Q,scale=1.,scheme='MSbar',n=32):
    B,V=born_virtual(Q,scale,scheme)
    U=universal(Q,scale,scheme)*B
    J3=three_remainder(Q,scale,scheme,n)
    Jp=pair_remainder(Q,scale,scheme)
    pref=(h.alpha_s(scale*Q)/math.pi)**3*Q*Q/9
    return {k: pref*a for k,a in dict(virtual=V,universal=U,three_gluon=J3,
                                    light_pair=Jp,increment=V+U+J3+Jp).items()}



def finite_shift(Q,scale=1.,scheme='MSbar'):
    """Candidate finite-mass shift Delta G=(8/3) D F, not new radiation.

    A cross-sector diagnostic; this is NOT silently applied to old code.
    Its interpretation requires the common convention discussed in Note48.
    """
    ms=masses(Q,scale,scheme);F=[1.+0j];D=[0j]
    for q in ('b','c'):
        f,df=rg.form_and_mass_derivative((ms[q]/Q)**2)
        F.append(f);D.append((8/3)*df)
    F,D=np.array(F),np.array(D)
    shift=np.array([(D[j]*F[j].conjugate()).real for j in range(3)]+[
        (D[i]*F[j].conjugate()+D[j]*F[i].conjugate()).real
        for i,j in ((0,1),(0,2),(1,2))])
    return (h.alpha_s(scale*Q)/math.pi)**3*Q*Q/9*shift

PARTS=('LO','virtual_literal','universal','three_gluon','light_pair',
       'finite_shift','literal_increment','matched_increment','matched_NLO')


def candidate_terms(Q,scale=1.,scheme='MSbar',n=32):
    """Return two explicitly distinguished convention assemblies.

    'matched' adds the finite (8/3)*DF shift fixed by one-loop mass
    conversion and tested against the independently written Note44 mixed
    coefficient. It is NOT an author-confirmed correction to either paper.
    A completed physical rate, source-erratum or abundance is not inferred.
    """
    terms=hard_terms(Q,scale,scheme,n)
    B,_=born_virtual(Q,scale,scheme)
    lo=(h.alpha_s(scale*Q)/math.pi)**2*Q*Q/9*B
    shift=finite_shift(Q,scale,scheme)
    inc=terms['increment']+shift
    return dict(LO=lo,virtual_literal=terms['virtual'],universal=terms['universal'],
                three_gluon=terms['three_gluon'],light_pair=terms['light_pair'],
                finite_shift=shift,literal_increment=terms['increment'],
                matched_increment=inc,matched_NLO=lo+inc)


def thermal_candidate(T=.5,pair='11',scale=1.,scheme='MSbar',angular_n=24,
                      thermal_n=24,method='laguerre'):
    """Finite-window thermal entries; rows PARTS, columns LABELS.

    Common MB momentum distributions are assumed. This function does NOT
    impose chemical equilibrium or certify an assembled physical NLO rate.
    Both quadratures integrate the window w in [0,90], without claiming
    control of the unknown spectrum above Q=80 GeV.
    """
    from scipy.special import roots_genlaguerre,kve,kv
    mi,mj,k=h._pair_setup(T,pair,h.W_CUT)
    masses(mi+mj,scale,scheme);r3.nodes(angular_n)
    if type(thermal_n) is not int or not 8<=thermal_n<=128:
        raise ValueError('thermal node count in [8,128] required')
    xi,xj=mi/T,mj/T;a=xi+xj;b=xi-xj
    acc=np.zeros((len(PARTS),len(LABELS)))
    if method=='laguerre':
        ns,ws=roots_genlaguerre(thermal_n,.5)
        pref=k*k/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj))
        for w,weight in zip(ns,ws):
            if w>h.W_CUT:continue
            y=a+w;Q=T*y
            f=y*y*math.sqrt((2*a+w)*(y*y-b*b))*kve(1,y)/((Q*Q-h.MH*h.MH)**2+(h.MH*h.GH)**2)
            terms=candidate_terms(float(Q),scale,scheme,angular_n)
            acc+=weight*f*np.stack([terms[p] for p in PARTS])
        return pref*acc
    if method=='Q':
        us,ws=roots_legendre(thermal_n)
        ts=(us+1)*math.sqrt(h.W_CUT)/2;ws=ws*math.sqrt(h.W_CUT)/2
        norm=8*mi*mi*mj*mj*T*kv(2,xi)*kv(2,xj)
        for t,weight in zip(ts,ws):
            Q=mi+mj+T*t*t;s=Q*Q
            lam=(s-(mi+mj)**2)*(s-(mi-mj)**2)
            f=(2*T*t)*k*k*s*math.sqrt(lam)*kv(1,Q/T)/(4*math.pi*((s-h.MH*h.MH)**2+(h.MH*h.GH)**2))
            terms=candidate_terms(float(Q),scale,scheme,angular_n)
            acc+=weight*f*np.stack([terms[p] for p in PARTS])
        return acc/norm
    raise ValueError('method must be laguerre or Q')


def complete_physical_rate(*args,**kwargs):
    raise NotImplementedError('finite convention mismatch: independent source matching unresolved')


def diagnostic(Q=20.,scale=1.,scheme='MSbar',n=32):
    """Compare to Note44's different closed mixed hard expression.

    Inputs and running are shared; virtual/real representations are not.
    """
    import mixed_gluon_nlo as m
    terms=candidate_terms(Q,scale,scheme,n)
    out={}
    for flavor,j in [('b',3),('c',4)]:
        reference=m.current_components(Q,flavor,scale,scheme)['delta_NLO']
        literal=terms['literal_increment'][j]
        matched=terms['matched_increment'][j]
        out[flavor]={'literal_increment_GeV2':float(literal),
          'finite_shift_GeV2':float(terms['finite_shift'][j]),
          'matched_increment_GeV2':float(matched),'reference_increment_GeV2':float(reference),
          'literal_minus_reference_GeV2':float(literal-reference),
          'matched_minus_reference_GeV2':float(matched-reference)}
    return {'Q_GeV':Q,'scale':scale,'scheme':scheme,'angular_nodes':n,'flavors':out,
      'source_erratum_confirmed':False,'complete_physical_NLO_claimed':False}


if __name__=='__main__':
    import json
    print(json.dumps(diagnostic(),indent=2))
