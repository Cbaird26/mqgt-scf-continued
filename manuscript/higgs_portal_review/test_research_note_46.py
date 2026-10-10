"""Note46: numerical checks, source limits and convention tests; no empirical test."""
import cmath
import hashlib
import math
from pathlib import Path
import unittest
import mpmath as mp
from scipy.special import roots_genlaguerre,kve
import bc_virtual_finite as v
import coherent_bc_rg as rg
import heavy_quark_thermal as h
import gluon_loop_thermal as g
from virtual_reference import product as mp_product,hpl_integral,form as mp_form


def gauss_laguerre(T,pair,n=64):
    mi,mj,k=h.PAIRS[pair];xi,xj=mi/T,mj/T;a=xi+xj;b=xi-xj
    pref=k*k/(32*math.pi*xi*xi*xj*xj*kve(2,xi)*kve(2,xj))
    nodes,weights=roots_genlaguerre(n,.5);out=0.
    for w,z in zip(nodes,weights):
        if w>h.W_CUT:continue
        y=a+w;Q=T*y
        out+=z*y*y*math.sqrt((2*a+w)*(y*y-b*b))*v.current_weight(Q)*kve(1,y)/((Q*Q-h.MH*h.MH)**2+(h.MH*h.GH)**2)
    return pref*out


