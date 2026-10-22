"""Exact-internal-spectrum, low-external-momentum spectral-action kernels.

All matrices act on the complete monopole spinor multiplets through radial
level L. No local expansion in 1/R is used. Coefficients are numerical
approximations to the convergent infinite sums, not interval certificates.
See main.tex for the derivation, field units, and cutoff qualifications.
"""
from functools import lru_cache
from math import pi, sqrt
import numpy as np
from scipy.linalg import eigh, eig, eigvals, expm


def states(n, levels):
    out = []
    for tau in (1, -1):
        s2 = n-tau
        for j2 in range(abs(s2), 2*levels+n, 2):
            for m2 in range(-j2, j2+1, 2):
                out.append((tau, j2, m2))
    return out


def cg_half(j, m, u, J):
    """C(j,m;1/2,u|J,m+u), Condon--Shortley convention."""
    if abs(J-j-0.5) < 1e-9:
        return sqrt(max(0., (j+2*u*m+1)/(2*j+1)))
    if abs(J-j+0.5) < 1e-9:
        return -2*u*sqrt(max(0., (j-2*u*m)/(2*j+1)))
    return 0.


def yukawa_element(target, source, scalar_m):
    """Integral of Y_target* Y_(1/2,scalar_m) Y_source, spin weight +1/2."""
    tau, jt2, mt2 = target
    ts, js2, ms2 = source
    if tau != ts or mt2 != ms2+round(2*scalar_m):
        return 0.
    J, j, m = jt2/2, js2/2, ms2/2
    source_s = (1-tau)/2
    return (sqrt(2*(2*j+1)/(4*pi*(2*J+1)))
            * cg_half(j, m, scalar_m, J)
            * cg_half(j, -source_s, -0.5, J))


@lru_cache(maxsize=None)
def blocks(kind="pair", levels=8):
    """Fixed conserved magnetic-label blocks.

    pair: n2,n1 with scalar m=-1/2; quark: n2,n1,n1 with
    down m=-1/2, conjugate-up m=+1/2. parallel is a potential
    control with both scalar harmonics m=-1/2, not an aligned EW vacuum.
    single0/1/2 are the unbroken sectors.
    """
    if kind.startswith("single"):
        specs = [(int(kind[-1]), 0., 0.)]
        links = []
    elif kind == "pair":
        specs = [(2, 1/6, 0.), (1, -1/3, .5)]
        links = [(0, 1, -.5)]
    elif kind == "lepton":
        specs = [(2, -.5, 0.), (1, -1., .5)]
        links = [(0, 1, -.5)]
    elif kind in ("quark", "parallel"):
        upper_m = .5 if kind == "quark" else -.5
        specs = [(2, 1/6, 0.), (1, -1/3, .5), (1, 2/3, -upper_m)]
        links = [(0, 1, -.5), (0, 2, upper_m)]
    else:
        raise ValueError(kind)
    grouped = {}
    for f, (n, y, offset) in enumerate(specs):
        for st in states(n, levels):
            k2 = st[2]-round(2*offset)
            grouped.setdefault(k2, []).append((f, *st))
    output = []
    for k2, basis in sorted(grouped.items()):
        N = len(basis)
        index = {s:i for i,s in enumerate(basis)}
        D = np.zeros((N,N)); C = np.zeros((N,N))
        gamma = np.diag([s[1] for s in basis])
        T = [np.diag([s[3]/2 for s in basis]),
             np.diag([specs[s[0]][1] for s in basis]),
             np.diag([specs[s[0]][0] for s in basis])]
        for i, (f,tau,j2,m2) in enumerate(basis):
            n = specs[f][0]; j=j2/2; m=m2/2; spin=(n-tau)/2
            flip=index.get((f,-tau,j2,m2))
            if flip is not None:
                D[i,flip]=sqrt(max(0.,j*(j+1)-(n*n-1)/4))
            if j:
                C[i,i]=-spin*m/(j*(j+1))
            up=index.get((f,tau,j2+2,m2))
            if up is not None:
                val=sqrt(max(0.,((j+1)**2-m*m)*((j+1)**2-spin*spin)
                             /((j+1)**2*(2*j+1)*(2*j+3))))
                C[i,up]=C[up,i]=val
        L=-gamma@(D@C-C@D)
        S=[]
        for target, source, mh in links:
            M=np.zeros((N,N))
            for i, (f,*st) in enumerate(basis):
                if f != target: continue
                for j, (g,*ss) in enumerate(basis):
                    if g == source:
                        M[i,j]=M[j,i]=yukawa_element(st,ss,mh)
            S.append(gamma@M)
        output.append(dict(k2=k2,basis=basis,D=D,C=C,gamma=gamma,L=L,T=T,S=S))
    return output


