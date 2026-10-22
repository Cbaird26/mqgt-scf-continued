"""Independent quadratures and external-Clifford checks.

The finite-q gauge check builds D, delta D, and delta(D^2) as full spinor
matrices, integrates the Gaussian moments, and differentiates the response.
It does not use the contracted neutral kinetic formula.
"""
from math import pi, sqrt, factorial
import numpy as np
from numpy.polynomial.legendre import leggauss


def clifford():
    I=np.eye(2); z=np.array([[1,0],[0,-1]])
    x=np.array([[0,1],[1,0]]); y=np.array([[0,-1j],[1j,0]])
    gs=[np.kron(x,I),np.kron(y,I),np.kron(z,x),np.kron(z,y)]
    g5=gs[0]@gs[1]@gs[2]@gs[3]
    return gs,g5


def direct_gauge_fourier(a,R,bvals,T,L,q,order=48):
    """Coefficient of A(q) A(-q) in S/kappa per unit four-volume."""
    gs,g5=clifford(); N=len(bvals); identity=np.eye(N)
    B=np.diag(bvals); e=np.array(bvals)**2; c=R/4
    vertex=-np.kron(gs[1],T)+c*q*np.kron(gs[0]@gs[1]@g5,L)
    vertex_back=vertex.conj().T
    h2=vertex_back@vertex+vertex@vertex_back
    contact=-a*np.dot(np.diag(h2),np.tile(np.exp(-a*e),4)).real
    xs,ws=leggauss(order); total=0.
    for s,w in zip((xs+1)/2,ws/2):
        ei=np.tile(np.exp(-a*s*e),4)
        ej=np.tile(np.exp(-a*(1-s)*e),4)
        gauss=0.
        for k1 in (-1/sqrt(2*a),1/sqrt(2*a)):
            for k2 in (-1/sqrt(2*a),1/sqrt(2*a)):
                dp=np.kron(gs[0]*(k1-s*q)+gs[1]*k2,identity)+np.kron(g5,B)
                dnext=dp+q*np.kron(gs[0],identity)
                h1=dnext@vertex+vertex@dp
                gauss+=np.sum(abs(h1)**2*ei[:,None]*ej[None,:])/4
        total+=w*np.exp(-a*s*(1-s)*q*q)*gauss
    return (contact+a*a*total)/(32*pi*pi*a*a)


def contracted_gauge_kinetic(a,R,bvals,T,L):
    from mode_sums import heat_moments
    b=np.array(bvals); e=b*b; c=R/4
    C=(b[:,None]-b[None,:])*T
    V=-T+c*(b[:,None]+b[None,:])*L
    I0,Iu,Io=heat_moments(e,a)
    contact=np.dot(np.sum(L*L,axis=1),np.exp(-a*e))
    return (np.sum(I0*(V*V+4*c*c/a*L*L)+2*c*Io*C*L
                   -Iu*(2*T*T+a*C*C))-2*c*c/a*contact)/(8*pi*pi)


def run_external_vertex_check():
    b=np.array([-.7,.2,1.1]);a=.83;R=1.3
    T=np.array([[.2,.3,-.1],[.3,-.4,.17],[-.1,.17,.6]])
    L=np.array([[.1,-.2,.25],[-.2,.2,.15],[.25,.15,-.3]])
    c0=direct_gauge_fourier(a,R,b,T,L,0.)
    vals=[(direct_gauge_fourier(a,R,b,T,L,h)-c0)/h**2 for h in (.08,.04,.02)]
    r1=(4*vals[1]-vals[0])/3;r2=(4*vals[2]-vals[1])/3
    direct=(16*r2-r1)/15
    contracted=contracted_gauge_kinetic(a,R,b,T,L)
    return dict(direct_full_clifford=direct,contracted=contracted,
                absolute_difference=abs(direct-contracted),finite_q_values=vals)


def gauss_heat_moments(e,a,order=160):
    x,w=leggauss(order);s=(x+1)/2;w=w/2
    heat=np.exp(-a*(s[:,None,None]*e[None,:,None]
                   +(1-s[:,None,None])*e[None,None,:]))
    return (np.einsum('s,sij->ij',w,heat),
            np.einsum('s,sij->ij',w*s*(1-s),heat),
            np.einsum('s,sij->ij',w*(1-2*s),heat))


def wigner_d(j,m,n,theta):
    """Factorial sum, independently used for sphere quadrature."""
    fact=lambda x:factorial(int(round(x)))
    norm=sqrt(fact(j+m)*fact(j-m)*fact(j+n)*fact(j-n))
    out=np.zeros_like(theta)
    for k in range(int(2*j)+1):
        args=(j+n-k,k,m-n+k,j-m-k)
        if min(args)<0: continue
        out+=((-1)**int(round(k+m-n))*norm/np.prod([fact(x) for x in args])
              *np.cos(theta/2)**int(round(2*j+n-m-2*k))
              *np.sin(theta/2)**int(round(m-n+2*k)))
    return out


def angular_overlap_checks():
    from mode_sums import states,yukawa_element
    x,w=leggauss(100);theta=np.arccos(x);errors=[];nchecked=0
    for source in states(1,3):
        tau,js2,ms2=source;j=js2/2;m=ms2/2;s=(1-tau)/2
        for mh in (-.5,.5):
            for J in (j-.5,j+.5):
                mt=m+mh;st=s+.5
                if J<max(abs(mt),abs(st)): continue
                target=(tau,round(2*J),round(2*mt))
                numeric=2*pi*sqrt((2*J+1)*2*(2*j+1)/(4*pi)**3)*np.dot(w,
                    wigner_d(J,mt,-st,theta)*wigner_d(.5,mh,-.5,theta)*wigner_d(j,m,-s,theta))
                errors.append(abs(numeric-yukawa_element(target,source,mh)))
                nchecked+=1
    return dict(integrals=nchecked,max_absolute_error=max(errors))
