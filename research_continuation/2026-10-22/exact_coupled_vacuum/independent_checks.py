"""Alternative numerical paths used by the vacuum validation runner."""
import numpy as np
from scipy.linalg import expm, eigvalsh
import mode_sums as m
import vacuum as v


def matrix_exponential_potential(x,levels=5):
    R,hd,hu=x;value=0.
    for kind,mult in [('quark',6),('lepton',2),('single0',6)]:
        for b in m.blocks(kind,levels):
            B=b['D']/R
            if b['S']:B=B+hd*b['S'][0]
            if len(b['S'])>1:B=B+hu*b['S'][1]
            for a,w in zip(v.NODES,v.WEIGHTS['minus']):
                value+=mult*w/a**2*np.trace(expm(-a*(B@B)))
    return value


def finite_gradient_hessian(x,step=.0004):
    x=np.asarray(x);n=len(x);I=np.eye(n);g=np.zeros(n);H=np.zeros((n,n))
    def f(y):return v.spectral(y,order=0)[0]
    f0=f(x)
    for i in range(n):
        vals=[f(x+k*step*I[i]) for k in [-2,-1,1,2]]
        g[i]=(vals[0]-8*vals[1]+8*vals[2]-vals[3])/(12*step)
        H[i,i]=(-vals[0]+16*vals[1]-30*f0+16*vals[2]-vals[3])/(12*step**2)
        for j in range(i):
            H[i,j]=H[j,i]=sum(si*sj*f(x+step*(si*I[i]+sj*I[j])) for si in (-1,1) for sj in (-1,1))/(4*step**2)
    return g,H


def dense_oriented_quark(x,theta,levels=9):
    """Direct full-flavour angular matrix; no magnetic-block decomposition."""
    R,hd,hu=x
    species=[m.states(n,levels) for n in [2,1,1]]
    basis=[(f,*s) for f,states in enumerate(species) for s in states]
    lookup={s:i for i,s in enumerate(basis)};N=len(basis)
    B=np.zeros((N,N))
    for i,(f,tau,j2,m2) in enumerate(basis):
        n=[2,1,1][f];j=j2/2
        other=lookup.get((f,-tau,j2,m2))
        if other is not None:B[i,other]=np.sqrt(j*(j+1)-(n*n-1)/4)/R
        if f!=0:continue
        for source,amp_minus,amp_plus in [(1,hd,0.),(2,hu*np.sin(theta),hu*np.cos(theta))]:
            for st in species[source]:
                j=lookup[(source,*st)]
                val=tau*(amp_minus*m.yukawa_element((tau,j2,m2),st,-.5)+amp_plus*m.yukawa_element((tau,j2,m2),st,.5))
                B[i,j]=B[j,i]=val
    ev=eigvalsh(B,check_finite=False)
    return 6*v.profile_functions(ev,v.WEIGHTS['minus'])[0].sum()


def charged_finite_difference(x,levels=9,step=.04):
    base=dense_oriented_quark(x,0.,levels)
    estimates=[]
    for t in [step,step/2]:
        estimates.append(2*(dense_oriented_quark(x,t,levels)-base)/t**2)
    return (4*estimates[1]-estimates[0])/3


def unbroken_analytic(R,levels=50):
    ell=np.arange(1,levels+1);out=np.zeros(3)
    for n,mult in [(0,12),(1,28),(2,16)]:
        for a,w in zip(v.NODES,v.WEIGHTS['minus']):
            b=a*ell*(ell+n);terms=(2*ell+n)*np.exp(-b/R**2)
            out[0]+=w*mult*(n/2+terms.sum())/a**2
            out[1]+=w*mult*np.sum(terms*2*b/R**3)/a**2
            out[2]+=w*mult*np.sum(terms*(4*b*b/R**6-6*b/R**4))/a**2
    return out
