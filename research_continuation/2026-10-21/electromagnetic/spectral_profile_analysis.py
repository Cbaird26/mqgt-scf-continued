#!/usr/bin/env python3
"""Finite-profile identifiability continuation of the 2026-10-12 spectral note.

No measured coupling is fitted. Units and hypercharge normalization are inherited
from expanded-archive PDF pp.7592-7599. Dependencies: numpy, scipy, matplotlib.
Run from any directory: python spectral_profile_analysis.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
V5 = (1, -32, 162, -256, 125)
V6 = (-1, 40, -270, 640, -625, 216)
A5 = F(5269, 8220)
A6 = A5
LOWER5, UPPER5 = -F(256, 81), F(2)
MULT = np.array([12.0, 28.0, 16.0])
CHARGE = np.array([1.0, 32.0, 4.0]) / 3.0
ARCHIVE = HERE.parents[1] / 'project_sources' / (
    '36-A-Theory-of-Everything-Baird-et-al-2026-Expanded-Research-'
    'Archive-Public-Edition-2026-10-20-2-.pdf'
)


def exact_rank(matrix):
    a = [list(map(F, row)) for row in matrix]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [x / q for x in a[r]]
        for i in range(len(a)):
            if i != r:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def profile(n=5, t=0.0):
    if n == 5:
        return (np.arange(1, 6) * float(A5),
                np.full(5, .2) + t * np.asarray(V5) / 2560.,
                np.asarray(V5, float) / 2560.)
    if n == 6:
        return (np.arange(1, 7) * float(A6),
                np.array([.2]*5+[0.]) + t * np.asarray(V6) / 7680.,
                np.asarray(V6, float) / 7680.)
    raise ValueError('Only declared five- and six-node families are supported.')


def components(radius, nodes, cutoff=40):
    """Return node-wise H, H', H'', H_Y, H_Y' from analytic derivatives."""
    p = np.arange(1, cutoff + 1, dtype=float)
    n = np.arange(3, dtype=float)
    q = nodes[:, None, None] * p[None, None, :] * (p[None, None, :] + n[None, :, None])
    d = 2 * p[None, None, :] + n[None, :, None]
    e = np.exp(-q / radius**2)
    h = n[None, :] / 2 + np.sum(d * e, axis=2)
    hp = np.sum(d * e * (2 * q / radius**3), axis=2)
    hpp = np.sum(d * e * (4 * q**2 / radius**6 - 6 * q / radius**4), axis=2)
    return h @ MULT, hp @ MULT, hpp @ MULT, h @ CHARGE, hp @ CHARGE


def evaluate(radius, nodes, weights, direction=None, cutoff=40):
    h, hp, hpp, hy, hyp = components(radius, nodes, cutoff)
    p = np.dot(weights / nodes**2, h)
    pr = np.dot(weights / nodes**2, hp)
    prr = np.dot(weights / nodes**2, hpp)
    j = np.dot(weights / nodes, h)
    jr = np.dot(weights / nodes, hp)
    ty = np.dot(weights, hy)
    tyr = np.dot(weights, hyp)
    result = {'P': p, 'P_R': pr, 'P_RR': prr, 'J': j,
              'J_R': jr, 'T': ty, 'T_R': tyr}
    if direction is not None:
        result.update(P_t=np.dot(direction / nodes**2, h),
                      P_Rt=np.dot(direction / nodes**2, hp),
                      J_t=np.dot(direction / nodes, h), T_t=np.dot(direction, hy))
    return result


def solve_profile(nodes, weights, direction=None, cutoff=40):
    def f(r):
        a = evaluate(r, nodes, weights, cutoff=cutoff)
        return r * a['P_R'] - 2 * a['P']
    # This brackets the tracked near-1.3 branch only; no global-root claim.
    radius = brentq(f, 1.20, 1.40, xtol=5e-15, rtol=1e-14)
    a = evaluate(radius, nodes, weights, direction, cutoff)
    c = a['P'] / radius**2
    z = a['T'] / (6 * math.pi**2)
    u = radius**2 * a['J'] / (24 * math.pi**2)
    result = dict(radius=radius, cosmological_subtraction=c,
                  potential_curvature=a['P_RR'] - 2 * c,
                  ZY_over_kappa=z, M4r_over_sqrt_kappa=math.sqrt(u),
                  M4r_squared_over_kappa=u, normalization_free_ratio=z/u,
                  stationarity_residual=f(radius), min_weight=float(np.min(weights)))
    if direction is not None:
        dr = -(radius * a['P_Rt'] - 2 * a['P_t']) / (radius * a['P_RR'] - a['P_R'])
        dz = (a['T_t'] + a['T_R'] * dr) / (6 * math.pi**2)
        du = (2 * radius * dr * a['J'] + radius**2 * (a['J_t'] + a['J_R'] * dr)) / (24 * math.pi**2)
        dlogq = dz/z - du/u
        result.update(dR_dt=dr, dZY_over_kappa_dt=dz,
                      dlog_ratio_dt=dlogq,
                      dt_per_unit_fractional_ratio_change=1/dlogq,
                      log_observable_jacobian_determinant=-dlogq)
    return result


def dec(x):
    if isinstance(x, F):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(str(x))


def decimal_pi():
    def atan_inv(n):
        x = Decimal(1)/n
        total = power = x
        for k in range(1, 300):
            power *= -x*x
            term = power / (2*k+1)
            total += term
            if abs(term) < Decimal('1e-78'):
                return total
        raise RuntimeError('atan convergence')
    return 16*atan_inv(Decimal(5))-4*atan_inv(Decimal(239))


def decimal_solution(nodes, weights, cutoff=40):
    """Independent 70-digit Decimal Newton implementation, no scipy root."""
    with localcontext() as ctx:
        ctx.prec = 70
        nodes, weights = list(map(dec, nodes)), list(map(dec, weights))
        pi = decimal_pi()
        def sums(r):
            vals = [Decimal(0)]*5 # P, P_R, P_RR, J, T
            for a, w in zip(nodes, weights):
                hh, dhh, ddhh, yy = [Decimal(0)]*4
                for n, dm, ym in zip(range(3), [12,28,16], [F(1,3), F(32,3), F(4,3)]):
                    h, hp, hpp = Decimal(n)/2, Decimal(0), Decimal(0)
                    for p in range(1, cutoff+1):
                        q = a*p*(p+n)
                        term = Decimal(2*p+n)*(-q/r**2).exp()
                        h += term
                        hp += term*2*q/r**3
                        hpp += term*(4*q*q/r**6-6*q/r**4)
                    hh += dm*h; dhh += dm*hp; ddhh += dm*hpp; yy += dec(ym)*h
                vals[0] += w/a**2*hh; vals[1] += w/a**2*dhh
                vals[2] += w/a**2*ddhh; vals[3] += w/a*hh; vals[4] += w*yy
            return vals
        r = Decimal('1.302')
        for iteration in range(30):
            p, pr, prr, j, ty = sums(r)
            delta = (r*pr-2*p)/(r*prr-pr)
            r -= delta
            if abs(delta) < Decimal('1e-62'):
                break
        else:
            raise RuntimeError('Decimal Newton root did not converge')
        p, pr, prr, j, ty = sums(r)
        c = p/r**2; z = ty/(6*pi*pi); u = r*r*j/(24*pi*pi)
        return {k:str(v) for k,v in dict(radius=r, cosmological_subtraction=c,
                potential_curvature=prr-2*c, ZY_over_kappa=z,
                M4r_over_sqrt_kappa=u.sqrt(), M4r_squared_over_kappa=u,
                normalization_free_ratio=z/u, stationarity_residual=r*pr-2*p).items()}


def fraction_weights(n, t):
    v, denominator = (V5,2560) if n==5 else (V6,7680)
    baseline = [F(1,5)]*5 if n==5 else [F(1,5)]*5+[F(0)]
    return [base+F(t)*F(vj,denominator) for base,vj in zip(baseline,v)]


def leading_data(nodes, weights):
    return [sum(weights)] + [sum(w/a**k for a,w in zip(nodes,weights)) for k in range(1,4)]


def heat_value_tail_bound(nodes, radius=1.4, cutoff=40):
    """Uniform bound for normalized nonnegative mixtures on these nodes.

    The integral test bounds each h_n tail once its summand decreases. The
    maximum of each node's weighted bound also bounds any convex mixture.
    This is a bound on values, not an interval enclosure of a stationary root.
    """
    candidates=[]
    for a in map(float,nodes):
        z2=radius**2/a
        if (2*cutoff)**2 < 2*z2:
            raise ValueError('Integral-test monotonicity condition fails.')
        tails=np.array([z2*math.exp(-cutoff*(cutoff+n)/z2) for n in range(3)])
        candidates.append([np.dot(MULT,tails)/a**2,
                           np.dot(MULT,tails)/a,np.dot(CHARGE,tails)])
    maxima=np.max(candidates,axis=0)
    return dict(radius_upper=radius,cutoff=cutoff,
                P_absolute=float(maxima[0]),J_absolute=float(maxima[1]),
                T_absolute=float(maxima[2]))


def source_hash():
    if ARCHIVE.exists():
        h=hashlib.sha256()
        with ARCHIVE.open('rb') as f:
            for chunk in iter(lambda:f.read(2**20),b''):
                h.update(chunk)
        return h.hexdigest()
    return None


def main():
    checks = []
    def check(name, condition, detail=None):
        if not bool(condition):
            raise AssertionError(name+': '+str(detail))
        checks.append({'name':name,'passed':True,'detail':detail})
    nodes5 = [A5*j for j in range(1,6)]
    nodes6 = [A6*j for j in range(1,7)]
    leading5 = [[F(1,j**k) for j in range(1,6)] for k in range(4)]
    leading6 = [[F(1,j**k) for j in range(1,7)] for k in range(4)]
    check('five_node_leading_constraint_rank_is_four',exact_rank(leading5)==4)
    check('five_node_exact_null_direction',all(sum(x*v for x,v in zip(row,V5))==0 for row in leading5))
    check('adding_first_derivative_has_rank_five',exact_rank(leading5+[[F(j) for j in range(1,6)]])==5)
    lo=max(-F(512,v) for v in V5 if v>0)
    hi=min(-F(512,v) for v in V5 if v<0)
    check('exact_weight_positivity_interval',lo==LOWER5 and hi==UPPER5,{'lower':str(lo),'upper':str(hi)})
    fp_slope=-sum(F(v,2560)*a for v,a in zip(V5,nodes5))
    fp_zero=-sum(a/5 for a in nodes5)
    m4_slope=sum(F(v,2560)/a**4 for v,a in zip(V5,nodes5))
    check('first_derivative_profile_datum_identifies_t_in_five_node_family',fp_slope!=0,str(fp_slope))
    check('extra_mellin_moment_identifies_t_in_five_node_family',m4_slope!=0,str(m4_slope))
    check('source_exact_leading_moments',leading_data(nodes5,fraction_weights(5,0))==
          [F(1),F(18769,26345),F(18769,26345),F(658531217359,731399400545)])
    augmented6=leading6+[[F(j) for j in range(1,7)]]
    check('six_node_extra_constraint_rank_is_five',exact_rank(augmented6)==5)
    check('six_node_exact_null_direction_preserves_first_derivative',
          all(sum(x*v for x,v in zip(row,V6))==0 for row in augmented6))
    w6minus,w6plus=fraction_weights(6,1),fraction_weights(6,2)
    check('six_node_pair_positive_weights',min(w6minus+w6plus)>0)
    check('six_node_pair_equal_leading_data',leading_data(nodes6,w6minus)==leading_data(nodes6,w6plus))
    check('six_node_pair_equal_first_derivative',sum(a*w for a,w in zip(nodes6,w6minus))==sum(a*w for a,w in zip(nodes6,w6plus)))
    check('six_node_pair_matches_original_five_node_center_leading_data',
          leading_data(nodes6,w6minus)==leading_data(nodes5,fraction_weights(5,0)))
    check('six_node_pair_matches_original_five_node_center_first_derivative',
          -sum(a*w for a,w in zip(nodes6,w6minus))==fp_zero)
    check('six_node_adding_second_derivative_has_rank_six',
          exact_rank(augmented6+[[F(j*j) for j in range(1,7)]])==6)
    # A five-constraint six-node construction gives a stronger finite-data counterexample.
    precise={}
    for label,t in [('lower_limit',LOWER5),('source_minus',F(-1)),('center',F(0)),('source_plus',F(1)),('upper_limit',UPPER5)]:
        precise[label]=decimal_solution(nodes5,fraction_weights(5,t))
    for label,t in [('six_first',F(1)),('six_second',F(2))]:
        precise[label]=decimal_solution(nodes6,fraction_weights(6,t))
    precise['exponential']=decimal_solution([F(1)],[F(1)])
    precise['rescaled_exponential']=decimal_solution([F(3)],[F(1)])
    check('source_minus_radius_reproduced',abs(float(precise['source_minus']['radius'])-1.30211764936900)<1e-13)
    check('source_plus_radius_reproduced',abs(float(precise['source_plus']['radius'])-1.30187576169391)<1e-13)
    check('source_minus_gauge_coefficient_reproduced',abs(float(precise['source_minus']['ZY_over_kappa'])-.245345972549864)<1e-14)
    check('source_plus_gauge_coefficient_reproduced',abs(float(precise['source_plus']['ZY_over_kappa'])-.245467728342579)<1e-14)
    check('source_exponential_reproduced',abs(float(precise['exponential']['radius'])-1.3007832832273603)<1e-14)
    check('scale_redefinition_leaves_gauge_and_gravity_radius_invariant',all(
        abs(float(precise['exponential'][k])-float(precise['rescaled_exponential'][k]))<1e-14
        for k in ['ZY_over_kappa','M4r_over_sqrt_kappa','normalization_free_ratio']))
    check('scale_redefinition_rescales_radius',abs(float(precise['rescaled_exponential']['radius'])/float(precise['exponential']['radius'])-math.sqrt(3))<1e-14)
    check('high_precision_stationarity_residuals',max(abs(Decimal(x['stationarity_residual'])) for x in precise.values())<Decimal('1e-55'))
    center20=decimal_solution(nodes5,fraction_weights(5,0),cutoff=20)
    high_precision_cutoff_difference=max(abs(Decimal(center20[k])-Decimal(precise['center'][k])) for k in ['radius','ZY_over_kappa','normalization_free_ratio'])
    check('high_precision_20_vs_40_level_check',high_precision_cutoff_difference<Decimal('1e-55'),str(high_precision_cutoff_difference))
    tail_bound=heat_value_tail_bound(nodes6)
    check('uniform_heat_value_tail_bound_below_1e_220',
          max(tail_bound[k] for k in ['P_absolute','J_absolute','T_absolute'])<1e-220,
          tail_bound)
    rows=[]
    for t in np.linspace(float(LOWER5),float(UPPER5),1001):
        a,w,dw=profile(5,t)
        row=dict(t=float(t),**solve_profile(a,w,dw))
        row['first_derivative_at_zero']=float(fp_zero)+float(fp_slope)*t
        rows.append(row)
    check('tracked_branch_curvature_positive_on_1001_point_grid',min(x['potential_curvature'] for x in rows)>0)
    check('gauge_coefficient_increases_on_grid',min(np.diff([x['ZY_over_kappa'] for x in rows]))>0)
    check('normalization_free_ratio_increases_on_grid',min(np.diff([x['normalization_free_ratio'] for x in rows]))>0)
    check('implicit_ratio_derivative_positive_on_grid',min(x['dlog_ratio_dt'] for x in rows)>0)
    check('interior_mixture_weights_positive',min(x['min_weight'] for x in rows[1:-1])>0)
    decimal_float_errors={}
    for label,t in [('lower_limit',float(LOWER5)),('source_minus',-1.),('center',0.),('source_plus',1.),('upper_limit',2.)]:
        actual=solve_profile(*profile(5,t))
        err=max(abs(actual[k]-float(precise[label][k])) for k in ['radius','ZY_over_kappa','normalization_free_ratio'])
        decimal_float_errors[label]=err
    check('independent_decimal_newton_vs_scipy_brent',max(decimal_float_errors.values())<1e-12,decimal_float_errors)
    center=solve_profile(*profile(5,0.))
    dt=1e-3
    qplus=solve_profile(*profile(5,dt))['normalization_free_ratio']
    qminus=solve_profile(*profile(5,-dt))['normalization_free_ratio']
    central_difference=(math.log(qplus)-math.log(qminus))/(2*dt)
    check('implicit_derivative_vs_independent_centered_difference',abs(central_difference-center['dlog_ratio_dt'])<1e-10)
    sixminus=precise['six_first'];sixplus=precise['six_second']
    dz6=float(sixplus['ZY_over_kappa'])-float(sixminus['ZY_over_kappa'])
    check('six_node_equal_first_derivative_still_changes_coupling',abs(dz6)>1e-8)
    # Reconstruct an unknown family parameter from f'(0), without a physical measurement.
    inferred=[]
    for t in [F(-3),F(-1),F(0),F(1),F(19,10)]:
        datum=-sum(a*w for a,w in zip(nodes5,fraction_weights(5,t)))
        recovered=(datum-fp_zero)/fp_slope
        check('exact_first_derivative_inverse_'+str(t),recovered==t)
        inferred.append({'t':str(t),'profile_derivative':str(datum),'recovered_t':str(recovered)})
    with (HERE/'profile_family_scan.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    def relative_percent(a,b,key):return 100*(float(b[key])/float(a[key])-1)
    result={
        'status':'conditional mathematical continuation; no physical profile selected; no alpha prediction',
        'source':{'archive_source_catalog':'sources/source_catalog.json',
                  'archive_source_id':'A1','archive_filename':ARCHIVE.name,
                  'sha256':source_hash(),'physical_pdf_pages':[7592,7599],
                  'title':'T-1: A shared spectral-action normalization test','date':'2026-10-12'},
        'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
                       'decimal_precision':70,'tracked_root_bracket':[1.2,1.4]},
        'five_node_family':{'nodes':'a_j=(5269/8220) j, j=1,...,5','weights':'1/5+t*v_j/2560',
                           'v':V5,'strict_positive_weight_interval':[str(LOWER5),str(UPPER5)],
                           'closure_endpoints_have_nonnegative_weights':True,
                           'constraint_rank':4,'nullity':1,'extra_first_derivative_rank':5,
                           'first_derivative_intercept':str(fp_zero),'first_derivative_slope':str(fp_slope),
                           'mellin_m4_slope':str(m4_slope),'exact_inverse_examples':inferred},
        'high_precision_results':precise,
        'uniform_heat_value_tail_bound':tail_bound,
        'scan_summary':{'points':len(rows),'endpoint_gauge_span_percent':relative_percent(rows[0],rows[-1],'ZY_over_kappa'),
                        'endpoint_ratio_span_percent':relative_percent(rows[0],rows[-1],'normalization_free_ratio'),
                        'min_sampled_potential_curvature':min(x['potential_curvature'] for x in rows),
                        'min_sampled_dlog_ratio_dt':min(x['dlog_ratio_dt'] for x in rows),
                        'max_sampled_dlog_ratio_dt':max(x['dlog_ratio_dt'] for x in rows),
                        'center_derivatives':center,
                        'monotonicity_scope':'Numerical on the sampled tracked branch, not interval-certified global uniqueness.'},
        'six_node_counterexample':{'nodes':'a_j=(5269/8220) j, j=1,...,6',
                                  'weights':'b_j+t*v_j/7680; b=(1/5,1/5,1/5,1/5,1/5,0)',
                                  'v':V6,'t_pair':[1,2],
                                  'strict_positive_weight_interval':['0','1536/625'],
                                  'constraints':'f(0), m1, m2, m3, f_prime(0)',
                                  'matches_original_five_node_center_data':True,
                                  'exact_leading_data':list(map(str,leading_data(nodes6,w6minus))),
                                  'first_derivative':str(fp_zero),
                                  'second_derivative_slope':str(sum(a*a*F(v,7680) for a,v in zip(nodes6,V6))),
                                  'extra_second_derivative_rank':6,
                                  'rank':5,'nullity':1,'gauge_difference':dz6,
                                  'gauge_relative_difference_percent':relative_percent(sixminus,sixplus,'ZY_over_kappa'),
                                  'ratio_relative_difference_percent':relative_percent(sixminus,sixplus,'normalization_free_ratio')},
        'checks':checks,
        'not_established':['Physical choice of profile or kappa','Full quantum or Lorentzian consistency',
                           'Canonical radion kinetic term or radion mass','Full electroweak embedding and running',
                           'Global uniqueness of the stationary-radius branch',
                           'An experimental measurement or attainable sensitivity']}
    (HERE/'profile_identifiability_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks_passed':len(checks),'scan_summary':result['scan_summary'],
                      'six_node_counterexample':result['six_node_counterexample']},indent=2))
    make_plot(rows,precise)


def make_plot(rows,precise):
    os.environ.setdefault('MPLCONFIGDIR','/tmp/toe_em_matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    t=np.array([x['t'] for x in rows]);z=np.array([x['ZY_over_kappa'] for x in rows]);q=np.array([x['normalization_free_ratio'] for x in rows])
    fig,axs=plt.subplots(1,2,figsize=(10.4,4.1),layout='constrained')
    for ax,data,center,key,label in [(axs[0],z,float(precise['center']['ZY_over_kappa']),'ZY_over_kappa',r'$Z_Y/\kappa$'),
                                      (axs[1],q,float(precise['center']['normalization_free_ratio']),'normalization_free_ratio',r'$Z_Y/(M_4r_*)^2$')]:
        ax.plot(t,100*(data/center-1),color='#175e86',lw=2)
        for label0,tt in [('source_minus',-1),('source_plus',1)]:
            ax.scatter([tt],[100*(float(precise[label0][key])/center-1)],color='#c55924',zorder=5)
        ax.axhline(0,color='.65',lw=.7);ax.set_xlabel(r'Profile-family coordinate $t$')
        ax.set_ylabel('Change from t = 0 (%)');ax.set_title(label)
        ax.grid(alpha=.2)
    fig.suptitle('Same leading spectral moments, different exact couplings\nConditional five-exponential family; orange points are the archived pair',fontsize=11)
    fig.savefig(HERE/'spectral_profile_sensitivity.png',dpi=180)
    plt.close(fig)


if __name__=='__main__':
    main()
