"""Note 42 numerical/algebraic checks, not experimental validation."""
import hashlib
import math
from pathlib import Path
import unittest
import mpmath as mp
from scipy.integrate import dblquad
from scipy.special import kve, roots_genlaguerre
import heavy_quark_thermal as h
import finite_mass_quark_thermal as fm
import gluon_loop_thermal as g


def blob(path):
    b=Path(path).read_bytes()
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()


def mp_form(tau):
    with mp.workdps(60):
        t=mp.mpf(str(tau))
        if t<=1:
            f=mp.asin(mp.sqrt(t))**2
        else:
            b=mp.sqrt(1-1/t)
            f=-mp.mpf(1)/4*(mp.log((1+b)/(1-b))-mp.j*mp.pi)**2
        return complex(mp.mpf(3)/2*(t+(t-1)*f)/t**2)


def laguerre(T,pair,n=64):
    mi,mj,k=h.PAIRS[pair]; xi,xj=mi/T,mj/T; a=xi+xj; b=xi-xj
    nodes,weights=roots_genlaguerre(n,.5)
    pref=k*k/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj))
    acc=0.
    for w,weight in zip(nodes,weights):
        if w>h.W_CUT:
            continue  # Same finite window; negligible cut discontinuity, not Q>80.
        y=a+w; Q=T*y
        acc+=weight*y*y*math.sqrt((2*a+w)*(y*y-b*b))*g.current_weight(Q)*kve(1,y)/((Q*Q-h.MH*h.MH)**2+(h.MH*h.GH)**2)
    return float(pref*acc)


def ww_leading_width(Q):
    """Independent operator-basis LO terms in 2503.22169v2 (4),(5),(7).

    Heavy-top limit C1=-a/12,C2=1. Both b/c masses set to same MSbar
    value in Yukawa and propagator. Higher-order terms are NOT included.
    """
    a=h.alpha_s(Q)/math.pi; C1=-a/12; CACF=4.
    Dtt=CACF*Q**3/(2*math.pi*h.V**2)
    Dmixed=0.; Fbc=0j
    for q in ('b','c'):
        m=h.running_mass(q,Q); z=(Q/m)**2; beta=math.sqrt(1-4/z)
        u=4/z/(1+beta)**2; lu=math.log(u)
        Dmixed+=Q*m*m*CACF/(math.pi*h.V**2)*((z-4)/(8*z)*(lu*lu-math.pi**2)-.5)
        Fbc+=m*m*((1-4/z)*complex(lu,math.pi)**2-4)
    Dbc=CACF/(128*math.pi*h.V**2*Q)*abs(Fbc)**2
    return C1*C1*Dtt+C1*a*Dmixed+a*a*Dbc