def heat_moments(e, a):
    """I0=integral heat, Iu=integral s(1-s)heat, Iodd=integral (1-2s)heat.

    Stable at repeated eigenvalues; exponentials use the lower endpoint.
    """
    x=a*e[:,None]; y=a*e[None,:]
    d=x-y
    choose=d.real>=0
    t=np.where(choose,d,-d)
    small=np.abs(t)<1.0
    f0=np.empty_like(t); fu=np.empty_like(t)
    z=t[small]
    # Integral Taylor coefficients: I0=sum (-t)^k/(k!(k+1));
    # Iu=sum (-t)^k/(k!(k+2)(k+3)).
    p=np.ones_like(z); q0=np.ones_like(z); qu=np.ones_like(z)/6
    for k in range(1,25):
        p*= -z/k
        q0+=p/(k+1); qu+=p/((k+2)*(k+3))
    f0[small]=q0; fu[small]=qu
    z=t[~small]; ez=np.exp(-z)
    f0[~small]=-np.expm1(-z)/z
    fu[~small]=((z-2)+(z+2)*ez)/z**3
    damp=np.exp(-np.where(choose,y,x))
    I0=damp*f0; Iu=damp*fu
    return I0,Iu,d*Iu


def scalar_quadratic(R, nodes, levels=8):
    """Per one n2--n1 Yukawa link: V/(kappa Lambda^4)=A2 h^2+...;
    Lkin=kappa Lambda^2 G/2 (partial h)^2. M/Lambda=h Y.
    """
    vals=np.zeros((len(nodes),2))
    for b in blocks("pair",levels):
        B=b['D']/R; S=b['S'][0]
        v,U=eigh(B); e=v*v
        Se=U.T@S@U; A=(v[:,None]+v[None,:])*Se
        for k,a in enumerate(nodes):
            I0,Iu,_=heat_moments(e,a)
            contact=np.dot(np.diag(Se@Se),np.exp(-a*e))
            vals[k,0]+=(-contact/a+.5*np.sum(I0*A*A))/(8*pi*pi)
            vals[k,1]+=np.sum(I0*Se*Se-a*Iu*A*A)/(8*pi*pi)
    return vals


def potential_coefficients(R,nodes,kind="pair",levels=7,method="toeplitz",radius=.3,points=20):
    """A2,A4 along equal real amplitudes on all links, per species block.

    Toeplitz exponential gives Taylor coefficients without finite differences.
    Cauchy contour/eigenvalue method is an independent numerical cross-check.
    """
    out=np.zeros((len(nodes),2))
    for b in blocks(kind,levels):
        B=b['D']/R; S=sum(b['S']); N=len(B)
        if method == "toeplitz":
            E=B@B; A=B@S+S@B; Z=S@S
            H=np.zeros((5*N,5*N))
            for i in range(5):
                H[i*N:(i+1)*N,i*N:(i+1)*N]=E
                if i<4: H[i*N:(i+1)*N,(i+1)*N:(i+2)*N]=A
                if i<3: H[i*N:(i+1)*N,(i+2)*N:(i+3)*N]=Z
            for k,a in enumerate(nodes):
                ex=expm(-a*H)
                out[k,0]+=np.trace(ex[:N,2*N:3*N])/(8*pi*pi*a*a)
                out[k,1]+=np.trace(ex[:N,4*N:5*N])/(8*pi*pi*a*a)
        elif method == "cauchy":
            accum=np.zeros((len(nodes),2),complex)
            for j in range(points):
                angle=2*pi*j/points; h=radius*np.exp(1j*angle)
                ev=eigvals(B+h*S)
                heat=np.exp(-np.asarray(nodes)[:,None]*ev[None,:]**2).sum(axis=1)
                for col,order in enumerate((2,4)):
                    accum[:,col]+=heat*np.exp(-1j*order*angle)/(points*radius**order)
            out+=accum.real/(8*pi*pi*np.asarray(nodes)[:,None]**2)
        else:
            raise ValueError(method)
    return out


def neutral_response(R,nodes,kind="quark",amplitudes=(0.,0.),levels=8,pauli=True):
    """Full neutral K/kappa and transverse M^2/(kappa Lambda^2).

    T=(J3,Y,X), includes all four geometric weak-response terms and the
    noncommuting-mass terms. Background amplitudes are M/Lambda=h_i Y_i.
    """
    K=np.zeros((len(nodes),3,3)); mass=np.zeros_like(K)
    for b in blocks(kind,levels):
        B=b['D']/R+sum((h*S for h,S in zip(amplitudes,b['S'])),np.zeros_like(b['D']))
        v,U=eigh(B); e=v*v
        T=np.array([U.T@t@U for t in b['T']])
        LL=np.zeros_like(T); LL[0]=U.T@b['L']@U if pauli else 0.
        CC=(v[:,None]-v[None,:])*T
        c=R/4
        V=-T+c*(v[:,None]+v[None,:])*LL
        for k,a in enumerate(nodes):
            I0,Iu,Io=heat_moments(e,a); heat=np.exp(-a*e)
            for x in range(3):
                for y in range(x,3):
                    contact=np.dot(np.sum(LL[x]*LL[y],axis=1),heat)
                    integrand=(I0*(V[x]*V[y]+4*c*c/a*LL[x]*LL[y])
                               +c*Io*(CC[x]*LL[y]+CC[y]*LL[x])
                               -Iu*(2*T[x]*T[y]+a*CC[x]*CC[y]))
                    val=(integrand.sum()-2*c*c/a*contact)/(8*pi*pi)
                    K[k,x,y]+=val
                    if x != y: K[k,y,x]+=val
                    contactT=np.dot(np.sum(T[x]*T[y],axis=1),heat)
                    valM=(2/a*(np.sum(I0*T[x]*T[y])-contactT)+np.sum(I0*CC[x]*CC[y]))/(8*pi*pi)
                    mass[k,x,y]+=valM
                    if x != y: mass[k,y,x]+=valM
    return K,mass


