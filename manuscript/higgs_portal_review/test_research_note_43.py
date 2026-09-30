"""Note 43: source, phase-space and numerical checks; not empirical validation."""
import hashlib
import math
from pathlib import Path
import unittest
import mpmath as mp
import numpy as np
from scipy.integrate import quad
from scipy.special import roots_genlaguerre, kve
import heavy_quark_thermal as h
import gluon_loop_thermal as g
import top_operator_nlo as t


def direct_real_width_ratio(Q, m, alpha):
    """Three-body phase-space integral with independently written tensor norm.

    Set the local Hgg tensor coupling to one; it cancels in the width ratio.
    NA=8, TR=1/2; Gamma_gg uses the identical-final-state factor 1/2.
    """
    NA, TR = 8., .5
    gamma2 = NA*Q**3/(64*math.pi)
    gs2 = 4*math.pi*alpha
    def integrand(u):
        z = 4*m*m*math.exp(u)  # pair invariant mass squared
        beta = math.sqrt(max(0.,1-4*m*m/z))
        def angle(c):
            amp2 = gs2*TR*NA*(Q*Q-z)**2/(2*z)*(1+c*c+4*m*m/z*(1-c*c))
            phase = 1/(2*Q)/(2*math.pi)*(Q*Q-z)/(8*math.pi*Q*Q)*beta/(16*math.pi)
            return amp2*phase*z  # dz=z du
        return quad(angle,-1,1,epsabs=1e-25,epsrel=1e-12)[0]
    return quad(integrand,0,math.log(Q*Q/(4*m*m)),epsabs=1e-25,epsrel=3e-11)[0]/gamma2


def laguerre(T, pair, part, n=64):
    mi,mj,k = h.PAIRS[pair]
    xi,xj = mi/T,mj/T
    a,b = xi+xj,xi-xj
    nodes, weights = roots_genlaguerre(n,.5)
    acc = 0.
    for w,weight in zip(nodes,weights):
        if w > h.W_CUT:
            continue  # finite-domain comparison, not infinity extrapolation
        y = a+w; Q=T*y
        acc += weight*y*y*math.sqrt((2*a+w)*(y*y-b*b))*t.current_weight(Q,part)*kve(1,y)/((Q*Q-h.MH*h.MH)**2+(h.MH*h.GH)**2)
    return float(k*k*acc/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj)))


