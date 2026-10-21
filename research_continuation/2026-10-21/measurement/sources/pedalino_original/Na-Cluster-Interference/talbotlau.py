#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides functions required for calculating Talbot-Lau 
interference patterns, visibilities, etc.

The dictionary "setup" contains all data required to calculate the interference pattern 
at fixed times of flight (T_1, T_2), as well as for velocity averaging. 
In the latter case L_1, L_2 must be specified, as well as further parameters 
in grating* and particle; the values T_1, T_2 in setup and (Phi_0, n_0 in grating*) 
then get modified and are erased in the end.

If the signal is in addition to be mass averaged then the parameters in particle get modified 
and are erased in the end.

setup = { 
    # all in SI units:
    'particle': particle dictionary
    'grating_1': grating dictionary,
    'grating_2': grating dictionary,
    'grating_3': grating dictionary,
    'T_1': <time of flight between grating_1 and grating_2>,
    'T_2': <time of flight between grating_2 and grating_3>,
    # needed when averaging velocity: (which modifies T_*, grating_*)
    'L_1': <distance between grating_1 and grating_2>,
    'L_2': <distance between grating_2 and grating_3>,
    'v_mean': <mean velocty>,
    'sigma_v': <velocity standard deviation>,
    #  
    'tau_e': <coherene time parameter of modification in s or np.nan to switch off>
    'hbar_over_sigma_q': < hbar / sigma_q , length scale of modification>
    }   
grating = {
    'type':'laser' or 'square',
    'period': <grating period in m>,
    'phi_0': <maximum phase shift> [laser]
    'n_0': <maximum mean number of photons> [laser], 
    'reflectivity': 1 [laser],
    'ionization probability': 1 [laser]
    # needed when averaging velocity: (which modofies phi_0, n_0)
    'power': laser power
    'w_y': laser waist
    #
    'open_fraction': 0.48 [square]
    'classical': <Boolean> telling whether grating transformation is classical
    }
particle = {
    'mass': <mass in kg>,
    'name': 'Name'
    'alpha_m3_of_m': function returning the polarizability in m^3
    'sigma_abs_of_m': function returning the absorption cross section in m^2
                these functions allow alpha, sigme to depend on a variable mass
    'masses': [m1, m2, ..]    needed when averaging mass: modifies mass
    'mass_distr': [w1, w2, ...] weights (unnormalized)
    #'m_mean': <mean mass>,    needed when averaging mass: modifies mass
    'radius_of_m': function returning particle radius, zero for point particle case.
    }
