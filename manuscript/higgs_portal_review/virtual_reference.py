"""Independent high-precision special-function route for Note 46 checks.

Uses defining 1D harmonic-polylogarithm integral and mpmath polylogarithms.
The published rational coefficient expression is shared: this is an
independent NUMERICAL evaluation, not a second Feynman-diagram derivation.
"""
import mpmath as mp
from bc_virtual_finite import hk_expression


def hpl_integral(theta):
    t=mp.mpc(theta)
    def f(u):
        if not u: return mp.mpc(0)
        z=t*u
        return t*(-mp.log(z)*mp.polylog(2,-z)+2*mp.polylog(3,-z))/(1-z)
    return mp.quad(f,[0,mp.mpf('.25'),mp.mpf('.7'),1])


def product(r,dps=60):
    with mp.workdps(dps):
        r=mp.mpf(str(r))
        b=mp.sqrt(1-4*r)
        t=-4*r/(1+b)**2
        return +hk_expression(t,mp.log(t),mp.log(1-t),mp.polylog,
                   hpl_integral(t),mp.zeta(2),mp.zeta(3),mp.zeta(4))


def form(r):
    r=mp.mpf(r);tau=1/(4*r)
    if tau<=1:f=mp.asin(mp.sqrt(tau))**2
    else:
        b=mp.sqrt(1-1/tau)
        f=-(mp.log((1+b)/(1-b))-mp.j*mp.pi)**2/4
    return mp.mpf('1.5')/tau*(1+(1-1/tau)*f)