class TopOperatorNLOTests(unittest.TestCase):
    def test_inherited_source_identities(self):
        for name,sha in {
            'heavy_quark_thermal.py':'40d51657a26fb20851be2bafa0ea6b3efe05ddfb',
            'finite_mass_quark_thermal.py':'117fd5d3abb650f05334d8bff6f88115c63e09da',
            'gluon_loop_thermal.py':'c49c6fab4baa2d9c01c64f9fd8c2fdb7f018d50c'}.items():
            b=Path(__file__).with_name(name).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha)

    def test_source_eq4_plus_wilson_matching(self):
        for Q in (20.,40.,80.):
            for s in (.5,1.,2.):
                m=t.masses(Q,s)
                L=math.log(s*s);lb=math.log(Q*Q/m['b']**2);lc=math.log(Q*Q/m['c']**2)
                # 2503.22169v2 Eq. (4), CA=3, nl=3; add 2*(11/4).
                source = (-lb/3-lc/3-2*L/3)+3*(11*L/6+73/12)+3*(-L/3-7/6)+11/2
                self.assertAlmostEqual(source,t.coefficient_veto(Q,m['b'],m['c'],s),delta=2e-14)

    def test_wilson_squared_contributes_eleven_halves(self):
        eps=1e-6
        derivative=((1+11*eps/4)**2-(1-11*eps/4)**2)/(2*eps)
        self.assertAlmostEqual(derivative,11/2,delta=2e-10)

    def test_scale_log_matches_five_flavor_beta(self):
        a=t.coefficient_veto(20,3.3,.74,2)-t.coefficient_veto(20,3.3,.74,1)
        self.assertAlmostEqual(a/math.log(4),2*h.rg_coefficients(5)[0],delta=2e-15)

    def test_LO_recovers_note42_heavy_top(self):
        for pair in h.PAIRS:
            a=t.thermal(.5,pair,'LO')[0]
            b=g.thermal_gg(.5,pair,component='heavy_top_only')[0]
            self.assertAlmostEqual(a/b,1.,delta=3e-13)

    def test_unit_width_normalization(self):
        Q=23.;a=h.alpha_s(Q)
        width=Q*t.current_weight(Q,'LO')/(8*math.pi*h.V**2)
        self.assertAlmostEqual(width/(a*a*Q**3/(72*math.pi**3*h.V**2)),1.,delta=3e-15)

    def test_real_integral_closed_form_vs_z_quadrature(self):
        for r in (1e-8,1e-4,.001,.01,.046,.1,.2,.249):
            self.assertAlmostEqual(t.real_integral(r)/t.real_integral_z(r),1.,delta=3e-10)

    def test_real_integral_independent_beta_variable(self):
        for r in (.0001,.001,.01,.04,.1,.2):
            self.assertAlmostEqual(t.real_integral(r)/t.real_integral_beta(r),1.,delta=3e-10)

    def test_real_integral_high_precision(self):
        with mp.workdps(60):
            for raw in ('0.001','0.01','0.046','0.2','0.249'):
                r=mp.mpf(raw);B=mp.sqrt(1-4*r)
                exact=(1-18*r*r+8*r**3)*mp.log((1+B)/(1-B))-(mp.mpf('3.5')+r)*B**3
                self.assertAlmostEqual(t.real_integral(float(r))/float(exact),1.,delta=3e-10)

    def test_threshold_scaling_beta_nine(self):
        B=.01;r=(1-B*B)/4
        self.assertAlmostEqual(t.real_integral(r)/B**9,16/105,delta=5e-5)

    def test_positive_monotonically_decreasing_real_integral(self):
        vals=[t.real_integral(r) for r in (.001,.01,.03,.1,.2,.249)]
        self.assertTrue(all(x>0 for x in vals))
        self.assertTrue(all(a>b for a,b in zip(vals,vals[1:])))

    def test_real_current_analytic_bound(self):
        for r in (1e-8,.001,.01,.1,.249):
            self.assertLess(t.real_integral(r),math.log(1/(4*r)))

    def test_massive_real_width_from_three_body_phase_space(self):
        for Q,m in ((20.,3.3),(23.,.74),(50.,4.3)):
            alpha=.15
            got=direct_real_width_ratio(Q,m,alpha)
            expected=alpha/(3*math.pi)*t.real_integral((m/Q)**2)
            self.assertAlmostEqual(got/expected,1.,delta=3e-11)

    def test_angular_trace_factor(self):
        for r in (.001,.1,.2):
            angular=quad(lambda c:(3/8)*(1+c*c+4*r*(1-c*c)),-1,1)[0]
            self.assertAlmostEqual(angular,1+2*r,delta=4e-16)

    def test_collinear_constant_minus_seven_halves(self):
        for r in (1e-10,1e-12,1e-14):
            self.assertAlmostEqual(t.real_minus_collinear_log(r),-3.5,delta=2e-8)

    def test_inclusive_massless_limit_matches_spira_eq26(self):
        for scale in (.5,1.,2.):
            Q=20.;m=Q*1e-6
            expected=95/4-7*5/6+(33-2*5)*math.log(scale*scale)/6
            self.assertAlmostEqual(t.coefficient_inclusive(Q,m,m,scale),expected,delta=2e-10)

    def test_veto_mass_log_not_a_finite_massless_prediction(self):
        self.assertLess(t.coefficient_veto(20,.001,.001),t.coefficient_veto(20,.01,.01))

    def test_NLO_inclusive_equals_veto_plus_real_cuts(self):
        for Q in (20.,30.,80.):
            for scheme in ('MSbar','pole1'):
                c=t.current_components(Q,scheme=scheme)
                self.assertAlmostEqual((c['NLO_veto']+c['real_b']+c['real_c'])/c['NLO_inclusive'],1.,delta=6e-15)

    def test_NLO_scale_dependence_starts_at_alpha_four(self):
        Q=20.;mb,mc=3.3,.74
        def slope(a0):
            def val(L):
                a=h.a_fixed_nf(Q*math.exp(L/2),Q,a0,5)
                E=t.coefficient_inclusive(Q,mb,mc,math.exp(L/2))
                return a*a*(1+a*E)
            eps=1e-3
            return abs((val(eps)-val(-eps))/(2*eps))
        self.assertAlmostEqual(slope(2e-4)/slope(1e-4),16.,delta=.03)

    def test_mass_scheme_shift_starts_at_alpha_four(self):
        Q=20.;mb,mc=3.3,.74
        def shift(a):
            masses=[m*(1+a*(4/3+2*math.log(Q/m))) for m in (mb,mc)]
            return abs(a**3*(t.coefficient_veto(Q,*masses)-t.coefficient_veto(Q,mb,mc)))
        self.assertAlmostEqual(shift(2e-5)/shift(1e-5),16.,delta=.003)

    def test_central_pair_reference_values(self):
        refs={'11':6.96010267867646e-17,'12':7.86276195635416e-17,'22':8.75315607071434e-17}
        for p,ref in refs.items():
            self.assertAlmostEqual(t.thermal(.5,p)[0]/ref,1.,delta=2e-11)

    def test_independent_thermal_variables_all_parts(self):
        for pair in h.PAIRS:
            for part in ('NLO_veto','real_b','real_c','NLO_inclusive'):
                a=t.thermal(.5,pair,part)[0];b=t.thermal(.5,pair,part,method='Q')[0]
                self.assertAlmostEqual(a/b,1.,delta=2e-10)

    def test_independent_laguerre_representation(self):
        for pair in h.PAIRS:
            for part in ('NLO_inclusive','real_b','real_c'):
                self.assertAlmostEqual(laguerre(.5,pair,part)/t.thermal(.5,pair,part)[0],1.,delta=2e-9)

    def test_window_and_lower_temperature(self):
        for T in (1/3,.5):
            for part in ('NLO_inclusive','real_c'):
                a=t.thermal(T,'12',part)[0]
                for cut in (60.,100.):
                    self.assertAlmostEqual(t.thermal(T,'12',part,cut=cut)[0]/a,1.,delta=2e-10)

    def test_current_cap_not_sample_max_and_positive_remainder(self):
        cap=t.current_cap()
        for Q in (20.,40.,80.):
            for scale in (.5,1.,2.):
                for scheme in ('MSbar','pole1'):
                    for part,val in t.current_components(Q,scale,scheme).items():
                        self.assertLess(abs(val),cap)
        for p in h.PAIRS:
            bound=t.remainder_to_80(.5,p)
            self.assertGreater(bound,0.)
            self.assertLess(bound/t.thermal(.5,p)[0],1e-20)

    def test_light_loop_square_is_coherent_not_incoherent(self):
        weights=h.equilibrium_weights(.5)
        exact=sum(weights[p]*h.thermal_from_weight(.5,p,lambda Q:
              h.alpha_s(Q)**2*Q**2/(9*math.pi**2)*abs(sum(g.loop_amplitudes(Q)[q] for q in ('b','c')))**2)[0] for p in h.PAIRS)
        parts=sum(weights[p]*sum(g.thermal_gg(.5,p,component=c)[0] for c in ('bb','cc','bc')) for p in h.PAIRS)
        self.assertAlmostEqual(exact/parts,1.,delta=2e-12)

    def test_flags_and_conditional_effective_values(self):
        s=t.summary();c=s['variants']['central']['conditional_effective_GeV_minus2']
        self.assertAlmostEqual(c['NLO_inclusive']/7.06335310504938e-17,1.,delta=2e-11)
        self.assertAlmostEqual(c['NLO_veto']/6.82936482528463e-17,1.,delta=2e-11)
        self.assertAlmostEqual(s['note42_O2_square_fraction_of_LO_gg'],.4261107318622,delta=2e-12)
        for key in ('full_coherent_NLO_gg_computed','NLO_O1_O2_computed','NLO_O2_square_computed',
                    'finite_top_NLO_computed','chemical_equilibrium_established','relic_density_computed',
                    'Q_above_80_included','Omnes_data_acquired_in_this_step'):
            self.assertIs(s[key],False)

    def test_invalid_inputs_rejected(self):
        for r in (0,-1,.25,math.inf,math.nan):
            with self.assertRaises(ValueError):t.real_integral(r)
        for call in (lambda:t.current_weight(1.5),lambda:t.current_weight(81),
                     lambda:t.current_weight(20,scale=.4),lambda:t.current_weight(20,scheme='unknown'),
                     lambda:t.current_weight(20,part='full_NLO'),lambda:t.coefficient_veto(20,-3,.74),
                     lambda:t.thermal(1.,'11'),lambda:t.thermal(.5,'21'),
                     lambda:t.thermal(.5,'11',cut=101)):
            with self.assertRaises(ValueError):call()


if __name__=='__main__':unittest.main()
