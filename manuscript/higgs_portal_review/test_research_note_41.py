"""Note-41 algebra/numerics; checks do not establish the hypothetical fields."""
import hashlib
import math
from pathlib import Path
import unittest
import mpmath as mp
from scipy.special import roots_genlaguerre, kve
import finite_mass_quark_thermal as f
import heavy_quark_thermal as h


def mp_pole(r):
    with mp.workdps(60):
        r=mp.mpf(str(r)); b=mp.sqrt(1-4*r); p=(1-b)/(1+b)
        L=mp.log((1+b)/(1-b))
        A=(1+b*b)*(4*mp.polylog(2,p)+2*mp.polylog(2,-p)
           -3*L*mp.log(2/(1+b))-2*L*mp.log(b))
        A-=3*b*mp.log(4/(1-b*b))+4*b*mp.log(b)
        return float(mp.mpf(4)/3*(A/b+(3+34*b*b-13*b**4)*L/(16*b**3)
                                 +3*(7*b*b-1)/(8*b*b)))


def laguerre(T,pair,flavor,n=64):
    mi,mj,k=h.PAIRS[pair];xi,xj=mi/T,mj/T;a=xi+xj;b=xi-xj
    pref=k*k/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj))
    nodes,weights=roots_genlaguerre(n,.5)
    acc=0.
    for w,weight in zip(nodes,weights):
        if w>h.W_CUT:
            continue  # finite-window comparison; no extrapolation past Q=80
        y=a+w;Q=T*y
        acc+=weight*y*y*math.sqrt((2*a+w)*(y*y-b*b))*f.current_weight(Q,flavor)*kve(1,y)/((Q*Q-h.MH*h.MH)**2+(h.MH*h.GH)**2)
    return float(pref*acc)