@author: Klaus Hornberger
"""
import numpy as np
import scipy.constants as co
import scipy.special as sp
#from scipy.integrate import simpson
import cmath
from scipy.integrate import trapezoid



def B(n, xi, grating):
    """
    Calculate the Talbot-Lau coefficients as defined in Eq (B.22) of 
    [L. Martinetz, Physical Review Research 6, 043270 (2024).]
    (note: for P_D=eta-1 zeta_abs differs from xi_ion used in Stefan Nimmrichter's 
     PhD thesis by a sign)
    """
    match grating['type']:
        case 'laser':
            phi_0 = grating['phi_0']    # maximal phase shift
            n_0 = grating['n_0']        # mean number of absorbed photos
            eta = grating['reflectivity'] # mirror reflectivity
            P_D = grating['ionization probability']  # Probability of ionization/loss after photon absorption
            
            if np.isnan(phi_0) or np.isnan(n_0): # happens when updategrating was missed    
                print("Error: phi_0 or n_0 not specified for Talbot-Lau coefficients")
                
            # Define the expressions for zeta_coh, zeta_abs, and phi as functions of xi
            zeta_coh = eta * np.sin(np.pi * xi) * phi_0
            zeta_abs = eta * (np.sin(np.pi * xi / 2)**2 - P_D / 2) * n_0
            if grating['classical']:
                zeta_coh = eta * np.pi * xi * phi_0 # transformation of a classical particle
                zeta_abs = - eta * P_D * n_0 / 2 # agrees for P_D=eta=1 with Nimmrichter thesis p. 100, line 3
            phi = (- (eta**2 + 1) / 4 * n_0 
                   + (1 - P_D) * ((eta**2 + 1) / 4 * np.cos(np.pi * xi) 
                                  - 1j * (eta**2 - 1) / 4 * np.sin(np.pi * xi)) * n_0)
            
            # Calculate the sign and square root term inside the Bessel function
            bessel_argument = np.sign(zeta_coh - zeta_abs) * cmath.sqrt(zeta_coh**2 - zeta_abs**2)
            # Calculate the Bessel function of order n
            bessel_term = sp.jv(n, bessel_argument)
            
            # Calculate the fraction raised to the power n/2
            if abs(zeta_coh - zeta_abs) > 1e-25:
            #    ratio_term = fraction**power   # horror for -1.0^(-0.5)
                power = n/2.0
                fraction = (zeta_coh + zeta_abs) / (zeta_coh - zeta_abs)
                if fraction !=0 :
                    ratio_term = cmath.exp(power*cmath.log(fraction))
                else:
                     ratio_term = 1       
            else:   
                ratio_term = 1

            return np.exp(np.real(phi)) * bessel_term * ratio_term
        
        case 'square':
            f = grating['open_fraction']
            return f * sp.sinc(np.pi * n * f  / np.pi) # Attention: python uses unconventional definition of sinc()
        case _:
            return "unknown grating"

def S(ell, setup):
    """
    Calculate the Fourier coefficients of the Signal as defined in (3.44)-(3.49) of
    Stefan Nimmrichter's PhD Thesis assuming 
    - a symmetric configration (N=1, tau=T_2-T_1 << T_i) and 
    - vanishing inital transverse coherence (tilde-D is a Kronecker-delta)
    - no transverse accelertion (a=0)
    - allowing for macrorealist modification if tau_e != nan
    so that  S(x_s) = sum_ell S_ell exp(2 pi i ell x_s/x_d)
    (returns np.array if setup['tau_e'] is a np.array )
    """
    m =  setup['particle']['mass']
    d =  setup['grating_2']['period']
    T_T = d*d*m/(2*np.pi*co.hbar) # Talbot time
    tau = setup['T_2'] - setup['T_1']
    xi_1 = ell * tau / T_T
    xi_2 = ell * setup['T_2'] / T_T
    Sn = ( B(-ell, xi_1, setup['grating_1']) * B(2*ell, xi_2, setup['grating_2']) 
        * B(-ell, 0, setup['grating_3']) )
    if np.any(np.isnan(setup['tau_e'])):
        return Sn
    else:
        return Sn * R(ell,setup)
    
def R(ell,setup):
    """
    Calculate the reduction factors R_ell due to 
    macrorealist modifications so that tilde-S_ell = S_ell * R_ell 
    according to (3.105) of Stefan Nimmrichter's thesis
    generalized to 2*T --> T1 + T2 with CSL parameters replaced by
    lambda_0 (m/m_0)^2 --> (1/tau_e) (m/m_e)^2 
    r_c --> hbar/(sqrt(2)*sigma_q)
    setup['tau_e'] may be a np.array
    """
    tau_e = setup['tau_e']
    hbosq = setup['hbar_over_sigma_q']

    if ell == 0:
        return np.ones(len(tau_e))
    
    T1 = setup['T_1']
    T2 = setup['T_2']
    m =  setup['particle']['mass']
    d =  setup['grating_2']['period']
    T_T = d*d*m/(2*co.pi*co.hbar) # Talbot time
    R = setup['particle']['radius_of_m']()

    if R == 0: # point particle 
    
        satval1 = T1 / tau_e * (m / co.m_e)**2
        satval2 = T2 / tau_e * (m / co.m_e)**2
        pre1 = np.sqrt(np.pi / 2) * hbosq / (ell * d) * T_T / T1
        pre2 = np.sqrt(np.pi / 2) * hbosq / (ell * d) * T_T / T2
        arg1 = ell * d / hbosq * T1 / T_T / np.sqrt(2)
        arg2 = ell * d / hbosq * T2 / T_T / np.sqrt(2)
        exponent = - satval1 * (1 - pre1 * sp.erf(arg1)) \
                   - satval2 * (1 - pre2 * sp.erf(arg2))
        return np.exp(exponent.astype(complex))
    
    else: # spherical particle with homogeneous denisty
        # based on (4.166) [and (4.164)] from Nimmrichter thesis with sigma_s = 0
        # NOTE: Nimmrichter thesis (C.12) has a SIGN ERROR: First plus must be minus!
        # I do the full integral numeriacally see note "Reduction-Factor-Formula.pdf"
        if T1 != T2:
            print("Error: T1 != T2") # just for lazyness only T1==T2  
            
        satval = T2 / tau_e * (m / co.m_e)**2
        rho = R / hbosq
        a = ell * d / hbosq * T2 / T_T
        
       
        z = np.linspace(1e-10, 8, 200)
        Si, _ = sp.sici(a * z)
        factor = 1 - Si / (a * z)
        #factor[0] = 0.0  # lim z->0 (1 - Si/(a z)) = 0
        integrand = np.exp(-0.5 * z**2) * (sp.spherical_jn(1, z * rho)**2) * factor
        zintegral = 9 * np.sqrt(2 / np.pi) / rho**2 * trapezoid(integrand, z)
        
        exponent = - 2 * satval * zintegral
        
        return np.exp(exponent.astype(complex))
        
        
def updategrating(grating,particle,vz):
    """
    change laser grating parameters Phi_0, n_0 based on vz and particle
    """
    if grating['type'] == 'laser':
        grating['phi_0'] = ( 8 * np.sqrt(2*np.pi) * particle['alpha_m3_of_m']() 
                            * grating['power'] / (co.hbar * co.c * grating['w_y'] * vz) )
        grating['n_0'] = ( 16 * grating['period'] * particle['sigma_abs_of_m']() * grating['power']
                          / ( np.sqrt(2*np.pi)**3 * co.hbar * co.c * grating['w_y'] * vz) ) 
    return 
    
def Svav(ell, setup, current=False, N_sample=39):
    """
    Calculate velocity average of Signal Fourier coefficient S_ell
    - using L_1, L2 in setup 
    - averaging the particle current if current==True ()
    - assuming a Gaussian velocity distribution characterized by v_0, sigma_v
    - The number N_sample of sample points can be quite significant, check for converence.
    - NOTE T_1, T_2 in setup and Phi_0, n_0 in grating* get MODIFIED and are erased in the end
    - setup['tau_e'] may be a np.array
    """
    # sample points chosen such that the cumulative probability increase is constant
    Ns=N_sample
    sample = np.sqrt(2) * sp.erfinv(2 * np.linspace(1/(Ns+1),Ns/(Ns+1),Ns) - 1)
    # add points on the wings
    sample = np.sort(np.append(sample,[-1.5, 1.5, -2, 2, -2.5, 2.5 ]))
    #
    v_0 = setup['v_mean']
    sigma_v = setup['sigma_v']
    vzs = v_0 + sigma_v * sample
    if np.min(vzs) < 0:
        print("Averaging error: vz < 0")
    ws = np.exp(- (vzs-v_0)**2 / (2*sigma_v**2)) 
    if current:
        ws *= vzs
    Ss = []
    for vz in vzs: 
        updategrating(setup['grating_1'], setup['particle'], vz)
        updategrating(setup['grating_2'], setup['particle'], vz)
        updategrating(setup['grating_3'], setup['particle'], vz)
        setup['T_1'] = setup['L_1'] / vz
        setup['T_2'] = setup['L_2'] / vz
        Ss.append(S(ell, setup))
    Ss = np.array(Ss)  # 2nd index: tau_e's
    if np.isscalar(Ss[0]):  #
        Sav = trapezoid(Ss * ws, vzs) / trapezoid(ws, vzs)
    else:  # case of many tau_e's (axis=0: integration over vzs)
        Sav = trapezoid(Ss * ws[:, None], vzs, axis=0) / trapezoid(ws, vzs) 
    
    # erase the modified values (to be on the safe side)
    setup['T_1'] = setup['T_2'] = np.nan
    updategrating(setup['grating_1'],setup['particle'],np.nan)
    updategrating(setup['grating_2'],setup['particle'],np.nan)
    updategrating(setup['grating_3'],setup['particle'],np.nan)
    
    return  Sav 

def Sav(ell, setup, current=False, N_sample=39):
    """
    Calculate mass average of velocity-averaged Signal Fourier coefficient S_ell
    - using Svav() for velocity average
    - mass average is done with particle['masses'] and particle['mass_distr']  
    """
    masses = np.array(setup['particle']['masses']) 
    weights = np.array(setup['particle']['mass_distr']) 
    weights /= weights.sum()
    Sav = 0
    for idx, m in enumerate(masses): 
        setup['particle']['mass'] = m
        Sav += weights[idx] * Svav(ell, setup, current=current, N_sample=N_sample) 
    setup['particle']['mass'] = np.nan 
    return Sav

    
def Vis(setup, type='sin'):
    """
    Calculate the sinusoidal or 'full' visibility  
    (no velocity or mass averaging)
    return visibility and transmission
    """
    match type:
        case 'sin':
            T = S(0, setup).real
            V = 2 * abs(S(1, setup)) / T
            return V, T
        case 'full':
            lmax = 7
            ells = np.arange(-lmax, lmax + 1)
            Sells = np.array([S(ell, setup) for ell in ells])
            xs = np.linspace(0,1,100)
            Ss = sum(Sell * np.exp(2j * np.pi * ell * xs) for ell, Sell in zip(ells, Sells))
            S_max = Ss.real.max()
            S_min = Ss.real.min()
            T = Sells[lmax].real # S(0)
            V = (S_max - S_min).real / (S_max + S_min).real      
            return V, T
        case _:
            return "unknown type"

def Vis_vav(setup, type='sin', current=False, N_sample=39):
    """
    Calculate the sinusoidal or 'full' visibility  
    *with* velocity averaging 
    """
    match type:
        case 'sin':
            T = Svav(0, setup, current=current, N_sample=N_sample).real
            V = 2 * abs(Svav(1, setup, current=current, N_sample=N_sample)) / T
            return V, T
        case 'full':
            lmax = 5
            ells = np.arange(-lmax, lmax + 1)
            Sells = np.array([Svav(ell, setup, current=current, N_sample=N_sample) for ell in ells])
            xs = np.linspace(0,1,100)
            Ss = sum(Sell * np.exp(2j * np.pi * ell * xs) for ell, Sell in zip(ells, Sells))
            S_max = Ss.real.max()
            S_min = Ss.real.min()
            T = Sells[lmax].real # S(0)
            V = (S_max - S_min).real / (S_max + S_min).real            
            return V, T
        case _:
            return "unknown type"

def Vis_av(setup, type='sin', current=False, N_sample=39):
    """
    Calculate the sinusoidal or 'full' visibility  
    with *velocity and mass* averaging 
    """
    lmax = 5
    match type:
        case 'sin':
            T = Sav(0, setup, current=current, N_sample=N_sample).real
            V = 2 * abs(Sav(1, setup, current=current, N_sample=N_sample)) / T
            return V, T
        case 'full':
            ells = np.arange(-lmax, lmax + 1)
            Sells = np.array([Sav(ell, setup, current=current, N_sample=N_sample) for ell in ells])
            xs = np.linspace(0,1,100)
            Ss = sum(Sell * np.exp(2j * np.pi * ell * xs) for ell, Sell in zip(ells, Sells))
            S_max = Ss.real.max()
            S_min = Ss.real.min()
            T = Sells[lmax].real # S(0)
            V = (S_max - S_min).real / (S_max + S_min).real            
            return V, T
        case _:
            return "unknown type"


def JeffreysPrior(tau_e, setup, V_sin, normalize=False):
    """
    Compute [unnormalized] p(tau_e) for array tau_e, 
    requires setup['hbar_over_sigma_q'] to be set.

    Typically, tau_e = np.logspace(np.log10(tau_e_min), np.log10(tau_e_max), num_points)
    """

    m = setup['particle']['mass']
    d = setup['grating_2']['period']
    hbosq = setup['hbar_over_sigma_q']
    T_T = d**2*m/(2*np.pi*co.hbar) 
    if setup['T_1']==setup['T_2']:
        T = setup['T_1']
    else:
        print('T1 != T2 in JeffreysPrior')
            
    y = d / hbosq * T / T_T
    if y > 1e-3:    
        f = 1 - np.sqrt(np.pi/2) / y * sp.erf(y / np.sqrt(2))
    else:
        f = y**2 / 6 - y**4 / 40 # avoid cancelation of all digits
    T_tilde = T * (m / co.m_e)**2 * f  # Compute T_tilde (2.68) Schrinski-Thesis  
    # Define the p_tau based on (2.67), Schrinski-Thesis
    def p_tau(taus, Vsin, Ttilde):
        den = np.sqrt(1 - Vsin**2*np.exp(-4 * Ttilde / taus))
        return (Ttilde / taus**2) * np.sqrt(1/den - 1)
    
    # Calculate p_tau for each value of tau_e
    p_tau_array = p_tau(tau_e, V_sin, T_tilde)
    
    p_tau_array[np.where(p_tau_array == 0)] = 1e-200 #so that one can take the logarithm
    
    # Approximate the integral using trapezoidal rule to normalize p_tau
    if normalize:
        integral = trapezoid(p_tau_array, tau_e)
        p_tau_normalized = p_tau_array / integral
        return p_tau_normalized
    else:
        return p_tau_array / p_tau_array.max()

def CharacterizeDistribution(taus, dist):
    """
    Compute for the [unnormalized] distribution dist 
    mean, standard deviation, 5% quantile, Kullback–Leibler divergence from Gauss
    """
    pdf = dist / np.trapz(dist, taus)  # normalize using trapezoidal integration
    mean = np.trapz(pdf * taus, taus)
    variance = np.trapz(pdf * (taus - mean)**2, taus)
    std = np.sqrt(variance)

    # Compute bin widths
    dtaus = np.diff(taus)
    dtaus = np.append(dtaus, dtaus[-1])  # match length
    # Approximate CDF using bin widths
    cdf = np.cumsum(pdf * dtaus)
    cdf /= cdf[-1]  # normalize
    # Find 5% quantile 
    tau_5_percent = taus[np.searchsorted(cdf, 0.05)]

    #  Kullback–Leibler divergence with respect to gaussian
    gaussian = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((taus - mean)/std)**2)
    mask = (pdf > 0) & (gaussian > 0)
    kl_div = np.trapz(pdf[mask] * np.log(pdf[mask] / gaussian[mask]), taus[mask])
    
    return mean, std, tau_5_percent, kl_div
