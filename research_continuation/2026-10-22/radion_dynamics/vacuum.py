"""Untruncated, constant-background spectral potential and analytic derivatives.

P=4*pi^2*V_sp/(kappa*Lambda^4).  Coordinates are (R,h_d,h_u).
The copied mode_sums.py is unchanged from the pinned predecessor.
Finite angular matrices are numerical approximations to the infinite trace.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh
import mode_sums as modes

HERE = Path(__file__).resolve().parent
INPUT = json.loads((HERE/'inputs/common_vacuum_pair.json').read_text())
NODES = np.array(INPUT['nodes'], float)
WEIGHTS = {k: np.array(INPUT['weights_'+k], float) for k in ('minus','plus')}
RSTAR = float(INPUT['common_R'])
CSTAR = float(INPUT['metrics']['minus']['c'])
COUNTS = np.array([16.,12.])


def profile_functions(b, weights):
    """g(b), g'(b), g''(b), g=sum w_a/a^2 exp(-a b^2)."""
    a = NODES[:,None]
    ex = np.exp(-a*b[None,:]**2)
    g = (weights/NODES**2)@ex
    gp = -2*b*((weights/NODES)@ex)
    gpp = 4*b*b*(weights@ex)-2*((weights/NODES)@ex)
    return g,gp,gpp


def derivative_divided_difference(v, gp, gpp):
    d = v[:,None]-v[None,:]
    near = np.abs(d) < 1e-7*(1+np.maximum(abs(v[:,None]),abs(v[None,:])))
    out = np.divide(gp[:,None]-gp[None,:],d,out=np.zeros_like(d),where=~near)
    # Symmetric mean differs from the coincident limit only at O(d^2).
    out[near] = ((gpp[:,None]+gpp[None,:])/2)[near]
    return out


def spectral(x, profile='minus', levels=12, order=2, weights=None):
    """Return P, gradient, Hessian; all fields retained to every power.

    Full-Dirac factors /2: 6 quark +2 lepton +6 n=0 spectator.
    Unit dimensionless Yukawas and four copied blocks are fixed fixtures.
    """
    R, hd, hu = np.asarray(x,float)
    if R <= 0: raise ValueError('R must be positive')
    w = WEIGHTS[profile] if weights is None else np.asarray(weights,float)
    val=0.; grad=np.zeros(3); hess=np.zeros((3,3))
    for kind, mult in [('quark',6.),('lepton',2.),('single0',6.)]:
        for b in modes.blocks(kind,levels):
            D=b['D']; zero=np.zeros_like(D)
            Sd=b['S'][0] if b['S'] else zero
            Su=b['S'][1] if len(b['S'])>1 else zero
            B=D/R+hd*Sd+hu*Su
            v,U=eigh(B,check_finite=False)
            g,gp,gpp=profile_functions(v,w)
            val+=mult*g.sum()
            if order==0: continue
            deriv=np.array([U.T@d@U for d in (-D/R**2,Sd,Su)])
            grad+=mult*np.einsum('i,aii->a',gp,deriv)
            if order==1: continue
            div=derivative_divided_difference(v,gp,gpp)
            hess+=mult*np.einsum('ij,aij,bji->ab',div,deriv,deriv)
            hess[0,0]+=mult*np.dot(gp,np.diag(U.T@(2*D/R**3)@U))
    return val,grad,hess


def equations(x,profile='minus',levels=12):
    p,g,H=spectral(x,profile,levels)
    R=x[0]
    eq=np.array([R*g[0]-2*p,g[1],g[2]])
    jac=np.array([[R*H[0,0]-g[0],R*H[0,1]-2*g[1],R*H[0,2]-2*g[2]],H[1],H[2]])
    return eq,jac


def vacuum_record(x,profile='minus',levels=12):
    p,g,H=spectral(x,profile,levels)
    c=p/x[0]**2
    Hv=H.copy();Hv[0,0]-=2*c
    eq,_=equations(x,profile,levels)
    return dict(R=x[0],h_d=x[1],h_u=x[2],P=p,c=c,
                flat_equations=eq,potential_Hessian=Hv,
                Hessian_eigenvalues=np.linalg.eigvalsh(Hv))


def tuned_spectral(x,alpha,profile='minus',levels=12,order=2):
    """Add alpha R^2 (16 h_d^2+12 h_u^2); alpha is external input."""
    p,g,H=spectral(x,profile,levels,order)
    R=x[0];h=np.asarray(x[1:]);s=COUNTS@h**2
    p+=alpha*R*R*s
    g+=np.r_[2*alpha*R*s,2*alpha*R*R*COUNTS*h]
    H[0,0]+=2*alpha*s
    H[0,1:]+=4*alpha*R*COUNTS*h;H[1:,0]+=4*alpha*R*COUNTS*h
    H[1:,1:]+=np.diag(2*alpha*R*R*COUNTS)
    return p,g,H