class FiniteMassTests(unittest.TestCase):
    def test_inherited_code_exact_blob(self):
        b=Path(h.__file__).read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        self.assertEqual(digest,'40d51657a26fb20851be2bafa0ea6b3efe05ddfb')

    def test_published_on_shell_coefficient_table2(self):
        # Behring/Bizon 1911.11524 Table 2, mb=4.78, MH=125.09.
        self.assertAlmostEqual(.75*f.pole_coefficient((4.78/125.09)**2),
                               -7.446648,delta=6e-7)

    def test_dilogarithm_against_60_digit_evaluation(self):
        for r in (1e-7,1e-5,.001,.01,.03,.1):
            self.assertAlmostEqual(f.pole_coefficient(r),mp_pole(r),delta=6e-12)

    def test_massless_coefficient_and_scale_log(self):
        for scale in (.5,1.,2.):
            self.assertAlmostEqual(f.msbar_coefficient(1e-8,scale),
                                   17/3+4*math.log(scale),delta=8e-7)

    def test_independent_quadratic_mass_coefficient_minus40(self):
        # Imaginary part of hep-ph/9704436 Eq. (7).
        r=1e-6
        B=(1-4*r)**1.5*f.msbar_coefficient(r)
        self.assertAlmostEqual((B-17/3)/r,-40.,delta=3e-4)

    def test_independent_r4_series_all_scales(self):
        for scale in (.5,1.,2.):
            for r in (.001,.01,.03):
                B=(1-4*r)**1.5*f.msbar_coefficient(r,scale)
                self.assertAlmostEqual(B,f.expanded_spectral_b1(r,scale),delta=3e-5)

    def test_born_mass_derivative(self):
        for r in (.001,.01,.04):
            eps=1e-5
            F=lambda rr:rr*(1-4*rr)**1.5
            slope=(math.log(F(r*math.exp(2*eps)))-math.log(F(r*math.exp(-2*eps))))/(2*eps)
            self.assertAlmostEqual(slope,f.born_log_derivative(r),delta=2e-9)

    def test_mass_scheme_reexpansion_difference_is_second_order(self):
        r=.027;m=math.sqrt(r);d=f.mass_conversion_d(r)
        B=lambda m:m*m*(1-4*m*m)**1.5
        errors=[]
        for a in (2e-5,1e-5):
            M=m*(1+a*d)
            os=B(M)*(1+a*f.pole_coefficient(M*M))
            ms=B(m)*(1+a*f.msbar_coefficient(r))
            errors.append(abs((os-ms)/B(m)))
        self.assertAlmostEqual(errors[0]/errors[1],4.,delta=.003)
        self.assertLess(errors[1],2e-9)

    def test_yukawa_only_conversion_is_not_all_msbar(self):
        r=.03;d=f.mass_conversion_d(r)
        hybrid=f.pole_coefficient(r)+2*d
        expected=d*12*r/(1-4*r)
        self.assertAlmostEqual(hybrid-f.msbar_coefficient(r),expected,delta=2e-14)

    def test_finite_mass_scale_derivative_is_second_order(self):
        def slope(a0):
            def value(t):
                a=h.a_fixed_nf(20*math.exp(t/2),20,a0,5)
                m=3.3*h.mass_ratio(a,a0,5)
                r=(m/20)**2
                return m*m*(1-4*r)**1.5*(1+a*f.msbar_coefficient(r,math.exp(t/2)))
            eps=1e-3
            return abs((value(eps)-value(-eps))/(2*eps))
        self.assertAlmostEqual(slope(2e-5)/slope(1e-5),4.,delta=.02)

    def test_central_pair_totals(self):
        refs={'11':1.19493093749360e-14,'12':1.22265605388329e-14,'22':1.23602466498016e-14}
        for p,v in refs.items():
            value=sum(f.thermal_quark(.5,p,q)[0] for q in ('b','c'))
            self.assertAlmostEqual(value/v,1.,delta=2e-10)

    def test_two_variables_all_six(self):
        for p in h.PAIRS:
            for q in ('b','c'):
                a=f.thermal_quark(.5,p,q)[0];b=f.thermal_quark(.5,p,q,method='Q')[0]
                self.assertAlmostEqual(a/b,1.,delta=2e-9)

    def test_independent_laguerre_all_six(self):
        for p in h.PAIRS:
            for q in ('b','c'):
                self.assertAlmostEqual(laguerre(.5,p,q)/f.thermal_quark(.5,p,q)[0],1.,delta=2e-9)

    def test_conditional_effective_and_scale_scan(self):
        weights=h.equilibrium_weights(.5)
        for scale,expected in ((.5,1.28623515019012e-14),(1.,1.19805650413715e-14),(2.,1.11684429461212e-14)):
            v=sum(weights[p]*sum(f.thermal_quark(.5,p,q,scale)[0] for q in ('b','c')) for p in h.PAIRS)
            self.assertAlmostEqual(v/expected,1.,delta=2e-10)

    def test_preserve_note40_comparators(self):
        weights=h.equilibrium_weights(.5)
        for phase,expected in ((False,1.40159797221544e-14),(True,1.20791269962841e-14)):
            v=sum(weights[p]*sum(h.thermal_quark(.5,p,q,born_phase=phase)[0] for q in ('b','c')) for p in h.PAIRS)
            self.assertAlmostEqual(v/expected,1.,delta=2e-10)

    def test_finite_window_convergence(self):
        for q in ('b','c'):
            a=f.thermal_quark(.5,'11',q,cut=90)[0]
            for cut in (60,100):
                self.assertAlmostEqual(f.thermal_quark(.5,'11',q,cut=cut)[0]/a,1.,delta=2e-9)

    def test_lower_temperature(self):
        for q in ('b','c'):
            a=f.thermal_quark(1/3,'12',q)[0]
            b=f.thermal_quark(1/3,'12',q,method='Q')[0]
            self.assertGreater(a,0.)
            self.assertAlmostEqual(a/b,1.,delta=2e-9)

    def test_positive_currents_and_analytic_cap(self):
        cap=f.hard_domain_current_cap()
        self.assertGreater(cap,0.)
        for Q in (20,21.5,23,40,65,80):
            for scale in (.5,1.,2.):
                for q in ('b','c'):
                    val=f.current_weight(Q,q,scale)
                    self.assertGreater(val,0.)
                    self.assertLess(val,cap)

    def test_remainder_only_to_domain_edge(self):
        for p in h.PAIRS:
            bound=f.within_domain_remainder_bound(.5,p)
            self.assertGreater(bound,0.)
            self.assertLess(bound/f.thermal_quark(.5,p,'c')[0],1e-20)

    def test_not_phase_only_diagnostic(self):
        for q in ('b','c'):
            self.assertLess(f.current_weight(20,q),h.current_weight(20,q,born_phase=True))

    def test_invalid_ratio(self):
        for r in (-1,0,.25,.3,math.inf,math.nan):
            with self.assertRaises(ValueError):f.pole_coefficient(r)
        with self.assertRaises(ValueError):f.msbar_coefficient(.01,0)

    def test_invalid_current_domain(self):
        for Q in (1.5,19.9,80.1,math.nan):
            with self.assertRaises(ValueError):f.current_weight(Q,'b')
        for scale in (0,.49,2.1,math.inf):
            with self.assertRaises(ValueError):f.current_weight(20,'b',scale)
        with self.assertRaises(ValueError):f.current_weight(20,'s')

    def test_invalid_thermal_domain(self):
        for fun in (lambda:f.thermal_quark(1,'11','b'),
                    lambda:f.thermal_quark(.5,'21','b'),
                    lambda:f.thermal_quark(.5,'11','b',cut=101),
                    lambda:f.thermal_quark(.5,'11','b',method='unknown')):
            with self.assertRaises(ValueError):fun()

    def test_summary_does_not_claim_missing_physics(self):
        s=f.summary()
        self.assertFalse(s['Q_above_80_included'])
        self.assertFalse(s['chemical_equilibrium_established'])
        self.assertFalse(s['Omnes_data_acquired_in_this_step'])
        self.assertFalse(s['relic_density_computed'])


if __name__=='__main__':unittest.main()
