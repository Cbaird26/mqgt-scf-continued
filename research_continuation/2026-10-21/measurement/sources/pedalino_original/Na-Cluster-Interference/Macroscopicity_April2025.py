#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Macroscopicity assessment for the Vienna Na cluster interference measurements from April 2025
based on https://doi.org/10.1103/PhysRevResearch.2.033034

@author: klaus hornberger
"""
import numpy as np
import pandas as pd
#import scipy as sp
import scipy.constants as co
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import os

import talbotlau as tl

####################################################
#
scan_name = '2204'
# scan_name = '1604'
create_animation = False
create_SI_plot = True    # Suppl Info Plot
print_updates = True

# hbosqs = np.logspace(-9, -6, 5 + 4 * 8)   # hbosqs > 1e-14
hbosqs = np.array([1e-8]) # 1e-8 maximizes tau_e

# hbosqs = (array of) hbar / sigma_q for which the Bayesian update is performed
# the maximizing value is the macroscopicity 
# Note: 
# for hbosqs < size of cluster (10nm) the sparticle size must taken into account, 
# see (4.166) in Stefan Nimmrichter's thesis


####################################################
#
#   April 2025 Sodium cluster interference
#

grating1 = {
    'type':'laser',
    'period': 133e-9,
    'phi_0': np.nan,
    'n_0': np.nan, 
    'reflectivity': 1,
    'ionization probability': 1,
    'w_y': 560e-6,
    'power': np.nan,
    'classical': False
    }
grating2 = {
    'type':'laser',
    'period': 133e-9,
    'phi_0': np.nan,
    'n_0': np.nan, 
    'reflectivity': 1,
    'ionization probability': 1,
    'w_y': 540e-6,
    'power': np.nan, 
    'classical': False
    }
grating3 = {
    'type':'laser',
    'period': 133e-9,
    'phi_0': np.nan,
    'n_0': np.nan, 
    'reflectivity': 1,
    'ionization probability': 1,
    'w_y': 575e-6,
    'power': np.nan, 
    'classical': False
    }
particle = {}
setup = {
    'T_1': np.nan,
    'T_2': np.nan,
    'particle': particle, 
    'grating_1': grating1,
    'grating_2': grating2,
    'grating_3': grating3,
    'tau_e':  np.nan, 
    'hbar_over_sigma_q': np.nan,
    'L_1': 0.98375, 
    'L_2': 0.98375,    
    }

# common particle properties
particle['mass'] = np.nan
particle['alpha_m3_of_m'] = lambda: -4.45e-30 * particle['mass'] / co.m_u / 22.9897
particle['sigma_abs_of_m']= lambda: ( 0.5837 * (particle['mass'] / co.m_u  / 1000 )**(2/3) - 1.5 ) * 4.24e-20
particle['radius_of_m']= lambda: (3 * particle['mass'] / (4*np.pi * 971))**(1/3) # bulk Na mass density
particle['masses'] = [] 
particle['mass_distr'] = [] 
 
match scan_name:
    case '1604':
        # source: Power_scan_100kTh_16042025
        # 48-1 measurements
        dirname = "Na-Cluster/Data_April2025/16042025/"
        exelname = "Power_scan_100kTh_16042025.xlsx"
        massspecname = "Mass spec/Sodium_HeAr_390C_60sccm_425nm_HP_14.dat"
        particle['name'] = scan_name
        setup['v_mean'] = 147
        setup['sigma_v'] = 10  # Gaussian standard deviation   
        nominal_m_mean = 200000 * co.m_u
        setup['phi'] = 0.504 # as extracted from fringe patterns using PowerScans_April2025
    case '2204':
        # source: .docx
        # 95 measurements
        dirname = "Na-Cluster/Data_April2025/22042025/"
        exelname = "Powerscan_85kTh_22042025.xlsx"
        massspecname = "Mass spec/Sodium_He_60sccm_Ar_161sccm_356C_425nm_L12p5cm_HP_massscan_16.dat"
        particle['name'] = scan_name
        setup['v_mean'] = 158
        setup['sigma_v'] = 9 #Gaussian standard deviation
        nominal_m_mean = 170000 * co.m_u
        setup['phi'] = -2.48 # as extracted from fringe patterns using PowerScans_April2025

####################################################
#
#  read filenames, powers, positions, counts 
# 
df = pd.read_excel(dirname+exelname) #, skiprows=1
# create array of dicionaries, each containing the data of a scan
# (note: array index = file name index -1)
dataset = [None] * len(df)
# 
for idx, dname in df['name'].items():
    try:
        # Öffnen und Einlesen der Datei als numpy-Array
        fullname = dirname+'Interference Scans/'+dname+"_s1.dat"
        #fullname = fullname.replace("50kTh", "100kda", 1)
        #if scan_name == '1804':
        #    fullname = fullname.replace("int","He_int")
        array = np.loadtxt(fullname , delimiter='\t', dtype=int)
        dataset[idx] = {
            "name": dname, # data filename (short)
            "P_G1": df.iloc[idx,5] * 1e-3, # G1 Power in Watt
            "P_G2": df.iloc[idx,6] * 1e-3, # G2 Power in Watt
            "P_G3": df.iloc[idx,7] * 1e-3, # G2 Power in Watt
            "full_counts": df.iloc[idx,1] * 1000, # counts ohne laser power
            "xs": array[:,0] * 1e-9, # Grating shift 
            "counts": array[:,1], 
            }
        #print(f"Inhalt von {dname} (Index {idx}):", array)
    except FileNotFoundError:
        print(f"Datei {dname} wurde nicht gefunden (Index {idx}).")

###################################################
#
# provide mass distribution & mean mass:
# based on cutting out [0.85*nominal_m_mean ,1.15*nominal_m_mean ] from QMS mass scan 
#
#
fullname = dirname + massspecname
array = np.loadtxt(fullname , delimiter='\t', dtype=float)
mass_spectrum = array[:,0] * co.m_u * 2 # doubly charged
mass_counts = array[:,1]
if np.any(mass_counts < 0): print("Error: Mass counts negative")

# for interpolating the mass spectrum
N_inter = 10
mass_spectrum_inter = np.linspace(mass_spectrum.min(), mass_spectrum.max(), 
                                  N_inter * len(mass_spectrum) )
mass_counts_inter = np.interp(mass_spectrum_inter, mass_spectrum, mass_counts)
mass_mask_inter = (mass_spectrum_inter > 0.85 * nominal_m_mean) & (mass_spectrum_inter < 1.15 * nominal_m_mean)
mass_spectrum_inter = mass_spectrum_inter[mass_mask_inter]
mass_counts_inter = mass_counts_inter[mass_mask_inter] / N_inter

mass_mask = (mass_spectrum > 0.85 * nominal_m_mean) & (mass_spectrum < 1.15 * nominal_m_mean)
mass_spectrum = mass_spectrum[mass_mask]
mass_counts = mass_counts[mass_mask]

particle['m_mean'] = np.average(mass_spectrum, weights=mass_counts) 

# choose type of mass averaging
match "inter": # "all", "edges", [  "quantile", "naive"  ]
    case 'all':
        particle['masses'] = mass_spectrum
        particle['mass_distr'] = mass_counts
    case "inter": # interpolate n_inter points between points in the mass spectrum
        particle['masses'] = mass_spectrum_inter
        particle['mass_distr'] = mass_counts_inter
        
    case 'quantile': # quantile Binning
        n_bins = 15
        if n_bins >= len(mass_spectrum): print("Error bin number too large")
        cum_w   = np.cumsum(mass_counts)
        total   = cum_w[-1]
        qs = (np.arange(n_bins) + 0.5) / n_bins * total
        particle['masses'] = np.interp(qs, cum_w, mass_spectrum)
        particle['mass_distr'] = np.full(n_bins, total / n_bins)
    case 'edges': # quantile Binning at edges, works also for n_bins >= len(mass_spectrum)
        n_bins = 15
        cum_counts = np.cumsum(mass_counts)
        total      = cum_counts[-1]
        edges = np.empty(len(mass_spectrum) + 1, dtype=float)
        edges[1:-1] = 0.5 * (mass_spectrum[:-1] + mass_spectrum[1:])
        dx0 = mass_spectrum[1] - mass_spectrum[0]
        dxn = mass_spectrum[-1] - mass_spectrum[-2]
        edges[0]     = mass_spectrum[0] - dx0/2
        edges[-1]    = mass_spectrum[-1] + dxn/2
        cdf_edges = np.concatenate(([0.0], cum_counts)) / total  
        qs = (np.arange(n_bins) + 0.5) / n_bins
        particle['masses']     = np.interp(qs, cdf_edges, edges)
        particle['mass_distr'] = np.full(n_bins, total / n_bins)
    case 'naive':  # uniform with width dm/m = 0.3 [=original assumption]
        n_bins = 11
        particle['masses'] = np.linspace(0.85 * particle['m_mean'], 
                                         1.15 * particle['m_mean'], n_bins)
        particle['mass_distr'] = np.full(len(particle['masses']), np.sum(mass_counts) / n_bins)

###################################################
#
#       Calculate macroscopicity
#
#       for given (array of) hbosqs = hbar / sigma_q
#
#

taus = np.logspace(14, 16, 400)
setup['tau_e'] = taus 
Gmean = []
Gstd = []
tau5 = []
KLdiv = []

for hbosq in hbosqs:
    setup['hbar_over_sigma_q'] = hbosq
    
    # Calculate JeffreysPrior 
    vz = setup['v_mean']
    particle['mass'] = particle['masses'].mean() # unweighted
    grating1['power'] = 60e-3 
    grating2['power'] = 30e-3 
    grating3['power'] = 60e-3 
    tl.updategrating(grating1,particle,vz)
    tl.updategrating(grating2,particle,vz)
    tl.updategrating(grating3,particle,vz)
    setup['T_1'] = setup['L_1'] / vz
    setup['T_2'] = setup['L_2'] / vz
    T_T = grating2['period']**2 * particle['mass'] / (2*np.pi*co.hbar)
    jeffreys = tl.JeffreysPrior(taus, setup, 0.5)
    
    if create_animation and len(hbosqs)==1:
        from collections import deque
        distr_history = deque(maxlen=6)
        distr_history.append(jeffreys)
        
        fig, ax = plt.subplots(figsize=(8, 4), dpi=300) 
        ax.set_xscale('log')
        ax.set_ylim(0.0, 1.02)
        line, = ax.plot(taus, jeffreys, 'b')
        frames = [[line]]
    if create_SI_plot and len(hbosqs)==1:
        SIfig, SIax = plt.subplots(figsize=(8, 5), dpi=300) 
        SIax.set_xscale('log')
        SIax.set_ylim(0.0, 1.02)
        SIax.plot(taus, jeffreys, '--')
        #SIframes = [[line]]
   
    # Bayesian updates
    
    ltd = np.log(jeffreys) # natural logarithm of tau distribution 
    N_data =0 # datapoints used
    
    for data in dataset:
        # 'raw data'
        xs = data['xs']
        cs = data['counts'] 
        C0 = data['full_counts']
        N_data += len(cs)
        # pameters for likelihood
        grating1['power'] = data['P_G1']
        grating2['power'] = data['P_G2']
        grating3['power'] = data['P_G3']
    
        V, T = tl.Vis_av(setup, type='sin', current=False)
        
        for idx, x  in enumerate(xs):
            c = cs[idx]
            S = T * (1 + V * np.cos(2 * np.pi * x/grating2['period'] 
                                    + setup['phi']))
            ltd += c * np.log(S/(1-S)) + C0 * np.log(1-S)
            ltd -= ltd.max() #normalize to maximum  e^0=1
    
        mean, std, t5, kl_div = tl.CharacterizeDistribution(taus, np.exp(ltd))
        if print_updates:
            print(data['name'][-3:]+f" tau5%={t5:.3},  mu_sig={np.log10(t5):.4g}, KL={kl_div:.3}, N={N_data}", 
                  )
        
        if create_animation and len(hbosqs)==1:
            # current tau distribution
            line, = ax.plot(taus, np.exp(ltd), color='blue', linewidth=2)
            arrow = ax.annotate('', xy=(t5, 0), xytext=(t5, -0.1),
                                arrowprops=dict(
                                arrowstyle='->', lw=1.5,              
                                color='blue', shrinkA=0, shrinkB=0  )
                                )
            arts = [line, arrow]
            # previous tau distributions
            alphas = np.linspace(0.2, 0.8, len(distr_history))
            for distr, a in zip(distr_history, alphas):
                line, = ax.plot(taus, distr, color='black', alpha=a, linewidth=1)
                arts.append(line)
            distr_history.append(np.exp(ltd))
            arts.append(ax.fill_between(taus, np.exp(ltd), where=taus <= t5, 
                        color='gray', alpha=0.3))
            # text
            arts.append(ax.text(0.5, 1.02, scan_name + '  ' + data['name'],
                           ha='center', transform=ax.transAxes))
            arts.append(ax.text(0.02, .02, r"$\mu(\hbar/\sigma_q=$"+f"{hbosq:.2}) = {np.log10(t5):.5}",
                           ha='left', transform=ax.transAxes))
            # # inset
            from matplotlib.patches import Rectangle
            rec_x0 = 0.02; rec_y0 = 0.58; rec_w = 0.3; rec_h = 0.38
            rect = Rectangle( (rec_x0, rec_y0), rec_w, rec_h,
                    transform=ax.transAxes,  
                    fill=True,               
                    facecolor = 'grey',
                    edgecolor='black',        
                    linewidth=0              
                )
            arts.append(ax.add_patch(rect))
            rec_b = 0.01 # border
            pxs = rec_x0 + rec_b + xs/xs.max() * (rec_w - 2 * rec_b)
            pys = rec_y0 + rec_b + (cs-cs.min())/(cs.max()-cs.min()) * ( rec_h - 2 * rec_b)
            dots, = ax.plot(pxs, pys, 'o', markersize=1, color='black', transform=ax.transAxes)
            arts.append(dots)
            # insetax = plt.axes([0.1, 0.6, 0.2, 0.2])  
            # #insetax.set_xlim(0, xs.max())
            # #insetax.set_ylim(0, 0.3 * C0)
            # insetax.set_xticks([]); insetax.set_yticks([])
            # inset, = insetax.plot(xs, cs, 'o', ms=3, color='green')
            # arts.append(inset)
            #            
            frames.append(arts) 
            # endof create animation
        if create_SI_plot and len(hbosqs)==1:    
            if data['name'] == 'Sodium_int_powerscan_3': # after 3*41 data points
                SIax.plot(taus, np.exp(ltd),  color='gray', linewidth=1)
                SIax.fill_between(taus, np.exp(ltd), where=taus <= t5, 
                            color='gray', alpha=0.3)
            if data['name'] == 'Sodium_int_powerscan_10': # after 10*41 data points
                SIax.plot(taus, np.exp(ltd),  color='gray', linewidth=1)
                SIax.fill_between(taus, np.exp(ltd), where=taus <= t5, 
                            color='gray', alpha=0.3)
            if data['name'] == 'Sodium_int_powerscan_95': # after 95*41 data points
                SIax.plot(taus, np.exp(ltd),  color='blue', linewidth=1)
                SIax.fill_between(taus, np.exp(ltd), where=taus <= t5, 
                            color='blue', alpha=0.3)
                SIax.annotate('', xy=(t5, 0), xytext=(t5, -0.08),
                                    arrowprops=dict(
                                    arrowstyle='->', lw=1.0,              
                                    color='blue', shrinkA=0, shrinkB=0  )
                                    )
            
        # endof data loop
    Gm, Gs, t5, KL = tl.CharacterizeDistribution(taus, np.exp(ltd))
    Gmean.append(Gm)
    Gstd.append(Gs)
    tau5.append(t5)
    KLdiv.append(KL)
    mu_sig = np.log10(t5)
    print(f"{hbosq=:.2e} {Gm=:.2e} {t5=:.2e} {KL=:.2e} {mu_sig=:.4g}", flush=True)
    # endof hbosq loop

Gmean = np.array(Gmean)
Gstd  = np.array(Gstd)
tau5  = np.array(tau5)
KLdiv = np.array(KLdiv)

print(f"{np.log10(tau5.max()):.4g}")

if len(hbosqs) > 2:
    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(hbosqs, Gmean, 'k', label=r'mean value')
    plt.fill_between(hbosqs, Gmean - Gstd, Gmean + Gstd, color='gray', 
                     alpha=0.3, label='standard deviation')
    plt.plot(hbosqs, tau5, 'b', label=r'5% percentile')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel(r'$\hbar/\sigma_q$')
    plt.ylabel(r'$\tau_e$')
    plt.legend()
    plt.suptitle(r" $\tau_e(\hbar/\sigma_q)$  " +scan_name+" data", y=.92, fontsize=12)
    # plt.text(0.02, .02, r"$\mu = " + f"{np.log10(tau5.max()):.4g}",
    #                    ha='left')
    plt.show()

if create_animation and len(hbosqs)==1:
    animation = ArtistAnimation(fig, frames, interval=500, blit=True, 
                              repeat=True)
    filename = f"update_animation_{scan_name}.gif"
    animation.save(filename, writer="pillow")
    os.system("xdg-open " + filename)
   
if create_SI_plot and len(hbosqs)==1:
    SIax.spines['top'].set_visible(False)
    SIax.spines['right'].set_visible(False)
    
    # Helvetica font and fontsize 16 for labels and ticks
    #plt.rcParams['font.family'] = 'Helvetica'
    SIax.set_xlabel(r'$\tau_e$ / s', fontsize=16)
    SIax.set_ylabel(r'$p(\tau_e)\,/\,p_{\rm max}$', fontsize=16)
    SIax.tick_params(labelsize=13)

    filename = "Bayesian_updates.png"
    SIfig.savefig(filename, bbox_inches='tight')