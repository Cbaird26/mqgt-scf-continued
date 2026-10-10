"""Note 45: algebra/numerics and explicit unknown-hard-coefficient checks.

Synthetic RG and polarization fixtures are labeled and are NOT QCD data.
"""
import hashlib
import math
from pathlib import Path
import unittest
import mpmath as mp
from scipy.special import roots_genlaguerre, kve
import coherent_bc_rg as r
import heavy_quark_thermal as h
import gluon_loop_thermal as g


def mp_F(rr):
    beta=mp.sqrt(1-4*rr)
    ell=mp.log((1+beta)/(1-beta))
    f=-mp.mpf(1)/4*(ell-mp.j*mp.pi)**2
    return 6*rr*(1+(1-4*rr)*f)


def one_loop_flow(t, a0, rb0=.025, rc0=.001):
    a=a0/(1+r.BETA0*a0*t)
    factor=(a/a0)**(2/r.BETA0)
    return a,rb0*factor,rc0*factor


def rg_slope(a0, include_log, finite_choice=0.):
    # Artificial finite matching term, not evaluated QCD.
    def current(t):
        a,rb,rc=one_loop_flow(t,a0)
        B=r.born_data(rb,rc)['B']['coherent']
        K=r.required_log_coefficient(rb,rc)['coherent']
        return a*a*B+a**3*(finite_choice*B+(t*K if include_log else 0.))
    # At L=0 and C_fin=0 the one-loop residual vanishes identically;
    # test at nonzero L rather than taking a meaningless ratio of zeros.
    dt=.002; center=.4
    return abs((current(center+dt)-current(center-dt))/(2*dt))


def laguerre(T,pair,part,component,n=64):
    mi,mj,k=h.PAIRS[pair];xi,xj=mi/T,mj/T;a=xi+xj;b=xi-xj
    pref=k*k/(32*math.pi*xi**2*xj**2*kve(2,xi)*kve(2,xj))
    nodes,weights=roots_genlaguerre(n,.5)
    total=0.
    for w,weight in zip(nodes,weights):
        if w>90:continue
        y=a+w;Q=T*y
        total+=weight*y*y*math.sqrt((2*a+w)*(y*y-b*b))*r.current_terms(Q)[component][part]*kve(1,y)/((Q*Q-h.MH*h.MH)**2+(h.MH*h.GH)**2)
    return float(pref*total)


