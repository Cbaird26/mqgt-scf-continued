"""Note 44 formula/software tests; not experimental or independent QCD validation."""
import hashlib
import math
from pathlib import Path
import unittest
import mpmath as mp
from scipy.optimize import brentq, root
from scipy.special import kve, roots_genlaguerre
import mixed_gluon_nlo as m
import heavy_quark_thermal as h
import gluon_loop_thermal as g
import top_operator_nlo as t


def mp_hard(r):
    """Separately written 70-digit Eq. (6) evaluation with mpmath polylogs."""
    with mp.workdps(70):
        r=mp.mpf(str(r));z=1/r;u=(z-2-mp.sqrt(z*(z-4)))/2
        l=mp.log(u);P=mp.pi;Li=mp.polylog;Z=mp.zeta(3)
        B=(27*Li(4,u*u)+72*Li(4,u)-32*(Li(3,u*u)-Z)*l
           +(28*Li(2,-u)+16*Li(2,u))*(l*l-P*P))*(u-1)*(u*u+1)/(2*(u+1))
        B+=(13*u**4+54*u**3-72*u*u+54*u+5)*l**4/(48*(u+1)**2)
        B-=(23*u**4+162*u**3-216*u*u+162*u+31)*P**2*l*l/(24*(u+1)**2)
        B-=(94*u**4-540*u**3+720*u*u-540*u-274)*P**4/(480*(u+1)**2)
        B-=4*(u-1)**2*(Li(3,-u)+8*Li(3,u)-4*Li(2,u)*l)
        B+=(51*u*u-110*u+51)*(Li(2,-u)*l-Li(3,-u))
        B+=(53*u*u-114*u+53)*(l*l-P*P)*mp.log(1+u)/2+(31*u*u-70*u+31)*Z
        B-=(141*u**3-205*u*u-7*u+39)*l**3/(24*(u+1))
        B+=(335*u**3-527*u*u+67*u+29)*P**2*l/(24*(u+1))
        B-=(341*u**4+384*u**3-1588*u*u+384*u+341)*(P*P-l*l)/(16*(u+1)**2)
        B-=12*(u+1)**2*mp.log(1+u)
        B+=3*(183*u**3-311*u*u+503*u-119)*l/(16*(u+1))
        B-=mp.mpf(5285)*(u*u+1)/32+mp.mpf(3611)*u/16
        return float(B/(12*(u+1)**2))


def laguerre(T,pair,q,n=64):
    mi,mj,k=h.PAIRS[pair];xi,xj=mi/T,mj/T;a=xi+xj;b=xi-xj
    nodes,weights=roots_genlaguerre(n,.5)
    pref=k*k/(32*math.pi*xi**2*xj**2*kve(2,xi)*kve(2,xj))
    vals=[]
    for w,weight in zip(nodes,weights):
        if w>90:continue  # finite-domain quadrature comparison only
        y=a+w;Q=T*y;D=(Q*Q-h.MH*h.MH)**2+(h.MH*h.GH)**2
        vals.append(weight*y*y*math.sqrt((2*a+w)*(y*y-b*b))*
                    m.current_components(Q,q)['NLO']*kve(1,y)/D)
    return float(pref*math.fsum(vals))


def generic_current(Q,mloop,mY,a,scheme='hybrid',scale=1.):
    logs=sum(2*math.log(Q/x) for x in mloop)
    total=0.
    for M,Y in zip(mloop,mY):
        r=(M/Q)**2
        C=math.fsum(m.coefficient_parts(r,logs,scale,scheme).values())
        total-=8/3*a*a*M*Y*(m.lo_shape(r)+a*C)
    return total


