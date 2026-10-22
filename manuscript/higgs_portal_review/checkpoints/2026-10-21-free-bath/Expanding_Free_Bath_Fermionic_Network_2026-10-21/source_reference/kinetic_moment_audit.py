"""Note 52: exact-recoil projected lepton scattering moments, natural GeV units.

Finite vacuum tree amplitudes; ideal MB bath and dilute singlets. The six
moments are density/centered energy (four scalar moments) and one component
of the two species' drift (two vector moments). This is a near-stationary
Galerkin diagnostic, NOT the spectrum of the full momentum collision operator.
No QCD response or cosmological yield is inferred. Note 51 is unchanged.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import math
import numpy as np
from scipy.integrate import quad_vec
from scipy.linalg import eigh
from scipy.special import kv, kve, roots_legendre, gamma, gammaincc
import leptonic_conversion_scattering as base

M1, M2, MH = base.M1, base.M2, base.MH
K11, K12, K22 = 0.001, base.K12, 0.001

@dataclass(frozen=True)
class Model:
    m1: float = M1
    m2: float = M2
    mh: float = MH
    k11: float = K11
    k12: float = K12
    k22: float = K22

    def validate(self) -> None:
        if not all(math.isfinite(x) for x in (self.m1,self.m2,self.mh,self.k11,self.k12,self.k22)):
            raise ValueError('finite model parameters required')
        if min(self.m1,self.m2,self.mh)<=0 or self.m2<self.m1:
            raise ValueError('positive ordered masses required')


def thermal_stats(T: float, m: float) -> tuple[float,float,float]:
    """Mean E, Var(E)/T^2, and <p_z^2>/T^2 for scalar MB shape."""
    if not math.isfinite(T) or not math.isfinite(m) or T<=0 or m<=0:
        raise ValueError('finite positive T,m required')
    x=m/T
    if not 5<=x<=100:
        raise ValueError('numerical audit supports 5<=m/T<=100')
    r=float(kve(1,x)/kve(2,x))
    mean=3*T+m*r
    cv=3+x*x*(1-r*r)-3*x*r
    return mean,cv,mean/T+1


def equilibrium_metric(T: float, model: Model=Model()) -> tuple[np.ndarray,np.ndarray]:
    """G/N_eq diagonal in (a1,a2,b1,b2,c1,c2); phi_E=(E-mean E)/T,
    phi_p=p_z/T. A common arbitrary fugacity cancels between D and G.
    """
    base._temperature(T); model.validate()
    x1,x2=model.m1/T,model.m2/T
    ratio=(model.m2/model.m1)**2*math.exp(x1-x2)*kve(2,x2)/kve(2,x1)
    r=np.array([1/(1+ratio),ratio/(1+ratio)],float)
    stats=[thermal_stats(T,m) for m in (model.m1,model.m2)]
    diag=np.array([r[0],r[1],r[0]*stats[0][1],r[1]*stats[1][1],
                   r[0]*stats[0][2],r[1]*stats[1][2]])
    return r,diag


def boost_moments(z: float) -> tuple[float,float,float]:
    """<cosh eta>, <cosh^2 eta>, <sinh^2 eta> under invariant MB boost.
    The rapidity measure is sinh(eta)^2 exp[-z cosh(eta)] d eta.
    """
    if not math.isfinite(z) or not 5<=z<=400:
        raise ValueError('boost audit supports 5<=q/T<=400')
    r=float(kve(2,z)/kve(1,z))
    u2=3*r/z
    return r,1+u2,u2


@lru_cache(maxsize=16)
def _nodes(n: int) -> tuple[np.ndarray,np.ndarray]:
    if type(n) is not int or not 8<=n<=256:
        raise ValueError('8..256 integer t-quadrature nodes required')
    return roots_legendre(n)


def transfer_moments(q: float, mi: float, mj: float, ml: float,
                     coupling: float, mh: float=MH, n: int=24) -> tuple[float,float]:
    """(W0, Wu) = int dt |M|^2/(16pi) * (1,-t), units GeV^2, GeV^4.
    No extra spin/color/symmetry factor here. Both charges/spins enter dR.
    """
    if not math.isfinite(coupling):
        raise ValueError('finite coupling required')
    base._model(mi,mj,ml,coupling,mh)
    if not math.isfinite(q) or q<max(mi,mj)+ml:
        raise ValueError('q below common threshold')
    if q==max(mi,mj)+ml or coupling==0:
        return 0.,0.
    tm,tp=base.t_limits(q,mi,mj,ml)
    lo,hi=-tp,-tm
    x,w=_nodes(n)
    u=(hi+lo)/2+(hi-lo)*x/2
    factor=coupling**2*ml**2/(16*math.pi)*(hi-lo)/2
    integrand=(4*ml*ml+u)/(mh*mh+u)**2
    return float(factor*np.dot(w,integrand)),float(factor*np.dot(w,u*integrand))


def _rest_kinematics(q: float,mi: float,mj: float,ml: float):
    s=q*q
    ai=(s+mi*mi-ml*ml)/(2*q)
    aj=(s+mj*mj-ml*ml)/(2*q)
    pi2=max(0.,base.kallen_initial(s,mi,ml)/(4*s))
    pj2=max(0.,base.kallen_initial(s,mj,ml)/(4*s))
    return ai,aj,pi2,pj2


def weighted_jump_gram(q: float,T: float,ml: float,pair: str,
                       model: Model=Model(),n: int=24) -> np.ndarray:
    """int dW <Delta phi Delta phi^T>_boost, before thermal q weight.

    For 21 the incoming heavy and outgoing light are counted ONCE. For ii
    the factor 1/2 avoids counting both directions in the Dirichlet form.
    This 1/2 is NOT an identical-initial-particle cross-section factor.
    """
    model.validate()
    masses=(model.m1,model.m2)
    if pair=='21': i,j,k=1,0,model.k12
    elif pair=='11': i,j,k=0,0,model.k11
    elif pair=='22': i,j,k=1,1,model.k22
    else: raise ValueError('pair must be 11,21,22')
    mi,mj=masses[i],masses[j]
    w0,wu=transfer_moments(q,mi,mj,ml,k,model.mh,n)
    ans=np.zeros((6,6))
    if w0==0:
        return ans
    z=q/T
    r,g2,u2=boost_moments(z)
    bz=r/z
    if i==j:
        # Exact squared energy and vector jumps, no small-transfer expansion.
        ans[2+i,2+i]=0.5*wu*bz/(T*T)
        ans[4+i,4+i]=0.5*wu*(1+bz)/(3*T*T)
        return ans
    ai,aj,pi2,pj2=_rest_kinematics(q,mi,mj,ml)
    ei=thermal_stats(T,mi)[0]; ej=thermal_stats(T,mj)[0]
    mui=(ai*r-ei)/T; muj=(aj*r-ej)/T
    vg=g2-r*r
    eii=w0*(mui*mui+(ai*ai*vg+pi2*bz)/(T*T))
    ejj=w0*(muj*muj+(aj*aj*vg+pj2*bz)/(T*T))
    # pi.pj in the CM frame: ai*aj -(mi^2+mj^2)/2 + t/2.
    dotw=w0*(ai*aj-(mi*mi+mj*mj)/2)-wu/2
    eij=w0*mui*muj+(w0*ai*aj*vg+dotw*bz)/(T*T)
    count=np.zeros(2); count[i]=1; count[j]=-1
    e_jump=np.zeros(2); e_jump[i]=mui; e_jump[j]=-muj
    ans[:2,:2]=w0*np.outer(count,count)
    ans[:2,2:4]=w0*np.outer(count,e_jump)
    ans[2:4,:2]=ans[:2,2:4].T
    ans[2+i,2+i]=eii; ans[2+j,2+j]=ejj
    ans[2+i,2+j]=ans[2+j,2+i]=-eij
    # Isotropy converts the bath-frame spatial dot product to one component.
    p_ii=w0*(ai*ai*g2+pi2*bz-mi*mi)/(3*T*T)
    p_jj=w0*(aj*aj*g2+pj2*bz-mj*mj)/(3*T*T)
    p_ij=(w0*ai*aj*g2+dotw*bz-w0*(mi*mi+mj*mj)/2-wu/2)/(3*T*T)
    ans[4+i,4+i]=p_ii; ans[4+j,4+j]=p_jj
    ans[4+i,4+j]=ans[4+j,4+i]=-p_ij
    return ans


def collision_gram(T: float,ml: float,pair: str,model: Model=Model(),
                   method: str='w',n: int=24,cut: float=90.) -> np.ndarray:
    """D/N_eq in GeV for a single flavor and unordered species channel.
    'w' uses scaled Bessels; 'q' uses the original unscaled invariant weight.
    The invariant CM boost is integrated to infinity analytically. Only
    relative invariant energy q=q0+T*w is truncated at cut.
    """
    base._temperature(T);model.validate();_nodes(n)
    if not math.isfinite(cut) or not 30<=cut<=120:
        raise ValueError('relative-energy window must be 30..120')
    if pair not in ('11','21','22'):
        raise ValueError('pair must be 11,21,22')
    q0=(model.m1 if pair=='11' else model.m2)+ml
    if method=='w':
        norm=(kve(2,model.m1/T)+(model.m2/model.m1)**2
              *math.exp(-(model.m2-model.m1)/T)*kve(2,model.m2/T))
        pref=base.G_LEPTON*T/(8*math.pi**2*model.m1**2*norm)*math.exp(-(q0-model.m1)/T)
        def f(w):
            q=q0+T*w
            return math.exp(-w)*kve(1,q/T)*weighted_jump_gram(q,T,ml,pair,model,n)
        value,_=quad_vec(f,0.,cut,epsabs=1e-32,epsrel=2e-10,limit=300)
        return pref*value
    if method=='q':
        neq=sum(base.number_density_MB(T,m) for m in (model.m1,model.m2))
        pref=base.G_LEPTON*T/(16*math.pi**4*neq)
        def f(q):
            return kv(1,q/T)*weighted_jump_gram(q,T,ml,pair,model,n)
        value,_=quad_vec(f,q0,q0+T*cut,epsabs=1e-48,epsrel=2e-10,limit=300)
        return pref*value
    raise ValueError('method must be w or q')


def normalized_operator(D: np.ndarray,metric: np.ndarray) -> np.ndarray:
    """Symmetric G^(-1/2) D G^(-1/2); no guessed physical eigenvalues."""
    if D.shape!=(6,6) or metric.shape!=(6,) or not np.all(np.isfinite(D)):
        raise ValueError('finite 6x6 matrix and six metric entries required')
    if np.any(~np.isfinite(metric)) or np.any(metric<=0):
        raise ValueError('finite positive metric required')
    if not np.allclose(D,D.T,rtol=1e-12,atol=1e-34):
        raise ValueError('symmetric collision form required')
    return D/np.sqrt(np.outer(metric,metric))


def projected_rates(D: np.ndarray,metric: np.ndarray) -> dict:
    """Remove the EXACT total-number direction, not a numerical eigenvalue.
    Scalar basis after normalization: density contrast, energy1, energy2.
    """
    C=normalized_operator(D,metric)
    # The first two entries sum to one (metric normalized to N_eq).
    r1,r2=metric[:2]
    U=np.zeros((4,3));U[:2,0]=[math.sqrt(r2),-math.sqrt(r1)]
    U[2,1]=U[3,2]=1.
    values,vectors=eigh(U.T@C[:4,:4]@U)
    drift=eigh(C[4:,4:],eigvals_only=True)
    slow=U@vectors[:,0]
    if slow[2]<0: slow=-slow
    return {'scalar_eigenvalues_GeV':values.tolist(),
            'drift_eigenvalues_GeV':drift.tolist(),
            'slow_scalar_coefficients':(slow/np.sqrt(metric[:4])).tolist(),
            'slow_scalar_number_norm_fraction':float(np.dot(slow[:2],slow[:2])),
            'counts_only_relaxation_GeV':float(C[0,0]+C[1,1])}


def evaluate(T: float,model: Model=Model(),method: str='w',n: int=24,cut: float=90.) -> dict:
    """Per-flavor Gram matrices and FD Loewner brackets, not a FD integral."""
    fractions,metric=equilibrium_metric(T,model)
    D=np.zeros((6,6)); lower=np.zeros((6,6)); rows=[]
    for name,ml in base.LEPTONS.items():
        flavor=np.zeros((6,6)); channels={}
        for pair in ('11','21','22'):
            block=collision_gram(T,ml,pair,model,method,n,cut)
            channels[pair]=block.tolist();flavor+=block
        fac=(1+math.exp(-ml/T))**-2
        rows.append({'flavor':name,'mass_GeV':ml,'FD_pointwise_lower':fac,
                     'channels_gram_per_N_GeV':channels})
        D+=flavor;lower+=fac*flavor
    H=base.hubble(T)
    rates=projected_rates(D,metric); lows=projected_rates(lower,metric)
    for out in (rates,lows):
        out['scalar_eigenvalues_over_H']=(np.array(out['scalar_eigenvalues_GeV'])/H).tolist()
        out['drift_eigenvalues_over_H']=(np.array(out['drift_eigenvalues_GeV'])/H).tolist()
        out['counts_only_relaxation_over_H']=out['counts_only_relaxation_GeV']/H
    return {'T_GeV':T,'H_GeV':H,'assumed_gstar':60.,'fractions':fractions.tolist(),
            'metric_per_N':metric.tolist(),'D_MB_per_N_GeV':D.tolist(),
            'D_FD_lower_per_N_GeV':lower.tolist(),'MB_projected':rates,
            'FD_lower_projected':lows,'channels':rows,'method':method,'t_nodes':n,'cut':cut,
            'complete_kinetic_spectrum':False,'QCD_bath_calculated':False,
            'FD_integral_calculated':False,'abundance_calculated':False}


def complete_kinetic_equilibrium(*args,**kwargs):
    raise NotImplementedError('Projected lepton moments are not proof of full kinetic equilibrium')


def full_qcd_response(*args,**kwargs):
    raise NotImplementedError('Requires a validated spacelike finite-temperature scalar response')


def omitted_normalized_form_bound(T: float,ml: float,pair: str,
                                  model: Model=Model(),cut: float=90.) -> float:
    """Conservative spectral-norm bound for the omitted mathematical MB tail.

    Applies to G^-1/2 D_tail G^-1/2. Uses positivity, trace/min(metric),
    W0 <= K^2 ml^2/(16pi mh^4)*(4ml^2 q^2+q^4/2), E_i<=P0,
    and monotonic scaled K1,K2. Floating evaluation is not directed rounding.
    This is NOT a bound on omitted physical channels/medium corrections.
    """
    base._temperature(T); model.validate()
    if pair not in ('11','21','22') or not math.isfinite(cut) or cut<30:
        raise ValueError('valid pair and cut>=30 required')
    _,metric=equilibrium_metric(T,model)
    mi=model.m1 if pair=='11' else model.m2
    coupling={'11':model.k11,'21':model.k12,'22':model.k22}[pair]
    q0=mi+ml;zc=q0/T+cut
    norm=kve(2,model.m1/T)+(model.m2/model.m1)**2*math.exp(-(model.m2-model.m1)/T)*kve(2,model.m2/T)
    pref=base.G_LEPTON*T/(8*math.pi**2*model.m1**2*norm)*math.exp(-(q0-model.m1)/T)
    pref*=coupling**2*ml**2/(16*math.pi*model.mh**4)/float(min(metric))
    em=max(thermal_stats(T,m)[0] for m in (model.m1,model.m2))
    c0=kve(1,zc)*(2+4*em*em/(T*T))
    c2=(16/(3*T*T))*(kve(1,zc)+3*kve(2,zc)/zc)
    def moment(power):
        return sum(math.comb(power,j)*q0**(power-j)*T**j*gamma(j+1)*gammaincc(j+1,cut) for j in range(power+1))
    return float(pref*(4*ml*ml*c0*moment(2)+(c0/2+4*ml*ml*c2)*moment(4)+c2/2*moment(6)))