class CoherentBCRGTests(unittest.TestCase):
    def test_inherited_sources_exact_blobs(self):
        expected={h.__file__:'40d51657a26fb20851be2bafa0ea6b3efe05ddfb',
                  g.__file__:'c49c6fab4baa2d9c01c64f9fd8c2fdb7f018d50c'}
        for path,sha in expected.items():
            b=Path(path).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha)

    def test_amplitude_recovers_note42(self):
        for rr in (1e-7,1e-4,.001,.025,.1):
            F,_=r.form_and_mass_derivative(rr)
            self.assertLess(abs(F-g.form_factor(1/(4*rr))),2e-14)

    def test_amplitude_and_derivative_70_digits(self):
        with mp.workdps(70):
            for val in ('1e-7','.001','.025','.1','.24'):
                rr=mp.mpf(val)
                F,D=r.form_and_mass_derivative(float(rr))
                Fmp=mp_F(rr);Dmp=2*rr*mp.diff(mp_F,rr)
                self.assertLess(abs(F-complex(Fmp)),2e-13)
                self.assertLess(abs(D-complex(Dmp)),2e-13)

    def test_born_components_sum(self):
        for kb,kc in ((1,1),(1,-1),(0,1),(2,-.7)):
            d=r.born_data(.02,.001,kb,kc)
            for key in ('B','D_b','D_c'):
                self.assertAlmostEqual(sum(d[key][c] for c in ('bb','cc','bc')),d[key]['coherent'],delta=3e-14)

    def test_mass_derivatives_by_independent_difference(self):
        rb,rc=.02,.001;eps=1e-5;d=r.born_data(rb,rc)
        for c in r.COMPONENTS:
            db=(r.born_data(rb*math.exp(2*eps),rc)['B'][c]-r.born_data(rb*math.exp(-2*eps),rc)['B'][c])/(2*eps)
            dc=(r.born_data(rb,rc*math.exp(2*eps))['B'][c]-r.born_data(rb,rc*math.exp(-2*eps))['B'][c])/(2*eps)
            self.assertAlmostEqual(db,d['D_b'][c],delta=3e-9)
            self.assertAlmostEqual(dc,d['D_c'][c],delta=3e-9)

    def test_coherent_logs_include_interference_derivative(self):
        k=r.required_log_coefficient(.02,.001)
        self.assertAlmostEqual(k['coherent']-k['bb']-k['cc'],k['bc'],delta=3e-14)
        self.assertGreater(abs(k['bc']),.01)

    def test_exact_cancellation_is_nonsingular(self):
        d=r.born_data(.02,.02,1,-1)
        k=r.required_log_coefficient(.02,.02,1,-1)
        self.assertEqual(d['B']['coherent'],0.)
        self.assertEqual(k['coherent'],0.)
        self.assertEqual(r.scheme_shift(.02,.02,1.,1.,-1.)['coherent'],0.)

    def test_sign_and_quadratic_scaling(self):
        a=r.required_log_coefficient(.02,.001,1,1)
        b=r.required_log_coefficient(.02,.001,-1,-1)
        c=r.required_log_coefficient(.02,.001,3,3)
        for k in r.COMPONENTS:
            self.assertEqual(a[k],b[k])
            self.assertAlmostEqual(c[k],9*a[k],delta=2e-13)

    def test_zero_couplings_have_zero_terms(self):
        out=r.current_terms(20,kb=0,kc=0)
        for comp in out.values():
            self.assertTrue(all(v==0 for v in comp.values()))

    def test_rg_formula_cancels_leading_scale_derivative(self):
        d=r.born_data(.025,.001);K=r.required_log_coefficient(.025,.001)
        for c in r.COMPONENTS:
            derivative=-2*r.BETA0*d['B'][c]-d['D_b'][c]-d['D_c'][c]
            self.assertAlmostEqual(derivative+K[c],0.,delta=2e-14)

    def test_uncorrected_rg_slope_is_cubic(self):
        self.assertAlmostEqual(rg_slope(2e-4,False)/rg_slope(1e-4,False),8.,delta=.005)

    def test_log_restored_rg_slope_is_quartic(self):
        for fixture in (0.,1.,-3.):
            self.assertAlmostEqual(rg_slope(2e-4,True,fixture)/rg_slope(1e-4,True,fixture),16.,delta=.03)

    def test_os_to_msbar_remainder_begins_at_a4(self):
        rb,rc=.025,.001
        for scale in (.5,1.,2.):
            errors=[]
            for a in (2e-5,1e-5):
                db=4/3+2*math.log(scale)-math.log(rb)
                dc=4/3+2*math.log(scale)-math.log(rc)
                shifted=r.born_data(rb*(1+a*db)**2,rc*(1+a*dc)**2)['B']['coherent']
                born=r.born_data(rb,rc)['B']['coherent']
                matched=born+a*r.scheme_shift(rb,rc,scale)['coherent']
                errors.append(abs(a*a*(shifted-matched)))
            self.assertAlmostEqual(errors[0]/errors[1],16.,delta=.01)

    def test_scheme_log_matches_rg_required_coefficient(self):
        rb,rc=.025,.001;d=r.born_data(rb,rc);eps=.01
        plus=r.scheme_shift(rb,rc,math.exp(eps/2))
        minus=r.scheme_shift(rb,rc,math.exp(-eps/2))
        K=r.required_log_coefficient(rb,rc)
        for c in r.COMPONENTS:
            slope=(plus[c]-minus[c])/(2*eps)
            self.assertAlmostEqual(2*r.BETA0*d['B'][c]+slope,K[c],delta=3e-13)

    def test_hybrid_loop_only_conversion(self):
        rb,rc=.025,.001;eps=1e-5
        Fb,Db=r.form_and_mass_derivative(rb);Fc,Dc=r.form_and_mass_derivative(rc)
        A=Fb+Fc
        # Independently rescale loop masses while holding Yukawa masses fixed.
        def hybrid(t):
            return abs(math.exp(-t)*(r.form_and_mass_derivative(rb*math.exp(2*t))[0]+r.form_and_mass_derivative(rc*math.exp(2*t))[0]))**2
        numeric=(hybrid(eps)-hybrid(-eps))/(2*eps)
        expected=2*((Db+Dc-A)*A.conjugate()).real
        self.assertAlmostEqual(numeric,expected,delta=3e-9)
        data=r.born_data(rb,rc)
        self.assertAlmostEqual(expected,data['D_b']['coherent']+data['D_c']['coherent']-2*data['B']['coherent'],delta=2e-14)

    def test_hybrid_and_os_scale_rules_reach_same_msbar_log(self):
        d=r.born_data(.025,.001)
        B=d['B']['coherent'];D=d['D_b']['coherent']+d['D_c']['coherent']
        self.assertAlmostEqual((2*r.BETA0+2)*B+(D-2*B),r.required_log_coefficient(.025,.001)['coherent'],delta=2e-14)

    def test_coherent_LO_thermal_recovers_prior_component_sum(self):
        for p in h.PAIRS:
            v=r.thermal(.5,p)[0]
            old=sum(g.thermal_gg(.5,p,component=c)[0] for c in ('bb','cc','bc'))
            self.assertAlmostEqual(v/old,1.,delta=3e-11)

    def test_all_components_two_thermal_variables(self):
        for p in h.PAIRS:
            for c in r.COMPONENTS:
                for k in ('LO','required_NLO_log_slope','OS_to_MSbar_finite_shift'):
                    a=r.thermal(.5,p,k,c)[0];b=r.thermal(.5,p,k,c,method='Q')[0]
                    self.assertAlmostEqual(a/b,1.,delta=3e-9)

    def test_independent_gauss_laguerre(self):
        for p in h.PAIRS:
            for k in ('LO','required_NLO_log_slope','OS_to_MSbar_finite_shift'):
                a=r.thermal(.5,p,k)[0];b=laguerre(.5,p,k,'coherent')
                self.assertAlmostEqual(a/b,1.,delta=3e-9)

    def test_temperature_and_window_stability(self):
        for T in (1/3,.4,.5):
            a=r.thermal(T,'12','required_NLO_log_slope')[0]
            self.assertGreater(a,0.)
            for cut in (60,100):
                b=r.thermal(T,'12','required_NLO_log_slope',cut=cut)[0]
                self.assertAlmostEqual(a/b,1.,delta=3e-9)

    def test_equilibrium_weighting_is_only_conditional(self):
        out=r.summary();e=out['conditional_effective']['coherent']
        self.assertAlmostEqual(e['LO']/2.6572614167929948e-17,1.,delta=3e-11)
        self.assertAlmostEqual(e['required_NLO_log_slope']/8.16337116395311e-18,1.,delta=3e-11)
        self.assertAlmostEqual(e['OS_to_MSbar_finite_shift']/1.727042936817734e-17,1.,delta=3e-11)
        self.assertFalse(out['chemical_equilibrium_established'])

    def test_finite_boundary_is_required(self):
        with self.assertRaisesRegex(ValueError,'absent'):
            r.finite_nlo_current(20,None)
        with self.assertRaises(ValueError):
            r.finite_nlo_current(20,lambda rb,rc:math.nan)

    def test_rg_does_not_determine_finite_boundary(self):
        # Two synthetic finite coefficients; not competing physics predictions.
        one=r.finite_nlo_current(20,lambda rb,rc:0.)
        two=r.finite_nlo_current(20,lambda rb,rc:1.)
        a=h.alpha_s(20)/math.pi
        self.assertAlmostEqual(two-one,400/9*a**3,delta=1e-16)
        self.assertNotEqual(one,two)

    def test_polarization_of_actual_LO_form_factor(self):
        rb,rc=.02,.001
        vals={s:r.born_data(rb,rc,kb,kc)['B']['coherent']
              for s,kb,kc in [('00',0,0),('10',1,0),('01',0,1),('11',1,1),('1-1',1,-1)]}
        result=r.polarize(vals);expected=r.born_data(rb,rc)['B']
        for c in result:self.assertAlmostEqual(result[c],expected[c],delta=2e-14)

    def test_polarization_works_on_signed_NLO_fixture(self):
        # Signed coefficient matrix fixture, not a physical NLO output.
        f=lambda b,c:2*b*b-3*c*c+7*b*c
        vals={s:f(b,c) for s,b,c in [('00',0,0),('10',1,0),('01',0,1),('11',1,1),('1-1',1,-1)]}
        self.assertEqual(r.polarize(vals),{'bb':2,'cc':-3,'bc':7})

    def test_incoherent_input_fails_interference_check(self):
        # Mixing coherent plus probe with an incoherent minus probe is invalid.
        with self.assertRaises(ValueError):
            r.polarize({'00':0,'10':2,'01':3,'11':8,'1-1':5})

    def test_polarization_rejects_unsubtracted_other_sector(self):
        with self.assertRaises(ValueError):
            r.polarize({'00':1,'10':2,'01':3,'11':4,'1-1':6})
        with self.assertRaises(ValueError):r.polarize({'10':2})

    def test_invalid_mass_coupling_and_current_domains(self):
        for v in (-1,0,.25,math.inf,math.nan):
            with self.assertRaises(ValueError):r.form_and_mass_derivative(v)
        with self.assertRaises(ValueError):r.born_data(.02,.001,math.inf,1.)
        with self.assertRaises(ValueError):r.current_terms(1.5)
        with self.assertRaises(ValueError):r.current_terms(20,3.)
        with self.assertRaises(ValueError):r.scheme_shift(.02,.001,0.)

    def test_invalid_thermal_and_missing_part(self):
        with self.assertRaises(ValueError):r.thermal(1.,'11')
        with self.assertRaises(ValueError):r.thermal(.5,'21')
        with self.assertRaises(ValueError):r.thermal(.5,'11','NLO')
        with self.assertRaises(ValueError):r.thermal(.5,'11',component='tt')

    def test_summary_keeps_all_missing_physics_explicit(self):
        out=r.summary()
        for k in ('finite_NLO_hard_current_computed','full_coherent_NLO_gg_computed',
                  'external_NLO_probe_data_obtained','Omnes_data_acquired',
                  'relic_density_computed','Q_above_80_included'):
            self.assertFalse(out[k])


if __name__=='__main__':unittest.main()
