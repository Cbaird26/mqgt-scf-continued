"""Notes 31-32: deliberately conversion-only radiation-era toy trajectory.

Masses and widths in GeV. Not a relic density or cosmological evolution
of the actual model. No hadronic/scattering channels, annihilation, changes
in g_star or g_starS, plasma correction, or physical initial conditions.
"""
from __future__ import annotations
import math

M1 = 10.0
M2 = 11.5
GAMMA_LEP = 3.060267688e-22
M_PLANCK = 1.2209e19


def kve_integral(nu: int, z: float, intervals: int = 320) -> float:
    """Approximate exp(z)*K_nu(z) by a positive integral on [0,4].

    Simpson rule is a numerical approximation, not a certified interval
    enclosure. Only the specified nonrelativistic x window is supported.
    """
    if nu not in (1, 2) or not math.isfinite(z) or not 8 <= z <= 100:
        raise ValueError('order 1 or 2 and z in [8,100] required')
    if not isinstance(intervals, int) or intervals < 80 or intervals % 2:
        raise ValueError('interval count must be even integer >=80')
    h = 4.0 / intervals
    def f(t):
        return math.exp(-z*(math.cosh(t)-1))*math.cosh(nu*t)
    accum = f(0)+f(4)
    for i in range(1, intervals):
        accum += (4 if i % 2 else 2)*f(i*h)
    return accum*h/3


def mb_rates(x: float, width=GAMMA_LEP, gstar=60.0) -> dict:
    """Conditional ideal-MB q, thermally dilated decays and Hubble rate."""
    if math.isfinite(x) and 30 < x < 30+1e-12:
        x = 30.0  # endpoint floating-point rounding, not extrapolation
    if not all(math.isfinite(t) for t in (x,width,gstar)) or not 10 <= x <= 30 or width < 0 or gstar <= 0:
        raise ValueError('x must lie [10,30], width nonnegative, gstar positive')
    T = M1/x
    z1, z2 = x, x*M2/M1
    k21 = kve_integral(2,z1)
    k22 = kve_integral(2,z2)
    d2 = kve_integral(1,z2)/k22
    q = (M2/M1)**2*math.exp(-(M2-M1)/T)*k22/k21
    H = math.sqrt(8*math.pi**3*gstar/90)*T*T/M_PLANCK
    A = width*d2
    B = A*q
    lam = A+B
    return dict(x=x,T=T,q=q,r=q/(1+q),d2=d2,H=H,A=A,B=B,
                Lambda=lam,Lambda_H=lam/H,dy_dx_factor=lam/(x*H))


def rhs(x:float,y:float,width=GAMMA_LEP,gstar=60.0)->float:
    if not math.isfinite(y) or not 0 <= y <= 1:
        raise ValueError('population fraction must be in [0,1]')
    metrics = mb_rates(x,width,gstar)
    return -metrics['dy_dx_factor']*(y-metrics['r'])


def evolve(x0=10.0,x1=30.0,steps=400,width=GAMMA_LEP,gstar=60.0,
           method='rk4',y0=None):
    """Return (x,y) trajectory; equilibrium initialization only if y0=None.

    RK4 suits small, nonstiff widths; exp-mid is a positivity-preserving
    exponential-midpoint method for larger rates. Neither represents a
    complete freeze-out or Boltzmann solver.
    """
    if (not isinstance(steps,int) or steps<1 or not all(map(math.isfinite,(x0,x1,width,gstar)))
            or not 10 <= x0 < x1 <= 30 or width<0 or gstar<=0
            or method not in ('rk4','exp-mid')):
        raise ValueError('invalid trajectory configuration')
    y=mb_rates(x0,width,gstar)['r'] if y0 is None else float(y0)
    if not math.isfinite(y) or not 0<=y<=1:
        raise ValueError('y0 must be a fraction')
    step=(x1-x0)/steps
    output=[(x0,y)]
    for i in range(steps):
        x=x0+i*step
        if method=='rk4':
            if width>GAMMA_LEP*10000:
                raise ValueError('RK4 may be stiff: use exp-mid')
            k1=rhs(x,y,width,gstar)
            k2=rhs(x+step/2,y+step*k1/2,width,gstar)
            k3=rhs(x+step/2,y+step*k2/2,width,gstar)
            k4=rhs(x+step,y+step*k3,width,gstar)
            y+=step*(k1+2*k2+2*k3+k4)/6
        else:
            mid=mb_rates(x+step/2,width,gstar)
            y=mid['r']+(y-mid['r'])*math.exp(-step*mid['dy_dx_factor'])
        if not math.isfinite(y) or not 0<=y<=1:
            raise ArithmeticError('trajectory left [0,1]')
        output.append((x0+(i+1)*step,y))
    return output


if __name__=='__main__':
    for rate in (0,GAMMA_LEP):
        trajectory=evolve(width=rate)
        print('vacuum leptonic width=',rate,'GeV; conditional y(10)=',trajectory[0][1])
        for i in (200,400):
            x,y=trajectory[i]
            metrics=mb_rates(x,rate)
            print(f'x={x:g}; y={y:.12g}; equilibrium r={metrics["r"]:.12g}; Lambda/H={metrics["Lambda_H"]:.12g}')