class VirtualFiniteTests(unittest.TestCase):
    def test_inherited_hashes(self):
        for mod,expected in ((h,'40d51657a26fb20851be2bafa0ea6b3efe05ddfb'),
                             (g,'c49c6fab4baa2d9c01c64f9fd8c2fdb7f018d50c')):
            b=Path(mod.__file__).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),expected)

    def test_polylogs_against_mpmath(self):
        with mp.workdps(55):
            for z in (-.09,-.03,-.001,.001,.07):
                for n in (2,3,4):
                    self.assertLess(abs(v.li_series(n,z)-complex(mp.polylog(n,z))),2e-16)

    def test_hpl_against_defining_integral(self):
        with mp.workdps(45):
            for z in (-.09,-.03,-.001):
                self.assertLess(abs(v.hpl_10m10(z)-complex(hpl_integral(z))),2e-17)

    def test_hpl_defining_derivative(self):
        for z in (-.08,-.01):
            e=1e-6*abs(z)
            deriv=(v.hpl_10m10(z+e)-v.hpl_10m10(z-e))/(2*e)
            expected=(-cmath.log(complex(z))*v.li_series(2,-z)+2*v.li_series(3,-z))/(1-z)
            self.assertLess(abs(deriv-expected),2e-10)

    def test_finite_polylog_series_remainder_bound(self):
        # |sum_(k>N) z^k/k^s| <= |z|^(N+1)/[(N+1)^s(1-|z|)].
        z=mp.mpf('0.1')
        with mp.workdps(70):
            z=mp.mpf('0.1');N=48
            for n in (2,3,4):
                trunc=sum(z**k/mp.mpf(k)**n for k in range(1,N+1))
                bound=z**(N+1)/(mp.mpf(N+1)**n*(1-z))
                self.assertLess(abs(mp.polylog(n,z)-trunc),bound)

    def test_full_expression_arbitrary_precision(self):
        for r in (.06,.03,.001,1e-6):
            expected=complex(mp_product(r,45))
            self.assertLess(abs(v.hk_product(r)-expected),1e-13*max(1.,abs(expected)))

    def test_source_heavy_mass_limit(self):
        # Pure formula check outside production evaluator; source limit 11/2.
        with mp.workdps(30):
            vals=[]
            for tau in ('0.1','0.01'):
                r=1/(4*mp.mpf(tau));c=mp_product(str(r),30)/mp_form(r)
                self.assertLess(abs(mp.im(c)),mp.mpf('1e-20'))
                vals.append(float(mp.re(c)))
            self.assertLess(abs(vals[1]-5.5),.011)
            self.assertLess(abs(vals[1]-5.5),abs(vals[0]-5.5)/9)

    def test_source_eq27_matches_mass_derivative(self):
        for r in (.001,.02,.05):
            tau=1/(4*r);b=math.sqrt(1-1/tau)
            ell=complex(math.log(tau)+2*math.log1p(b),-math.pi)
            f=-ell**2/4;fp=-ell/(2*tau*b)
            FC2=3/tau**2*(tau+(tau-2)*f-(tau-1)*tau*fp)
            DF=rg.form_and_mass_derivative(r)[1]
            self.assertLess(abs(FC2-DF),2e-14)

    def test_F0_matches_published_LO_normalization(self):
        for r in (.001,.02,.05):
            self.assertLess(abs(rg.form_and_mass_derivative(r)[0]-g.form_factor(1/(4*r))),2e-15)

    def test_component_sum(self):
        for Q in (20.,23.,50.,80.):
            c=[v.current_weight(Q,component=q) for q in ('bb','cc','bc')]
            self.assertAlmostEqual(sum(c),v.current_weight(Q),delta=5e-17)

    def test_additive_formula_equals_source_ratio_away_from_zero(self):
        rb,rc=.027,.0014
        F=[rg.form_and_mass_derivative(r)[0] for r in (rb,rc)]
        G=[v.hk_product(r)-2*math.log(r)*rg.form_and_mass_derivative(r)[1] for r in (rb,rc)]
        c=(sum(G)/sum(F)).real
        out=v.coefficient_components(rb,rc)['virtual']['coherent']
        self.assertAlmostEqual(out,abs(sum(F))**2*c,places=13)

    def test_exact_cancellation_does_not_divide_by_LO(self):
        d=v.coefficient_components(.02,.02,kb=1,kc=-1)
        self.assertEqual(d['B']['coherent'],0.)
        self.assertEqual(d['virtual']['coherent'],0.)
        self.assertEqual(v.current_weight(20,kb=0,kc=0),0.)

    def test_polarization_with_fixed_masses(self):
        f=lambda b,c:v.current_weight(22,kb=b,kc=c)
        results=rg.polarize({'10':f(1,0),'01':f(0,1),'11':f(1,1),'1-1':f(1,-1),'00':f(0,0)})
        for c in ('bb','cc','bc'):
            self.assertAlmostEqual(results[c],v.current_weight(22,component=c),delta=5e-17)

    def test_no_extra_cross_section_factor_two(self):
        rb,rc=.02,.001
        d=v.coefficient_components(rb,rc,kc=0)
        F,DF=rg.form_and_mass_derivative(rb)
        G=v.hk_product(rb)-2*math.log(rb)*DF
        self.assertAlmostEqual(d['virtual']['bb'],(G*F.conjugate()).real,places=14)

    def test_MS_OS_conversion_difference(self):
        for scale in (.5,1.,2.):
            rb,rc=.027,.0014
            ms=v.coefficient_components(rb,rc,scale)['virtual']
            os=v.coefficient_components(rb,rc,scale,'pole1')['virtual']
            shift=rg.scheme_shift(rb,rc,scale)
            for c in v.COMPONENTS:
                self.assertAlmostEqual(ms[c]-os[c],shift[c],delta=2e-13)

    def test_scheme_reexpansion_residual_is_fourth_order(self):
        rb,rc=.027,.0014
        d1,d2=4/3-math.log(rb),4/3-math.log(rc)
        errs=[]
        for a in (2e-5,1e-5):
            pole=v.coefficient_components(rb*(1+a*d1)**2,rc*(1+a*d2)**2,scheme='pole1')
            ms=v.coefficient_components(rb,rc)
            os=a*a*pole['B']['coherent']+a**3*pole['virtual']['coherent']
            ss=a*a*ms['B']['coherent']+a**3*ms['virtual']['coherent']
            errs.append(abs(os-ss))
        self.assertAlmostEqual(errs[0]/errs[1],16.,delta=.03)

    def test_frozen_mass_scale_coefficient_reproduces_RG_note45(self):
        rb,rc=.027,.0014;e=1e-4
        c1=v.coefficient_components(rb,rc,math.exp(e/2))
        c0=v.coefficient_components(rb,rc,math.exp(-e/2))
        K=rg.required_log_coefficient(rb,rc)
        for c in v.COMPONENTS:
            slope=(c1['virtual'][c]+c1['universal_scale_log'][c]-c0['virtual'][c]-c0['universal_scale_log'][c])/(2*e)
            self.assertAlmostEqual(slope,K[c],delta=3e-10)

    def test_residual_scale_derivative_starts_fourth_order(self):
        rb0,rc0=.027,.0014
        def slope(a0):
            def f(L):
                a=a0/(1+rg.BETA0*a0*L)
                factor=(a/a0)**(2/rg.BETA0)
                d=v.coefficient_components(rb0*factor,rc0*factor,math.exp(L/2))
                return a*a*d['B']['coherent']+a**3*(d['virtual']['coherent']+d['universal_scale_log']['coherent'])
            e=.002
            return abs((f(.4+e)-f(.4-e))/(2*e))
        self.assertAlmostEqual(slope(2e-4)/slope(1e-4),16.,delta=.1)

    def test_thermal_central_regressions(self):
        refs={'11':1.58463635802393e-17,'12':1.51811945129334e-17,'22':1.44396275371635e-17}
        for p,x in refs.items():
            self.assertAlmostEqual(v.thermal(.5,p)[0]/x,1.,delta=2e-10)

    def test_coherent_LO_recovery(self):
        w=h.equilibrium_weights(.5)
        lo=sum(w[p]*v.thermal(.5,p,part='LO')[0] for p in h.PAIRS)
        self.assertAlmostEqual(lo/2.65726141679e-17,1.,delta=3e-11)

    def test_thermal_Q_and_w_all_components(self):
        for p in h.PAIRS:
            for c in v.COMPONENTS:
                w=v.thermal(.5,p,component=c)[0]
                Q=v.thermal(.5,p,component=c,method='Q')[0]
                self.assertLess(abs(Q-w),2e-29)

    def test_thermal_laguerre_independent(self):
        for p in h.PAIRS:
            self.assertAlmostEqual(gauss_laguerre(.5,p)/v.thermal(.5,p)[0],1.,delta=2e-9)

    def test_thermal_laguerre_order(self):
        for n in (32,64,96):
            self.assertAlmostEqual(gauss_laguerre(.5,'11',n)/v.thermal(.5,'11')[0],1.,delta=2e-8)

    def test_finite_window(self):
        a=v.thermal(.5,'12')[0]
        for cut in (50,70,100):
            self.assertAlmostEqual(v.thermal(.5,'12',cut=cut)[0]/a,1.,delta=2e-9)

    def test_low_temperature_check(self):
        a=v.thermal(1/3,'12')[0];b=v.thermal(1/3,'12',method='Q')[0]
        self.assertAlmostEqual(a/b,1.,delta=2e-9)

    def test_effective_is_conditional_weighted_sum(self):
        s=v.summary();w=h.equilibrium_weights(.5)
        for c in v.COMPONENTS:
            self.assertEqual(sum(w[p]*s['pair_virtual_GeV_minus2'][p][c] for p in h.PAIRS),s['conditional_effective_virtual_GeV_minus2'][c])

    def test_auxiliary_pole_virtual_can_be_negative(self):
        w=h.equilibrium_weights(.5)
        val=sum(w[p]*v.thermal(.5,p,scheme='pole1')[0] for p in h.PAIRS)
        self.assertLess(val,0.) # Not a standalone probability.

    def test_scale_log_is_zero_centrally(self):
        c=v.coefficient_components(.03,.001)
        self.assertTrue(all(x==0. for x in c['universal_scale_log'].values()))
        self.assertEqual(v.current_weight(20,part='virtual'),v.current_weight(20,part='virtual_scale'))

    def test_reject_invalid_math_inputs(self):
        for r in (0.,-.1,.081,float('nan'),float('inf')):
            with self.assertRaises(ValueError):v.hk_product(r)
        with self.assertRaises(ValueError):v.li_series(1,.01)
        with self.assertRaises(ValueError):v.hpl_10m10(0)
        with self.assertRaises(ValueError):v.li_series(2,.2)

    def test_reject_invalid_hard_thermal_inputs(self):
        for fun in (lambda:v.current_weight(1.5),lambda:v.current_weight(81),
                    lambda:v.current_weight(22,scale=.4),lambda:v.current_weight(22,part='full'),
                    lambda:v.current_weight(22,scheme='unknown'),lambda:v.thermal(.6,'11'),
                    lambda:v.thermal(.5,'21'),lambda:v.thermal(.5,'11',cut=101)):
            with self.assertRaises(ValueError):fun()

    def test_missing_full_result_rejected(self):
        with self.assertRaises(NotImplementedError):v.complete_nlo_current(20)

    def test_scope_flags(self):
        d=v.summary()
        for k in ('chemical_equilibrium_established','complete_coherent_NLO_computed',
                  'physical_rate_beyond_Q80_computed','relic_density_computed','low_energy_Omnes_data_acquired'):
            self.assertFalse(d[k])

if __name__=='__main__':unittest.main()