class GluonLoopTests(unittest.TestCase):
    def test_01_inherited_note40_bytes(self):
        self.assertEqual(blob(h.__file__),'40d51657a26fb20851be2bafa0ea6b3efe05ddfb')

    def test_02_inherited_note41_bytes(self):
        self.assertEqual(blob(fm.__file__),'117fd5d3abb650f05334d8bff6f88115c63e09da')

    def test_03_reproduce_finite_mass_note41_effective(self):
        weights=h.equilibrium_weights(.5)
        v=sum(weights[p]*sum(fm.thermal_quark(.5,p,q)[0] for q in ('b','c')) for p in h.PAIRS)
        self.assertAlmostEqual(v/1.19805650413715e-14,1.,delta=2e-10)
        self.assertAlmostEqual(.75*fm.pole_coefficient((4.78/125.09)**2),-7.446648,delta=6e-7)

    def test_04_heavy_and_chiral_limits(self):
        self.assertEqual(g.form_factor(0),1+0j)
        self.assertAlmostEqual(g.form_factor(1e-8).real,1.,delta=3e-9)
        self.assertLess(abs(g.form_factor(1e12)),1e-9)

    def test_05_heavy_series_60_digit_check(self):
        for tau in (1e-12,1e-8,1e-5,9.99e-5,9.99e-4):
            self.assertLess(abs(g.form_factor(tau)-mp_form(tau)),2e-14)

    def test_06_full_form_factor_60_digit_check(self):
        for tau in (1e-4,1e-3,.003,.05,.7,1.,1.0001,2.,10.,100.,10000.):
            self.assertLess(abs(g.form_factor(tau)-mp_form(tau)),3e-12)

    def test_07_branch_point_and_imaginary_part(self):
        self.assertEqual(g.form_factor(1),1.5+0j)
        self.assertEqual(g.form_factor(.9).imag,0)
        self.assertGreater(g.form_factor(1.1).imag,0)
        self.assertLess(abs(g.form_factor(1+1e-9)-g.form_factor(1-1e-9)),1e-7)

    def test_08_independent_feynman_parameter_integral(self):
        # F=3 int_0^1 dx int_0^(1-x)dy (1-4xy)/(1-4 tau xy), tau<1.
        for tau in (.003,.05,.7):
            value,_=dblquad(lambda y,x:3*(1-4*x*y)/(1-4*tau*x*y),0,1,
                           lambda x:0,lambda x:1-x,epsabs=1e-11,epsrel=1e-11)
            self.assertAlmostEqual(value,g.form_factor(tau).real,delta=2e-11)

    def test_09_independent_Wang_operator_normalization(self):
        for Q in (20.,23.,40.,80.):
            width=Q*g.current_weight(Q,component='heavy_top_coherent')/(8*math.pi*h.V**2)
            self.assertAlmostEqual(ww_leading_width(Q)/width,1.,delta=3e-13)

    def test_10_published_width_normalization(self):
        for Q in (20.,40.,80.):
            amps=g.loop_amplitudes(Q)
            gamma=h.alpha_s(Q)**2*Q**3/(72*math.pi**3*h.V**2)*abs(sum(amps.values()))**2
            self.assertAlmostEqual(g.unit_higgs_width(Q)/gamma,1.,delta=3e-15)

    def test_11_spectral_cross_section_matching(self):
        Q=25.; s=Q*Q
        for mi,mj,k in h.PAIRS.values():
            lam=(s-(mi+mj)**2)*(s-(mi-mj)**2); D=(s-h.MH**2)**2+(h.MH*h.GH)**2
            direct=k*k*s*g.current_weight(Q)/(8*math.pi*D*math.sqrt(lam))
            via_width=h.V**2*k*k*Q*g.unit_higgs_width(Q)/(D*math.sqrt(lam))
            self.assertAlmostEqual(direct/via_width,1.,delta=3e-15)

    def test_12_signed_decomposition_reassembles_coherence(self):
        for Q in (20.,21.5,23.,40.,80.):
            c=g.components(Q)
            self.assertAlmostEqual(sum(c.values())/g.current_weight(Q),1.,delta=3e-14)
            self.assertAlmostEqual(sum(c[q+q] for q in g.FLAVORS)/g.current_weight(Q,component='incoherent'),1.,delta=3e-14)

    def test_13_positive_coherent_current(self):
        for scheme in ('MSbar','pole1'):
            for Q in (20,21.5,23,40,65,80):
                for scale in (.5,1.,2.):
                    self.assertGreater(g.current_weight(Q,scale,scheme),0.)

    def test_14_interference_is_signed_not_separate_widths(self):
        self.assertGreater(g.components(20)['tb'],0.)
        self.assertLess(g.components(23)['tb'],0.)
        self.assertLess(g.components(20)['tc'],0.)
        self.assertGreater(g.components(20)['bc'],0.)

    def test_15_running_mass_loop_convention(self):
        for scale in (.5,1.,2.):
            amps=g.loop_amplitudes(25.,scale)
            for q in ('b','c'):
                self.assertEqual(amps[q],g.form_factor((25/(2*h.running_mass(q,25*scale)))**2))

    def test_16_auxiliary_pole_input_conversion(self):
        self.assertAlmostEqual(g.auxiliary_pole_mass('b'),4.307173039825607,delta=2e-12)
        self.assertAlmostEqual(g.auxiliary_pole_mass('c'),1.271321673378413,delta=2e-12)

    def test_17_LO_scheme_shift_begins_at_alpha_cubed(self):
        Q=23.; m=3.; d=2.; errors=[]
        for a in (2e-5,1e-5):
            def rate(mass):
                return a*a*abs(1+g.form_factor((Q/(2*mass))**2))**2
            errors.append(abs(rate(m*(1+a*d))-rate(m)))
        self.assertAlmostEqual(errors[0]/errors[1],8.,delta=.003)

    def test_18_two_integration_variables_all_pairs(self):
        for p in h.PAIRS:
            self.assertAlmostEqual(g.thermal_gg(.5,p,method='Q')[0]/g.thermal_gg(.5,p)[0],1.,delta=2e-10)

    def test_19_laguerre_and_quadrature_order(self):
        for p in h.PAIRS:
            v=g.thermal_gg(.5,p)[0]
            for n in (32,64):
                self.assertAlmostEqual(laguerre(.5,p,n)/v,1.,delta=2e-9)

    def test_20_finite_window_sensitivity(self):
        for p in h.PAIRS:
            v=g.thermal_gg(.5,p)[0]
            for cut in (60.,100.):
                self.assertAlmostEqual(g.thermal_gg(.5,p,cut=cut)[0]/v,1.,delta=2e-10)

    def test_21_lower_temperature(self):
        for p in h.PAIRS:
            v=g.thermal_gg(1/3,p)[0]
            self.assertGreater(v,0.)
            self.assertAlmostEqual(g.thermal_gg(1/3,p,method='Q')[0]/v,1.,delta=2e-10)

    def test_22_pair_numerical_regressions(self):
        refs={'11':6.234892739296664e-17,'12':6.244685637049902e-17,'22':6.275420642867611e-17}
        for p,ref in refs.items():
            self.assertAlmostEqual(g.thermal_gg(.5,p)[0]/ref,1.,delta=2e-10)

    def test_23_integrated_decomposition(self):
        for p in h.PAIRS:
            total=sum(g.thermal_gg(.5,p,component=c)[0] for c in g.COMPONENTS)
            self.assertAlmostEqual(total/g.thermal_gg(.5,p)[0],1.,delta=2e-10)

    def test_24_effective_scan_and_scope(self):
        s=g.summary()
        refs={'central':6.236081886931395e-17,'mu_half':9.776010056896179e-17,
              'mu_double':4.275780622827688e-17,'pole1_diagnostic':1.0702670867584023e-16}
        for name,ref in refs.items():
            self.assertAlmostEqual(s['variants'][name]['conditional_effective_GeV_minus2']/ref,1.,delta=2e-10)
        for key in ('NLO_gg_computed','light_quark_loops_included','Q_above_80_included',
                    'chemical_equilibrium_established','relic_density_computed','Omnes_data_acquired_in_this_step'):
            self.assertFalse(s[key])

    def test_25_analytic_cap_and_finite_remainder(self):
        cap=g.domain_cap()
        for scheme in ('MSbar','pole1'):
            for Q in (20,23,40,80):
                for scale in (.5,1.,2.):
                    self.assertLess(g.current_weight(Q,scale,scheme),cap)
        for p in h.PAIRS:
            bound=g.remainder_to_80(.5,p)
            self.assertGreater(bound,0.)
            self.assertLess(bound/g.thermal_gg(.5,p)[0],1e-20)

    def test_26_invalid_inputs(self):
        for tau in (-1.,math.nan,math.inf):
            with self.assertRaises(ValueError):g.form_factor(tau)
        for Q in (1.5,19.9,80.1,math.nan):
            with self.assertRaises(ValueError):g.current_weight(Q)
        for fun in (lambda:g.current_weight(20,scale=.49),lambda:g.current_weight(20,scheme='unknown'),
                    lambda:g.current_weight(20,component='unknown'),lambda:g.auxiliary_pole_mass('s'),
                    lambda:g.thermal_gg(1,'11'),lambda:g.thermal_gg(.5,'21'),
                    lambda:g.thermal_gg(.5,'11',cut=101),lambda:g.thermal_gg(.5,'11',method='bad')):
            with self.assertRaises(ValueError):fun()


if __name__=='__main__':unittest.main()
