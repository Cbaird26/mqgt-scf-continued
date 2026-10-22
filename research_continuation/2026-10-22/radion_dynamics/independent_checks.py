"""Independent matrix-integral and external-curvature normalization controls."""
import numpy as np
from scipy.linalg import expm,eigvalsh
from numpy.polynomial.legendre import leggauss
import mode_sums as m
import vacuum as v


def matrix_integral_metric(x,profile='minus',levels=3,quadrature=40):
    """No internal eigenbasis or analytic heat_moments in this calculation."""
    z,wt=leggauss(quadrature);s=(z+1)/2;wt=wt/2
    R,hd,hu=x;G=np.zeros((3,3))
    for kind,n in [('quark',12),('lepton',4),('single0',12)]:
        for b in m.blocks(kind,levels):
            D=b['D'];zero=np.zeros_like(D)
            Sd=b['S'][0] if b['S'] else zero
            Su=b['S'][1] if len(b['S'])>1 else zero
            B=D/R+hd*Sd+hu*Su;E=B@B
            T=np.array([-D/R**2,Sd,Su]);A=np.array([B@t+t@B for t in T])
            for rate,w in zip(v.NODES,v.WEIGHTS[profile]):
                for u,weight in zip(s,wt):
                    L=expm(-rate*u*E);Q=expm(-rate*(1-u)*E)
                    LTQ=np.array([L@t@Q for t in T]);LAQ=np.array([L@a@Q for a in A])
                    G+=n*w*weight*(np.einsum('aij,bji->ab',LTQ,T)
                         -rate*u*(1-u)*np.einsum('aij,bji->ab',LAQ,A))/(8*np.pi**2)
    return G


def sphere4_gravity(x,profile='minus',levels=10,radii=(20.,40.,80.)):
    """Extract F from exact round S4 external Dirac heat sums.

    For radius L, eigenvalues +/-k/L, k>=2, total degeneracy
    4*k*(k*k-1)/3. Divide by Vol(S4)=8*pi^2*L^4/3.
    """
    R,hd,hu=x;h_internal=np.zeros(len(v.NODES))
    for kind,n in [('quark',12),('lepton',4),('single0',12)]:
        for b in m.blocks(kind,levels):
            B=b['D']/R
            if b['S']:B=B+hd*b['S'][0]
            if len(b['S'])>1:B=B+hu*b['S'][1]
            ev=eigvalsh(B,check_finite=False)
            h_internal+=n*np.exp(-v.NODES[:,None]*ev[None,:]**2).sum(axis=1)
    flat=np.dot(v.WEIGHTS[profile]/(8*np.pi**2*v.NODES**2),h_internal)
    estimates=[]
    for L in radii:
        k=np.arange(2,int(np.ceil(11*L/np.sqrt(v.NODES.min())))+1,dtype=float)
        deg=4*k*(k*k-1)/3;vol=8*np.pi**2*L**4/3
        h4=np.exp(-v.NODES[:,None]*k[None,:]**2/L**2)@deg/vol
        curved=.5*np.dot(v.WEIGHTS[profile]*h_internal,h4)
        estimates.append(-2*(curved-flat)/(12/L**2))
    improved=[(4*estimates[i+1]-estimates[i])/3 for i in range(len(estimates)-1)]
    return dict(external_radii=list(radii),F_estimates=estimates,Richardson=improved)


def finite_gravity_gradient(x,profile,geometry,step=1e-4):
    x=np.asarray(x);eye=np.eye(3);out=[]
    for direction in eye:
        vals=[geometry(x+k*step*direction,profile,8)[0] for k in (-2,-1,1,2)]
        out.append((vals[0]-8*vals[1]+8*vals[2]-vals[3])/(12*step))
    return np.array(out)


def dense_charged_kinetic(x,profile='minus',levels=3,quadrature=36):
    """Full flavour/angular construction, independent of magnetic blocks.

    Computes the 2x2 real charged metric by direct exponential quadrature.
    """
    R,hd,hu=x;G=np.zeros((2,2));z,wt=leggauss(quadrature);s=(z+1)/2;wt/=2
    for kind,charges,n in [('quark',[2,1,1],12),('lepton',[2,1],4)]:
        species=[m.states(n,levels) for n in charges]
        basis=[(f,*st) for f,sts in enumerate(species) for st in sts]
        lookup={st:i for i,st in enumerate(basis)};N=len(basis)
        B=np.zeros((N,N));T=np.zeros((2,N,N))
        for i,(f,tau,j2,m2) in enumerate(basis):
            j=j2/2;flip=lookup.get((f,-tau,j2,m2))
            if flip is not None:B[i,flip]=np.sqrt(j*(j+1)-(charges[f]**2-1)/4)/R
            if f!=0:continue
            for source in range(1,len(charges)):
                neutral_m=-.5 if source==1 else .5;charged_m=-neutral_m
                for st in species[source]:
                    col=lookup[(source,*st)]
                    B[i,col]=B[col,i]=tau*(hd if source==1 else hu)*m.yukawa_element((tau,j2,m2),st,neutral_m)
                    T[source-1,i,col]=T[source-1,col,i]=tau*m.yukawa_element((tau,j2,m2),st,charged_m)
        E=B@B;A=np.array([B@t+t@B for t in T])
        for rate,w in zip(v.NODES,v.WEIGHTS[profile]):
            for u,weight in zip(s,wt):
                L=expm(-rate*u*E);Q=expm(-rate*(1-u)*E)
                G+=n*w*weight*(np.einsum('aij,bji->ab',np.array([L@t@Q for t in T]),T)
                    -rate*u*(1-u)*np.einsum('aij,bji->ab',np.array([L@a@Q for a in A]),A))/(8*np.pi**2)
    return G