def tuned_equations(x,alpha,profile='minus',levels=12):
    eq,jac=equations(x,profile,levels)
    R=x[0];h=np.asarray(x[1:])
    # R*d_R(delta P)-2*delta P is identically zero.
    eq[1:]+=2*alpha*R*R*COUNTS*h
    jac[1:,0]+=4*alpha*R*COUNTS*h
    jac[1:,1:]+=np.diag(2*alpha*R*R*COUNTS)
    return eq,jac


def charged_orientation_curvature(x,profile='minus',levels=12):
    """d^2 P/dtheta^2 for rotating up relative to down at fixed norms.

    Charged perturbations link adjacent magnetic blocks. Uses exact trace
    Hessian in the unperturbed eigenbasis; no dense angular diagonalization.
    The lepton, spectator and counterterm are orientation independent.
    """
    R,hd,hu=x;w=WEIGHTS[profile]
    bs=modes.blocks('quark',levels)
    diagonal=[];value=0.
    for b in bs:
        v,U=eigh(b['D']/R+hd*b['S'][0]+hu*b['S'][1],check_finite=False)
        _,gp,gpp=profile_functions(v,w)
        value+=6*np.dot(gp,np.diag(U.T@(-hu*b['S'][1])@U))
        diagonal.append((v,U,gp,gpp))
    for i,b in enumerate(bs):
        for j,c in enumerate(bs):
            if j<=i or abs(b['k2']-c['k2'])!=2:continue
            T=np.zeros((len(b['basis']),len(c['basis'])))
            for ii,(f,*st) in enumerate(b['basis']):
                for jj,(g,*ss) in enumerate(c['basis']):
                    if f==0 and g==2:
                        T[ii,jj]=hu*st[0]*modes.yukawa_element(st,ss,-.5)
                    elif f==2 and g==0:
                        T[ii,jj]=hu*st[0]*modes.yukawa_element(ss,st,-.5)
            vi,Ui,gpi,gppi=diagonal[i];vj,Uj,gpj,gppj=diagonal[j]
            d=vi[:,None]-vj[None,:]
            near=abs(d)<1e-7*(1+np.maximum(abs(vi[:,None]),abs(vj[None,:])))
            div=np.divide(gpi[:,None]-gpj[None,:],d,out=np.zeros_like(d),where=~near)
            div[near]=((gppi[:,None]+gppj[None,:])/2)[near]
            T=Ui.T@T@Uj
            value+=12*np.sum(div*T*T)
    return value


def scalar_amplitude_metric(x,profile='minus',levels=12):
    """G_ij in Lkin/(kappa Lambda^2)=G_ij/2 (dh_i)(dh_j)."""
    R,hd,hu=x;w=WEIGHTS[profile];out=np.zeros((2,2))
    for kind,mult in [('quark',12),('lepton',4)]:
        for b in modes.blocks(kind,levels):
            v,U=eigh(b['D']/R+hd*b['S'][0]+(hu*b['S'][1] if kind=='quark' else 0),check_finite=False)
            derivatives=[U.T@s@U for s in b['S']]
            for a,ww in zip(NODES,w):
                I0,Iu,_=modes.heat_moments(v*v,a)
                for i,Si in enumerate(derivatives):
                    Ai=(v[:,None]+v[None,:])*Si
                    for j,Sj in enumerate(derivatives):
                        Aj=(v[:,None]+v[None,:])*Sj
                        out[i,j]+=mult*ww*np.sum(I0*Si*Sj-a*Iu*Ai*Aj)/(8*np.pi**2)
    return out


def weyl_diagonal(h,alpha=0.,profile='minus'):
    """Exact leading R->infinity coefficient P(R,h,h)/R^2.

    The limit holds at fixed finite h. This is a controlled asymptotic
    expression for the full heat trace, not a polynomial expansion in h.
    """
    z=NODES*h*h/(2*np.pi)
    lepton=np.divide(-np.expm1(-z),z,out=np.ones_like(z),where=z!=0)
    return WEIGHTS[profile]@((24+24*np.exp(-z)+8*lepton)/NODES**3)+28*alpha*h*h


if __name__=='__main__':
    for h in [0.,.1,1.,2.,3.,5.,8.,12.,20.,30.]:
        L=max(12,int(RSTAR*3+h*.7))
        p,g,H=spectral([RSTAR,h,h],levels=L)
        print(h,L,p,g.tolist(),np.linalg.eigvalsh(H).tolist(),flush=True)
