"""Positive, symmetric scalar-pair annihilation kernels in comoving momentum cells.

Declared extension: the same portal vertex, tree ffbar final states only,
and an explicit constant timelike Higgs width of 0.0041 GeV. The inverse
source uses exactly the same kernel and zero-chemical-potential equilibrium
cell masses. The cross section is spin summed, without an initial spin average.
"""
from __future__ import annotations

import math
import numpy as np
from scipy.special import kv, roots_legendre, roots_laguerre, logsumexp

MASS = np.array([10., 11.5])
MH = 125.
K = .001
WIDTH = .0041
FERMIONS = [('e', .00051099895, 1), ('mu', .1056583755, 1),
            ('tau', 1.77686, 1), ('u', .002, 3), ('d', .005, 3),
            ('s', .100, 3), ('c', 1.300, 3), ('b', 4.200, 3)]


def equilibrium_total_density(T):
    return float(np.sum(MASS**2 * T * kv(2, MASS/T)/(2*math.pi**2)))


def conditional_nodes(T, edges_y, radial_order=4):
    """Positive quadrature for each equilibrium-conditioned cell, including infinity."""
    gl, gw = roots_legendre(radial_order)
    tail_x, tail_w = roots_laguerre(max(16, 4*radial_order))
    out = []
    nbin = len(edges_y)-1
    for species, mass in enumerate(MASS):
        z = mass/T
        for cell, (lo, hi) in enumerate(zip(edges_y[:-1], edges_y[1:])):
            if np.isinf(hi):
                y = lo + tail_x
                logw = np.log(tail_w) + 2*np.log(y) - (np.hypot(z,y)-z) + tail_x
            else:
                y = (hi+lo)/2 + (hi-lo)*gl/2
                logw = np.log(gw*(hi-lo)/2) + 2*np.log(y) - (np.hypot(z,y)-z)
            probability = np.exp(logw-logsumexp(logw))
            out.extend((species*nbin+cell, species, float(a*T),
                        float(np.hypot(mass,a*T)), float(w))
                       for a,w in zip(y,probability))
    points = np.asarray(out)
    return points[:,0].astype(int), points[:,1].astype(int), points[:,2], points[:,3], points[:,4]


def sigma_v(s, Ea, Eb, width=WIDTH):
    """Sum over ffbar channels; units GeV^-2. No initial-pair symmetry factor."""
    strength = np.zeros_like(s)
    for _,mf,nc in FERMIONS:
        strength += nc*mf*mf*np.maximum(s-4*mf*mf,0.)**1.5
    denominator = 16*math.pi*np.sqrt(s)*Ea*Eb*((s-MH*MH)**2+(MH*width)**2)
    return K*K*strength/denominator


def pair_kernel(T, edges_y, radial_order=4, angular_order=24, width=WIDTH):
    cells,species,p,E,w = conditional_nodes(T, np.asarray(edges_y),radial_order)
    size = 2*(len(edges_y)-1)
    answer = np.zeros((size,size))
    c,cw = roots_legendre(angular_order)
    masses2 = MASS[species]**2
    for lo in range(0,len(p),48):
        hi = min(lo+48,len(p))
        ea,eb = E[lo:hi,None],E[None,:]
        constant = masses2[lo:hi,None]+masses2[None,:]+2*ea*eb
        pq = 2*p[lo:hi,None]*p[None,:]
        averaged = np.zeros_like(constant)
        for cosine,weight in zip(c,cw):
            averaged += (weight/2)*sigma_v(constant-pq*cosine,ea,eb,width)
        pair_index = cells[lo:hi,None]*size+cells[None,:]
        values = averaged*w[lo:hi,None]*w[None,:]
        answer += np.bincount(pair_index.ravel(),weights=values.ravel(),minlength=size*size).reshape(size,size)
    answer = (answer+answer.T)/2
    if not np.isfinite(answer).all() or np.min(answer)<0:
        raise ValueError('Invalid annihilation kernel')
    return answer


def rhs(M, kernel, equilibrium_comoving_masses, alpha):
    eq = equilibrium_comoving_masses
    return alpha*(eq*(kernel@eq)-M*(kernel@M))


def positive_step(M, step_eta, kernel, equilibrium_comoving_masses, alpha):
    """Second-order exponential midpoint for nonnegative source and bilinear loss.

    T and all external coefficients are held at the enclosing midpoint.
    This step preserves positivity by construction, without clipping.
    """
    source = alpha*equilibrium_comoving_masses*(kernel@equilibrium_comoving_masses)

    def frozen(state,loss,h):
        survival = np.exp(-h*loss)
        source_time = np.empty_like(loss)
        np.divide(-np.expm1(-h*loss),loss,out=source_time,where=loss!=0)
        source_time[loss==0] = h
        return state*survival+source*source_time

    midpoint = frozen(M,alpha*(kernel@M),step_eta/2)
    return frozen(M,alpha*(kernel@midpoint),step_eta)