class MixedGluonTests(unittest.TestCase):
    def test_inherited_blob_identities(self):
        refs={'heavy_quark_thermal.py':'40d51657a26fb20851be2bafa0ea6b3efe05ddfb',
              'finite_mass_quark_thermal.py':'117fd5d3abb650f05334d8bff6f88115c63e09da',
              'gluon_loop_thermal.py':'c49c6fab4baa2d9c01c64f9fd8c2fdb7f018d50c',
              'top_operator_nlo.py':'cf2c5f0fa09802330dfdf401e15ed1c1d78b9ab3'}
        for name,ref in refs.items():
            b=Path(__file__).with_name(name).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),ref)

    def test_polylogs_independent_backend(self):
        with mp.workdps(60):
            for n in (2,3,4):
                for z in (-.7,-.1,-.001,0.,.001,.05,.7):
                    self.assertAlmostEqual(m.polylog(n,z),float(mp.polylog(n,z)),delta=3e-16)

    def test_rationalized_coordinate(self):
        with mp.workdps(60):
            for r in (1e-10,.001,.03,.15):
                z=1/mp.mpf(str(r));u=(z-2-mp.sqrt(z*(z-4)))/2
                self.assertAlmostEqual(m.coordinates(r)[1]/float(u),1.,delta=8e-16)

    def test_LO_recovers_coherent_loop_interference(self):
        for Q in (20.,21.5,23.,40.,80.):
            for scale in (.5,1.,2.):
                for scheme in ('MSbar','pole1'):
                    for q in ('b','c'):
                        lo=m.current_components(Q,q,scale,scheme)['LO']
                        old=g.components(Q,scale,scheme,heavy_top=True)['t'+q]
                        self.assertAlmostEqual(lo,old,delta=2e-15)

    def test_source_width_normalization(self):
        Q=30.;M=3.2;Y=2.8;a=.04;r=(M/Q)**2
        delta1=4*Q*M*Y/(math.pi*h.V*h.V)*m.lo_shape(r)
        width=(-a/12)*a*delta1
        S=8*math.pi*h.V*h.V/Q*width
        self.assertAlmostEqual(S,-8/3*a*a*M*Y*m.lo_shape(r),delta=1e-17)

    def test_hard_formula_against_70_digit(self):
        for r in (1e-10,1e-6,.001,.005,.027,.05,.1):
            expected=mp_hard(r)
            self.assertAlmostEqual(m.hard_shape(r),expected,delta=2e-11*max(1,abs(expected)))

    def test_published_LO_power_expansion_eq8(self):
        r=1e-7;l=-math.log(r)
        expanded=(l*l-math.pi**2-4)/8-r*(l*l+l-math.pi**2)/2
        self.assertAlmostEqual(m.lo_shape(r),expanded,delta=2e-12)

    def test_published_NLO_small_mass_expansion_eq10(self):
        r=1e-11;log=-math.log(r)
        full=m.hard_shape(r)-log*m.lo_shape(r)/3
        self.assertAlmostEqual(full,m.small_mass_shape(r),delta=3e-7)

    def test_wavefunction_spectator_and_symmetrization(self):
        rb,rc=.027,.0014;logs=-math.log(rb*rc)
        d1b=3*m.lo_shape(rb);d1c=.2*m.lo_shape(rc);d1=d1b+d1c
        literal=-(logs/6)*d1-(logs/6)*d1
        self.assertAlmostEqual(literal,-logs*d1/3,places=14)
        for r in (rb,rc):
            self.assertEqual(m.coefficient_parts(r,logs)['wavefunction'],-logs*m.lo_shape(r)/3)

    def test_wavefunction_coefficient_matches_external_gg_leg_factor(self):
        # Same gg external-state factor as source Eq.(4) / Note43.
        Q=30.;mb,mc=3.,.7;logs=2*math.log(Q/mb)+2*math.log(Q/mc)
        E=t.coefficient_veto(Q,mb,mc)-(95/4-7*3/6)
        self.assertAlmostEqual(E,-logs/3,delta=2e-15)

    def test_published_table1_withheld_NLO_consistency(self):
        # Source Table 1 OS rows at mu=Q. Infer auxiliary masses from TWO
        # rounded LO rows, then check the NLO row without fitting to it.
        # This is a rounding-level consistency test, NOT independent input
        # mass retrieval or reproduction of the source's four-loop running.
        Q=125.09;v=1/math.sqrt(math.sqrt(2)*1.166378e-5)
        a=math.sqrt(.1837e-3*72*math.pi*v*v/Q**3)
        norm=Q/(8*math.pi*v*v)
        def rates(masses):
            Fs=[g.form_factor((Q/(2*x))**2) for x in masses]
            pref=norm*a*a*Q*Q/9
            return pref*2*sum(F.real for F in Fs),pref*abs(sum(Fs))**2
        sol=root(lambda x:[(rates(x)[0]+.0364e-3)*1e5,
                           (rates(x)[1]-.0051e-3)*1e5],[5.,2.8])
        self.assertTrue(sol.success)
        logs=sum(2*math.log(Q/x) for x in sol.x)
        delta=sum(norm*(-8/3)*a**3*x*x*sum(m.coefficient_parts(
                    (x/Q)**2,logs,scheme='pole1').values()) for x in sol.x)
        self.assertAlmostEqual(1000*delta,-.0152,delta=5e-5)  # MeV

    def test_single_Wilson_matching_factor(self):
        r=.03;cp=m.coefficient_parts(r,8.)
        self.assertEqual(cp['matching'],11*m.lo_shape(r)/4)
        self.assertNotEqual(cp['matching'],11*m.lo_shape(r)/2)

    def test_loop_mass_derivative_finite_difference(self):
        for r in (.001,.027,.05):
            eps=1e-5
            vals=[math.exp(e)*m.lo_shape(r*math.exp(2*e)) for e in (-eps,eps)]
            self.assertAlmostEqual((vals[1]-vals[0])/(2*eps),m.loop_mass_derivative(r),delta=3e-9)

    def test_no_extra_Yukawa_conversion_in_MSbar(self):
        r=.027;d=4/3-math.log(r);c=m.coefficient_parts(r,10.)
        correct=d*m.loop_mass_derivative(r)
        wrong=correct+d*m.lo_shape(r)
        self.assertEqual(c['scheme'],correct)
        self.assertGreater(abs(c['scheme']-wrong),.1)

    def test_hybrid_to_MSbar_reexpansion_first_missing_order(self):
        errors=[];Q=30.;ms=[3.1,.7]
        for a in (2e-5,1e-5):
            pole=[x*(1+a*(4/3+2*math.log(Q/x))) for x in ms]
            exact=generic_current(Q,pole,ms,a,'hybrid')
            expanded=generic_current(Q,ms,ms,a,'MSbar')
            errors.append(abs(exact-expanded))
        self.assertAlmostEqual(errors[0]/errors[1],16.,delta=.025)

    def test_hybrid_to_pole_reexpansion_first_missing_order(self):
        errors=[];Q=30.;pole=[4.3,1.27]
        for a in (2e-5,1e-5):
            yuk=[x*(1-a*(4/3+2*math.log(Q/x))) for x in pole]
            exact=generic_current(Q,pole,yuk,a,'hybrid')
            expanded=generic_current(Q,pole,pole,a,'pole1')
            errors.append(abs(exact-expanded))
        self.assertAlmostEqual(errors[0]/errors[1],16.,delta=.001)

    def test_MSbar_explicit_scale_log_identity(self):
        r=.027;eps=1e-4
        C=lambda L:sum(m.coefficient_parts(r,10.,math.exp(L/2)).values())
        deriv=(C(eps)-C(-eps))/(2*eps)
        expected=(23/6+1)*m.lo_shape(r)+m.loop_mass_derivative(r)
        self.assertAlmostEqual(deriv,expected,delta=1e-10)

    def test_running_scale_remainder_is_fourth_order(self):
        def slope(a0):
            def value(L):
                a=h.a_fixed_nf(30*math.exp(L/2),30,a0,5)
                masses=[x*h.mass_ratio(a,a0,5) for x in (3.1,.7)]
                return generic_current(30,masses,masses,a,'MSbar',math.exp(L/2))
            eps=1e-3
            return abs((value(eps)-value(-eps))/(2*eps))
        self.assertAlmostEqual(slope(2e-5)/slope(1e-5),16.,delta=.02)

    def test_zero_LO_is_not_singular(self):
        root=brentq(m.lo_shape,.001,.1,xtol=1e-15)
        self.assertLess(abs(m.lo_shape(root)),1e-13)
        cp=m.coefficient_parts(root,10.)
        self.assertTrue(all(math.isfinite(v) for v in cp.values()))
        self.assertGreater(abs(cp['scheme']),1.)

    def test_signed_channels_not_clipped(self):
        self.assertGreater(m.current_components(20,'b')['LO'],0.)
        self.assertLess(m.current_components(23,'b')['LO'],0.)
        self.assertLess(m.current_components(20,'c')['NLO'],0.)

    def test_component_sum(self):
        c=m.current_components(20,'b')
        self.assertAlmostEqual(c['NLO'],c['LO']+sum(c['delta_'+s] for s in ('hard','wavefunction','matching','scale','scheme')),places=15)

    def test_Q_w_thermal_all_six(self):
        for p in h.PAIRS:
            for q in ('b','c'):
                a=m.thermal(.5,p,q)[0];b=m.thermal(.5,p,q,method='Q')[0]
                self.assertAlmostEqual(a,b,delta=1e-27)

    def test_generalized_laguerre_all_six(self):
        for p in h.PAIRS:
            for q in ('b','c'):
                self.assertAlmostEqual(m.thermal(.5,p,q)[0],laguerre(.5,p,q),delta=2e-27)

    def test_laguerre_order_convergence(self):
        for q in ('b','c'):
            self.assertAlmostEqual(laguerre(.5,'11',q,32),laguerre(.5,'11',q,64),delta=1e-26)

    def test_window_and_lower_temperature(self):
        for T in (1/3,.5):
            for q in ('b','c'):
                a=m.thermal(T,'12',q)[0]
                for cut in (60,100):
                    self.assertAlmostEqual(a,m.thermal(T,'12',q,cut=cut)[0],delta=1e-27)

    def test_effective_central_regression(self):
        w=h.equilibrium_weights(.5)
        expected={'b':1.2363434370148974e-17,'c':-8.77436054110391e-18}
        for q,ref in expected.items():
            val=sum(w[p]*m.thermal(.5,p,q)[0] for p in w)
            self.assertAlmostEqual(val,ref,delta=2e-27)

    def test_scale_and_scheme_regression(self):
        w=h.equilibrium_weights(.5)
        for sc,sch,ref in ((.5,'MSbar',1.23936046191678e-17),(2.,'MSbar',-1.33848747591964e-18),(1.,'pole1',1.85730873047797e-17)):
            val=sum(w[p]*sum(m.thermal(.5,p,q,scale=sc,scheme=sch)[0] for q in ('b','c')) for p in w)
            self.assertAlmostEqual(val,ref,delta=2e-27)

    def test_absolute_cap_not_a_sample_max(self):
        cap=m.current_cap()
        for Q in (20.,21.5,23.,40.,80.):
            for sc in (.5,1.,2.):
                for sch in ('MSbar','pole1'):
                    for q in ('b','c'):
                        self.assertLess(abs(m.current_components(Q,q,sc,sch)['NLO']),cap)
        self.assertGreater(cap,1.)

    def test_finite_domain_remainder(self):
        for p in h.PAIRS:
            bound=m.remainder_to_80(.5,p)
            self.assertGreater(bound,0.)
            self.assertLess(bound,1e-40)

    def test_invalid_shape_inputs(self):
        for r in (-1,0,.25,math.inf,math.nan):
            with self.assertRaises(ValueError):m.hard_shape(r)
        with self.assertRaises(ValueError):m.polylog(1,.01)
        with self.assertRaises(ValueError):m.polylog(2,.9)
        with self.assertRaises(ValueError):m.coefficient_parts(.03,4.,scheme='invalid')

    def test_invalid_current_inputs(self):
        for Q in (1.5,19.9,80.1,math.nan):
            with self.assertRaises(ValueError):m.current_components(Q,'b')
        with self.assertRaises(ValueError):m.current_components(20,'s')
        with self.assertRaises(ValueError):m.current_components(20,'b',.49)
        with self.assertRaises(ValueError):m.current_components(20,'b',scheme='hybrid')

    def test_invalid_thermal_inputs(self):
        for call in (lambda:m.thermal(1.,'11','b'),lambda:m.thermal(.5,'21','b'),
                     lambda:m.thermal(.5,'11','b',cut=101),lambda:m.thermal(.5,'11','b',part='total'),
                     lambda:m.thermal(.5,'11','b',method='bad')):
            with self.assertRaises(ValueError):call()

    def test_partial_sum_does_not_double_count_LO(self):
        s=m.summary();z=s['PARTIAL_UPGRADE_NOT_FULL_NLO']
        self.assertAlmostEqual(z['sum_GeV_minus2'],9.851884092106958e-17,delta=3e-27)
        self.assertAlmostEqual(z['sum_GeV_minus2']-z['coherent_LO_note42'],
            z['top_NLO_veto_increment_note43']+z['mixed_NLO_increment'],delta=1e-30)
        for k in ('coherent_bc_square_NLO_computed','full_coherent_NLO_gg_computed',
                  'mixed_real_heavy_cuts_included','chemical_equilibrium_established',
                  'relic_density_computed','Q_above_80_included'):
            self.assertFalse(s[k])


if __name__=='__main__':unittest.main()