def full_response(R,nodes,hd,hu,levels=8,yukawas=(1.,1.,1.),Nb=4):
    yd,ye,yu=yukawas
    kq,mq=neutral_response(R,nodes,'quark',(yd*hd,yu*hu),levels)
    kl,ml=neutral_response(R,nodes,'lepton',(ye*hd,),levels)
    # The n=0 spectator has no Higgs coupling. Its K cancels in every shift.
    return Nb*(3*kq+kl),Nb*(3*mq+ml)


def higgs_shifts(R,nodes,levels=8,step=.04):
    """Second-order shifts for the two neutral vevs; Richardson in h^2.
    Entries multiply h_d^2 or h_u^2 with unit dimensionless Yukawas.
    """
    K0,M0=full_response(R,nodes,0.,0.,levels)
    shifts=[]; masses=[]; errors=[]
    for direction in ((1.,0.),(0.,1.)):
        kval=[]; mval=[]
        for h in (step,step/2,step/4):
            K,M=full_response(R,nodes,h*direction[0],h*direction[1],levels)
            kval.append((K-K0)/h**2);mval.append((M-M0)/h**2)
        r1=(4*kval[1]-kval[0])/3;r2=(4*kval[2]-kval[1])/3
        shifts.append((16*r2-r1)/15)
        errors.append(np.max(np.abs(r2-r1)))
        mr1=(4*mval[1]-mval[0])/3;mr2=(4*mval[2]-mval[1])/3
        masses.append((16*mr2-mr1)/15)
    return np.array(shifts),np.array(masses),np.array(errors)


def analytic_response(R,nodes,kind,amplitudes,levels=8):
    """Holomorphic continuation of K, using a general similarity eigenbasis.

    This permits Cauchy extraction of h^2, without subtracting nearly equal
    real-background responses. Transposes here mean index reversal, never
    complex conjugation. No absolute values of analytically continued data.
    """
    K=np.zeros((len(nodes),3,3),complex)
    for b in blocks(kind,levels):
        B=b['D']/R+sum((h*S for h,S in zip(amplitudes,b['S'])),np.zeros_like(b['D']))
        v,U=eig(B); Ui=np.linalg.inv(U); e=v*v
        T=np.array([Ui@t@U for t in b['T']])
        LL=np.zeros_like(T); LL[0]=Ui@b['L']@U
        CC=(v[:,None]-v[None,:])*T; c=R/4
        V=-T+c*(v[:,None]+v[None,:])*LL
        for k,a in enumerate(nodes):
            I0,Iu,Io=heat_moments(e,a); heat=np.exp(-a*e)
            for x in range(3):
                for y in range(x,3):
                    contact=np.dot(np.sum(LL[x]*LL[y].T,axis=1),heat)
                    terms=(I0*(V[x]*V[y].T+4*c*c/a*LL[x]*LL[y].T)
                           +c*Io*(CC[x]*LL[y].T+CC[y]*LL[x].T)
                           -Iu*(2*T[x]*T[y].T-a*CC[x]*CC[y].T))
                    value=(terms.sum()-2*c*c/a*contact)/(8*pi*pi)
                    K[k,x,y]+=value
                    if x != y: K[k,y,x]+=value
    return K


def cauchy_shifts(R,nodes,levels=8,radius=.2,points=16):
    """Coefficient of h_i^2 in full K/kappa, Nb=4 and unit Yukawas."""
    shifts=np.zeros((2,len(nodes),3,3),complex)
    for direction in range(2):
        for k in range(points):
            angle=2*pi*k/points; h=radius*np.exp(1j*angle)
            amps=(h,0.) if direction==0 else (0.,h)
            response=12*analytic_response(R,nodes,'quark',amps,levels)
            if direction==0:
                response+=4*analytic_response(R,nodes,'lepton',(h,),levels)
            shifts[direction]+=response*np.exp(-2j*angle)/(points*radius**2)
    return shifts
