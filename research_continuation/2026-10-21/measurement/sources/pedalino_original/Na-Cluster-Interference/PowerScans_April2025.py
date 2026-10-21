#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analysis of the Vienna Na cluster interference measurements from April 2025
-- power scan --

@author: Klaus Hornberger
"""
import numpy as np
import pandas as pd
import scipy.constants as co
import matplotlib.pyplot as plt
import talbotlau as tl


####################################################
#
#   April 2025 Sodium cluster interference
#   Power Scans
#

scan_name = '2204'
#scan_name = '1604'

plot_data = True
Extract_phase = False
create_animation = False

mydpi = 150

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
        setup['sigma_v'] = 10 # Gaussian standard deviation    
        nominal_m_mean = 200000 * co.m_u
        rows, cols = 10, 5
        
    case '2204':
        # source: .docx
        # 95 measurements
        dirname = "Na-Cluster/Data_April2025/22042025/"
        exelname = "Powerscan_85kTh_22042025.xlsx"
        massspecname = "Mass spec/Sodium_He_60sccm_Ar_161sccm_356C_425nm_L12p5cm_HP_massscan_16.dat"
        particle['name'] = scan_name
        setup['v_mean'] = 158
        setup['sigma_v'] = 9  # Gaussian standard deviation
        nominal_m_mean = 170000 * co.m_u
        rows, cols = 20, 5


################################################
#
# Ad hoc modifications of setup parameters
#
# grating1['reflectivity'] *= 0.95
# grating2['reflectivity'] *= 0.95
# grating3['reflectivity'] *= 0.95



####################################################
#
#  read filenames, powers, positions, counts, mass spectrum 
# 
df = pd.read_excel(dirname+exelname)
# create array of dicionaries, each containing the data of a scan
# (note: array index = file name index -1)
dataset = [None] * len(df)
# 
for idx, dname in df['name'].items():
    try:
        fullname = dirname + 'Interference Scans/'+dname+"_s1.dat"
        array = np.loadtxt(fullname , delimiter='\t', dtype=int)
        dataset[idx] = {
            "name": dname, # data filename (short)
            "P_G1": df.iloc[idx,5] * 1e-3, # G1 Power in Watt
            "P_G2": df.iloc[idx,6] * 1e-3, # G2 Power in Watt
            "P_G3": df.iloc[idx,7] * 1e-3, # G2 Power in Watt
            "full_counts": df.iloc[idx,1] * 1000, # counts w/o laser power
            "xs": array[:,0] * 1e-9, # Grating shift 
            "counts": array[:,1], 
            }
    except FileNotFoundError:
        print(f"File {dname} not found (Index {idx}).")
    except Exception as e:
        print(f"Error reading {dname} (Index {idx}): {e}")

# remove reference scans from dataset
for idx, data in enumerate(dataset):
    if data['P_G1'] < 1e-3:
        del dataset[idx]


###################################################
#
# provide mass distribution & mean mass:
# based on cutting out [0.85*nominal_m_mean ,1.15*nominal_m_mean ] from QMS mass scan 
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
print(f"{particle['name']} mean mass: {particle['m_mean'] / co.m_u / 1000:.3g} kDa")

# choose type of mass averaging
match "inter": # "all", "inter", "edges", [  "naive"  ]
    case 'all': # (only) all masses in the xperimental spectrum
        particle['masses'] = mass_spectrum
        particle['mass_distr'] = mass_counts
    case "inter": # interpolate n_inter points between points in the mass spectrum
        particle['masses'] = mass_spectrum_inter
        particle['mass_distr'] = mass_counts_inter
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

print(f"mean mass after binning: {np.average(particle['masses'], weights=particle['mass_distr']) / co.m_u / 1000:.3g} kDa")

if plot_data:
    plt.figure(figsize=(10, 6), dpi=mydpi)
    plt.bar(mass_spectrum/co.m_u, mass_counts / np.gradient(mass_spectrum/co.m_u), 
            width=np.gradient(mass_spectrum/co.m_u), align='center',          
            edgecolor='black', color='grey', alpha=0.8)
    plt.bar(particle['masses']/co.m_u, particle['mass_distr'] / np.gradient(particle['masses']/co.m_u), 
            width=np.gradient(particle['masses']/co.m_u), align='center',          
            edgecolor='blue', color='blue', alpha=0.4)
    plt.xlabel(r'mass (amu)')
    plt.suptitle(scan_name + " power scan - mass distribution", y=.92, fontsize=12)
    plt.show()

###################################################
#
# shift the data onto a single grating period
# (for easier Fourier analysis and phase extraction)
# -- assming the period to be known -- 
# and extract sinusoidal visibility etc
#
from scipy.stats import binned_statistic
binsize = 15e-9
period = grating3['period']
N_bins = round(period / binsize) 
for data in dataset:
    mean_counts, bin_edges, _ = binned_statistic(
        data['xs'] % period, # xs modulo period
        data['counts'], 
        statistic='mean', bins=N_bins, range=(0, period))
    data['xs_mod_d'] = bin_edges[0:-1] + binsize/2
    data['counts_mod_d'] = mean_counts
    #not:  data['integrated_counts'] = 0
    # record standard deviations of the
    std_counts, _ , _ = binned_statistic(
        data['xs'] % period, # xs modulo period
        data['counts'], 
        statistic='std', bins=N_bins, range=(0, period))
    data['sigma_counts_mod_d'] = std_counts
    # Calculate Fourier coefficients of experimental data
    data['S_ell'] = np.fft.fft(mean_counts) / N_bins
    # 
    data['S_mean'] = np.abs(data['S_ell'][0])
    data['V_fft'] = 2 * np.abs(data['S_ell'][1] / data['S_ell'][0])
    data['phase_fft'] = np.angle(data['S_ell'][1] * np.exp(-2j*np.pi*binsize/2/period)) 

###################################################
#
# perform nonlinear fit to extract visibilities and 
# transmissions including their statistical errors 
# using the fft values as initial guesses
#
from scipy.optimize import curve_fit
#binsize = 15e-9
period = grating3['period']
def model(x, T, V, phi):
    return T * (1.0 + V * np.cos(2.0 * np.pi * x / period + phi))
for data in dataset:
    xs = data['xs']
    cs = data['counts'] 
    # starting values from fft
    T0  = data['S_mean']
    V0  = data['V_fft']
    phi0 = data['phase_fft']
    lower_bounds = [cs.min(), 0, -np.pi]
    upper_bounds = [cs.max(), 1, np.pi]
    # non-linear least squares (equal weights ⇒ iid Gaussian assumption)
    popt, pcov = curve_fit(model, xs, cs, p0=[T0, V0, phi0],
                           bounds= [lower_bounds, upper_bounds])
    # 1-σ errors: sqrt of diagonal of covariance matrix
    perr = np.sqrt(np.diag(pcov))
    data['S_fit'] = popt[0]
    data['V_fit'] = popt[1]
    data['phase_fit'] = popt[2]
    data['S_fit_err'] = perr[0]
    data['V_fit_err'] = perr[1]
    data['phase_fit_err'] = perr[2]


###################################################
#
# plot the data of all runs (shifted to a single period)
#
max_counts = max(d['counts_mod_d'].max() for d in dataset)

if plot_data:
    fig, axes = plt.subplots(rows, cols, figsize=(12, 18), 
                             sharex=True, sharey=True, dpi=mydpi)
    axes = axes.flatten() # Flatten the axes array for easy iteration
    # Plot each dataset in a subplot
    for idx in range(len(dataset)):
        axes[idx].errorbar(dataset[idx]['xs_mod_d'] * 1e9, dataset[idx]['counts_mod_d'],
                           yerr=dataset[idx]['sigma_counts_mod_d'], fmt='bo',
                           capsize=1)
        # 
        xs = np.linspace(0, period, 200)
        cs= dataset[idx]['S_mean'] * (1 + dataset[idx]['V_fft'] 
              * np.cos(2*np.pi*xs/period +  dataset[idx]['phase_fft']))
        csfit= dataset[idx]['S_fit'] * (1 + dataset[idx]['V_fit'] 
              * np.cos(2*np.pi*xs/period +  dataset[idx]['phase_fit']))
        axes[idx].plot(xs * 1e9, cs ,'-g')
        axes[idx].plot(xs * 1e9, csfit ,'--r')
        #
        fstr = f"{dataset[idx]['name']}:\n"  + f"{dataset[idx]['P_G1']*1e3:.0f} mW, " \
            +f"{dataset[idx]['P_G2']*1e3:.0f} mW, " +f"{dataset[idx]['P_G3']*1e3:.0f} mW"
        axes[idx].text(0.01, 0.02, fstr, transform=axes[idx].transAxes,
                ha='left', va='bottom', fontsize=6, color="black", alpha=0.5) 
        axes[idx].text(0.02, .95, r"V$_{sin}$" + f"={dataset[idx]['V_fft']:.0%}" +
                       r"V$_{fit}$" + f"={dataset[idx]['V_fit']:.1%}" 
                       + r"$\pm$" f"{dataset[idx]['V_fit_err']:.1%} ",
                transform=axes[idx].transAxes,
                ha='left', va='top', fontsize=9, color="black") 
    # Remove any remaining empty subplots
    for i in range(len(dataset), len(axes)):
        fig.delaxes(axes[i])
    axes[0].autoscale(axis='y')
    axes[0].autoscale(axis='x', tight=True)
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.suptitle(scan_name + " measurement data (shifted to a single grating period)", y=.90, fontsize=12)
    plt.show()

###################################################
#
#  Collect experimental data for power scans
#
expPs = np.array([data['P_G2']  for data in dataset])
# mean number of counts within 4(!) full periods, so that phase value does not matter
# expcounts_in4d = np.array([np.where(data['xs'] < 4 * period,
#                                data['counts'],0).mean() for data in dataset])
expcounts_in4d = np.array([data['counts'][(data['xs'] >= 0) 
                                          & (data['xs'] < 4 * period)
                                         ].mean() for data in dataset])
expfftphases = np.array([data['phase_fft'] for data in dataset])
expfitphases = np.array([data['phase_fit'] for data in dataset])
expVffts = np.array([data['V_fft'] for data in dataset])
expVfits = np.array([data['V_fit'] for data in dataset])
expVfit_errs  = np.array([data['V_fit_err'] for data in dataset])


###################################################
#
# calculate averages of runs with (almost) equal power
#
expPs_mean, expVfits_mean, expVfit_errs_mean = [], [], []
expcounts_in4d_mean, expcounts_in4d_std = [], []
Pthres = 0.54321e-3
bins = np.arange(np.min(expPs), np.max(expPs) + Pthres, Pthres)
bin_indices = np.digitize(expPs, bins) - 1  # Bin indices, shifted to match 0-based indexing
# Loop through each bin to calculate the means for expPs and expVfits in each bin
for i in range(len(bins) - 1):
    mask = bin_indices == i
    if np.any(mask):  # Check if there are points in this bin
        expPs_mean.append(np.mean(expPs[mask]))        # Mean of expPs values in the bin
        expVfits_mean.append(np.mean(expVfits[mask]))  # Mean of expVfits values in the bin
        the_mean_std = np.linalg.norm(expVfit_errs[mask]) / np.sqrt(len(expVfit_errs[mask]))
        expVfit_errs_mean.append(the_mean_std)         # Standard deviation for the bin
        expcounts_in4d_mean.append(np.mean(expcounts_in4d[mask]))# Mean of expcounts values in the bin
        expcounts_in4d_std.append(np.std(expcounts_in4d[mask]))  # Std dev of expcounts values in the bin
expPs_mean = np.array(expPs_mean)
expVfits_mean = np.array(expVfits_mean)
expVfit_errs_mean = np.array(expVfit_errs_mean)
expcounts_in4d_mean = np.array(expcounts_in4d_mean)
expcounts_in4d_std = np.array(expcounts_in4d_std)

###################################################
#
#  plot extracted phases
#
if Extract_phase:
    pVt = 0.4 # threshold for V/Vmax being "high" vivibility
    exphivisphases = np.where(expVfits > pVt * expVfits.max(), expfitphases , np.nan)
    explovisphases = np.where(expVfits > pVt * expVfits.max(), np.nan, expfitphases )
    exphivisphases_fft = np.where(expVffts > pVt * expVffts.max(), expfftphases , np.nan)
    explovisphases_fft = np.where(expVffts > pVt * expVffts.max(), np.nan, expfftphases )
    # significant phases: Visibility > 3 standard deviations
    expsigphases = np.where(expVfits > 3 * expVfit_errs, expfitphases , np.nan)
    # calculate mean (accounting for periodicity)
    zs = np.exp(1j * expsigphases[~np.isnan(expsigphases)])
    mean_exp_phase = np.angle(zs.mean())
    print(f'mean extracted phase: phi={mean_exp_phase:.3}')
    #
    plt.figure(figsize=(10, 6), dpi=mydpi)
    plt.plot(expsigphases / np.pi, 'sk', label=r'V$_{fit}$ > 3$\sigma_{Vfit}$')
    plt.plot(exphivisphases / np.pi, 'bo', label=r'V$_{fit}$/V$_0$'+f'>{pVt}')
    plt.plot(explovisphases / np.pi, 'bo', markerfacecolor='none', label=r'V$_{fit}$/V$_0$'+f'<{pVt}')
    plt.plot(exphivisphases_fft / np.pi, 'gs', label=r'V$_{fft}$/V$_0$'+f'>{pVt}')
    plt.plot(explovisphases_fft / np.pi, 'gs', markerfacecolor='none', label=r'V$_{fft}$/V$_0$'+f'<{pVt}')
    plt.plot([0,len(expVfits)],[mean_exp_phase/np.pi, mean_exp_phase/np.pi] ,'k--')
    plt.xlabel('# of run')
    plt.ylabel(r'fringe phase [$\pi$]')
    plt.legend()
    plt.suptitle("Phase of the fringe pattern, at high and low visibilities", y=.92, fontsize=12)
    plt.text(len(expVfits), mean_exp_phase/np.pi, 
             f'mean extracted phase: phi={mean_exp_phase:.3}',
             ha='right', va='bottom', fontsize=12, color="black") 
    plt.show()

#################################################
#
#
#        Calculate quantum expectation
#
#
#################################################
Ps = np.linspace(0.0, 70e-3, 250)
Vs_vav = np.zeros(np.size(Ps))
Ts_vav = np.zeros(np.size(Ps))
Ts_av = np.zeros(np.size(Ps))
Ts_cl = np.zeros(np.size(Ps))
Vs_av = np.zeros(np.size(Ps))
Vs_cl = np.zeros(np.size(Ps))
P_G1 = np.mean([d['P_G1'] for d in dataset])
P_G3 = np.mean([d['P_G3'] for d in dataset])
grating1['power'] = P_G1
grating3['power'] = P_G3

vistype = 'sin' # 'vis', 'full'
#print(f"calculating {vistype} visibilities")
current = False
N_sample=15 # bins size for velocity averave

particle['mass'] = particle['m_mean']
for idx, P in enumerate(Ps):
  grating2['power']  = P
  Vs_vav[idx], Ts_vav[idx]   = tl.Vis_vav(setup, type=vistype, current=current, N_sample=N_sample)  

for idx, P in enumerate(Ps):
  grating2['power']  = P
  Vs_av[idx], Ts_av[idx] = tl.Vis_av(setup, type=vistype, current=current, N_sample=N_sample)
  

for idx, P in enumerate(Ps):
  grating2['power'] = P
  grating2['classical'] = True
  Vs_cl[idx], Ts_cl[idx] = tl.Vis_av(setup, type=vistype, current=current, N_sample=N_sample)
  grating2['classical'] = False
###################################################
#
#  Plot visibility vs power
#
fig = plt.figure(figsize=(10, 6), dpi=mydpi)
plt.errorbar(expPs_mean / 1e-3, expVfits_mean,  yerr = expVfit_errs_mean, 
             fmt='bo', capsize=5, label=r'mean V$_{sin}^{fit}$')
plt.plot(expPs / 1e-3, expVfits, 'bo', markersize=6, fillstyle='none', alpha=1,
         label=r'V$_{sin}^{fit}$')
plt.plot(expPs / 1e-3, expVffts, 'gx', markersize=8, alpha=0.8, 
         label=r'V$_{sin}^{fft}$')
plt.plot(Ps / 1e-3, Vs_av ,'k', label=r"$V (mass average)$")
#plt.plot(Ps / 1e-3, Vs_vav, ':', color='grey', label=r"$V (fixed mass)$")
plt.plot(Ps / 1e-3, Vs_cl ,'r--', label=r"$V_{class}$")
plt.xlabel(r'$G_2$ power [mW]')
plt.ylabel(rf'V$_{{{vistype}}}$')
plt.ylim(0, 1.2 * Vs_av.max())
plt.xlim(0,75)
plt.legend()
plt.suptitle(scan_name + " power scan - Visibilities", y=.92, fontsize=12)
fig.text(0.9, 0.92, f'v_mean={setup['v_mean']}', ha='right', transform=fig.transFigure)
plt.show()

###################################################
#
#  Transmission vs power
#
#

expcounts_fullmean = [] # mean of counts, not confined to 4d
predcounts = []  # predicted counts when accounting for P_G1, P_G3
for d in dataset:
    grating1['power'] = d['P_G1']
    grating2['power'] = d['P_G2']
    grating3['power'] = d['P_G3']
    _, T = tl.Vis_av(setup, type=vistype, current=current, N_sample=N_sample)
    predcounts.append(d['full_counts'] * T)
    expcounts_fullmean.append(d['counts'].mean())

fig = plt.figure(figsize=(10, 6), dpi=mydpi)
plt.plot(expPs / 1e-3, expcounts_in4d,'bo', markerfacecolor = 'none', label='data')
plt.plot(expPs / 1e-3, expcounts_fullmean,'bo', markersize= 3)
plt.plot(expPs / 1e-3, predcounts, 'ks', markerfacecolor = 'none', label='model')
plt.yscale('log')
plt.xlabel(r'$G_2$ power [mW]')
plt.ylabel(r'Counts')
plt.autoscale(axis='x', tight=True)
plt.autoscale(axis='y', tight=False)
#plt.ylim(20,200)
plt.legend()
plt.suptitle(scan_name + " power scan - mean counts (P_G1, P_G2, P_G3)", y=.92, fontsize=12)
fig.text(0.9, 0.92, f'v_mean={setup['v_mean']}', ha='right', transform=fig.transFigure)
plt.show()

# Check predition vs data set    
if create_animation:
    from matplotlib.animation import ArtistAnimation, FFMpegWriter
    import os
    
    #particle['sigma_abs_of_m'] = lambda: 6.2e-19
    if particle['name'] == '2204':
        phi = -2.48 # as extracted from data
    if particle['name'] == '1604':
        phi = 0.504 

    full_counts = np.array([d['full_counts'] for d in dataset])        
    # plt.figure()
    # plt.plot(full_counts)
    # plt.ylim(0, 1.1 * full_counts.max())
    # plt.xlabel("# of dataset")
    # plt.suptitle("Full counts without gratings", y=.92, fontsize=12)
    # plt.show()

    fig, ax = plt.subplots() 
    
    frames = []
    for data in dataset:
        points, = ax.plot(data['xs'], data['counts'] , 'o')

        grating2['power'] = data['P_G2']
        V, T = tl.Vis_av(setup)

        C0 = data["full_counts"]

        ax.set_ylim(0.0 , 0.25 * full_counts.max())        

        xa = np.linspace(0, 4.5 * grating2['period']) 
        ya = C0 * T * (1 + V * np.cos(2 * np.pi * xa/grating2['period'] + phi))
        line, = ax.plot(xa, ya, 'k')

        text = ax.text(0.5, 1.02, particle['name'] + ' ' + data['name'] + ' data vs. model',
                       ha='center', transform=ax.transAxes)
        frames.append([points, line, text]) 

    fps = 2
    animation = ArtistAnimation(fig, frames, interval = 1000/fps, blit=True, 
                                 repeat=True)
    #animation_name = "counts_vs_model_" + scan_name + ".gif" 
    #animation.save(animation_name, writer="pillow")
    #os.system(f"xdg-open {animation_name}") # linux
   
    animation_name = "counts_vs_model_" + scan_name + ".webm" 
    writer = FFMpegWriter(
        fps=fps,
        extra_args=[
            "-vcodec", "libvpx-vp9",
            "-b:v", "0",
            "-crf", "32",
            "-pix_fmt", "yuv420p",
            "-row-mt", "1",
            "-deadline", "good",
            "-cpu-used", "1"
        ]
    )
    animation.save(animation_name, writer=writer)
        