"""Bounded pole searches and residue diagnostics; no global completeness claim."""
import numpy as np
from scipy.optimize import brentq, root


def real_roots(fun, lower=-20., upper=20., count=1601):
    # Resolve small tuned scalar roots in addition to the uniform mesh.
    xx=np.unique(np.r_[np.linspace(lower,upper,count),-np.geomspace(1e-8,.1,400),np.geomspace(1e-8,.1,200)])
    yy=np.array([float(np.real(fun(float(x)))) for x in xx]);roots=[];brackets=[]
    for lo,hi,a,b in zip(xx[:-1],xx[1:],yy[:-1],yy[1:]):
        if a*b<0:
            z=brentq(lambda z:float(np.real(fun(z))),lo,hi,xtol=2e-13,rtol=2e-14)
            if not roots or abs(z-roots[-1])>1e-8:roots.append(z);brackets.append([lo,hi])
    return roots,brackets


def contour(fun,bounds=(-20.,20.,-20.,20.),per_side=512):
    x0,x1,y0,y1=bounds
    zz=np.r_[np.linspace(x0+1j*y0,x1+1j*y0,per_side,endpoint=False),
             np.linspace(x1+1j*y0,x1+1j*y1,per_side,endpoint=False),
             np.linspace(x1+1j*y1,x0+1j*y1,per_side,endpoint=False),
             np.linspace(x0+1j*y1,x0+1j*y0,per_side,endpoint=False)]
    vv=np.array([fun(z) for z in zz]);phase=np.angle(np.roll(vv,-1)/vv)
    winding=float(np.sum(phase)/(2*np.pi))
    return {'bounds':list(bounds),'per_side':per_side,'winding':winding,'rounded_count':int(round(winding)),
            'max_phase_step':float(np.max(abs(phase))),'min_abs_value_on_sampled_contour':float(min(abs(vv)))}


def complex_roots(fun, bounds=(-20.,20.,0.,20.), nx=12, ny=12, known=()):
    x0,x1,y0,y1=bounds;found=list(known);attempts=[]
    for x in np.linspace(x0+.2,x1-.2,nx):
        for y in np.linspace(max(.2,y0+.2),y1-.2,ny):
            scale=max(abs(fun(complex(x,y))),1e-12)
            def eq(a):
                if abs(a[0])>50 or abs(a[1])>80:return [1e50,1e50]
                f=fun(complex(*a))/scale
                return [f.real,f.imag]
            sol=root(eq,[x,y],tol=2e-10)
            z=complex(*sol.x)
            residual=abs(fun(z))/max(scale,1e-12)
            # Relative residual and proximity to region; later null-vector checks required.
            ok=sol.success and residual<1e-8 and x0<z.real<x1 and y0+1e-7<z.imag<y1
            if ok and all(abs(z-q)>1e-6 for q in found):found.append(z)
            attempts.append({'start':[float(x),float(y)],'success':bool(sol.success),'endpoint':[z.real,z.imag],
                             'scaled_residual':float(residual),'accepted':bool(ok)})
    return sorted(found,key=lambda z:(z.imag,z.real)),attempts


def locate_by_contours(fun,bounds=(-20.,20.,.1,20.),max_depth=40):
    """Adaptive numerical argument-principle isolation, not interval certification."""
    cells=[];found=[]
    def sample(bounds,n):
        x0,x1,y0,y1=bounds
        zz=np.r_[np.linspace(x0+1j*y0,x1+1j*y0,n,endpoint=False),np.linspace(x1+1j*y0,x1+1j*y1,n,endpoint=False),
                 np.linspace(x1+1j*y1,x0+1j*y1,n,endpoint=False),np.linspace(x0+1j*y1,x0+1j*y0,n,endpoint=False)]
        vv=np.array([fun(z) for z in zz]);rat=np.roll(vv,-1)/vv
        dl=np.log(abs(rat))+1j*np.angle(rat)
        count=int(round(np.sum(dl.imag)/(2*np.pi)))
        moment=np.sum((zz+np.roll(zz,-1))/2*dl)/(2j*np.pi)
        return count,moment,float(max(abs(dl.imag))),float(min(abs(vv)))
    def walk(bounds,depth):
        n=32;last=None
        while True:
            count,moment,step,minimum=sample(bounds,n)
            if last==count and step<.5:break
            if n>=4096:raise RuntimeError('Unresolved contour')
            last=count;n*=2
        cells.append({'bounds':list(bounds),'depth':depth,'per_side':n,'count':count,'max_phase_step':step,'min_abs_value':minimum})
        if count==0:return
        if count<0:raise RuntimeError('Negative count for entire function')
        if count==1:
            start=moment
            scale=max(abs(fun(start)),1e-20)
            sol=root(lambda x:[fun(complex(*x)).real/scale,fun(complex(*x)).imag/scale],[start.real,start.imag],tol=1e-11)
            z=complex(*sol.x)
            x0,x1,y0,y1=bounds
            if (sol.success or np.linalg.norm(sol.fun)<1e-7) and x0<z.real<x1 and y0<z.imag<y1:
                found.append(z);return
        if depth>=max_depth:raise RuntimeError('Unresolved cell at depth limit')
        x0,x1,y0,y1=bounds
        # Deliberately off-center to reduce accidental root-on-boundary cases.
        if x1-x0>=y1-y0:
            mid=x0+.493*(x1-x0);walk((x0,mid,y0,y1),depth+1);walk((mid,x1,y0,y1),depth+1)
        else:
            mid=y0+.507*(y1-y0);walk((x0,x1,y0,mid),depth+1);walk((x0,x1,mid,y1),depth+1)
    walk(bounds,0)
    return sorted(found,key=lambda z:(z.imag,z.real)),cells


def polish(fun,prime,z):
    for _ in range(20):
        delta=fun(z)/prime(z);z-=delta
        if abs(delta)<2e-13*(1+abs(z)):break
    return z


def complex_residue(kernel,z):
    K,Kp,_,_=kernel.operator(z)
    _,s,Vh=np.linalg.svd(K);vv=Vh.conj().T[:,-1]
    slope=vv@Kp@vv;residue=np.outer(vv,vv)/slope
    return {'z':[z.real,z.imag], 'normalized_smallest_singular_value':float(s[-1]/s[0]),
            'complex_residue_matrix_real':residue.real.tolist(),
            'complex_residue_matrix_imag':residue.imag.tolist(),
            'residue_sign':'not defined for a non-real pole'}
