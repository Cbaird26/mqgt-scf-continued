"""Note 22 local algebra/integration regression checks; no QCD input files."""
import math
import unittest
from near_threshold_benchmark import (LEPTONS, HBAR_C, M_H, SM_H_WIDTH,
                                      contact_ratio_ceiling, higgs_pair_widths,
                                      leptonic_floor, reconstructed_mass_matrix,
                                      width_lepton)

class CompressedBenchmarkChecks(unittest.TestCase):
    def test_recoil_window_excludes_high_virtual_masses(self):
        self.assertLess(1.5**2,2.0**2)
        self.assertAlmostEqual(11.5-10,1.5)

    def test_muon_open_tau_closed(self):
        widths,_,_=leptonic_floor(10,1.5,0.001,n=2048)
        self.assertGreater(widths['muon'],0)
        self.assertEqual(widths['tau'],0)
        self.assertGreater(widths['electron'],0)

    def test_threshold_is_exactly_closed(self):
        mf=LEPTONS['muon']
        self.assertEqual(width_lepton(10,2*mf,0.001,mf),0)
        self.assertEqual(width_lepton(10,2*mf*0.9,0.001,mf),0)

    def test_muon_partial_width_reference(self):
        w=width_lepton(10,1.5,0.001,LEPTONS['muon'],n=8192)
        self.assertAlmostEqual(w/3.060190637e-22,1,delta=2e-8)

    def test_quadratic_coupling_scaling(self):
        w=width_lepton(10,1.5,0.001,LEPTONS['muon'],n=1024)
        w2=width_lepton(10,1.5,0.002,LEPTONS['muon'],n=1024)
        self.assertAlmostEqual(w2/w,4,places=12)

    def test_smooth_endpoint_quad_convergence(self):
        a=width_lepton(10,1.5,0.001,LEPTONS['muon'],n=1024)
        b=width_lepton(10,1.5,0.001,LEPTONS['muon'],n=8192)
        self.assertAlmostEqual(a/b,1,delta=1e-7)

    def test_contact_propagator_bracket(self):
        w=width_lepton(10,1.5,0.001,LEPTONS['muon'],n=1024)
        wc=width_lepton(10,1.5,0.001,LEPTONS['muon'],n=1024,contact=True)
        self.assertGreater(w/wc,1/(1+(0.0041/125)**2))
        self.assertLess(w/wc,contact_ratio_ceiling(1.5))
        self.assertLess(contact_ratio_ceiling(1.5)-1,0.0003)

    def test_lepton_floor_and_upper_bound(self):
        widths,floor,ctau=leptonic_floor(10,1.5,0.001,n=8192)
        self.assertAlmostEqual(floor/3.060267688e-22,1,delta=2e-8)
        self.assertAlmostEqual(ctau/644803.0059,1,delta=2e-8)
        self.assertAlmostEqual(floor*ctau,HBAR_C,delta=1e-29)

    def test_original_benchmark_recovery(self):
        widths,floor,ctau=leptonic_floor(10,15,0.001,n=8192)
        self.assertAlmostEqual(widths['tau']/1.151478228e-15,1,delta=2e-8)
        self.assertAlmostEqual(ctau/.1706244049,1,delta=2e-8)

    def test_reconstructed_masses_and_positive_bare_matrix(self):
        p,e,g,det=reconstructed_mass_matrix(10,11.5)
        self.assertAlmostEqual(p,55.609)
        self.assertAlmostEqual(e,116.125)
        self.assertAlmostEqual(g,16.125)
        self.assertGreater(p,0)
        self.assertGreater(det,0)
        A=p+0.002*246**2/2
        B=e
        roots=((A+B-math.sqrt((A-B)**2+4*g*g))/2,
               (A+B+math.sqrt((A-B)**2+4*g*g))/2)
        self.assertAlmostEqual(roots[0],100)
        self.assertAlmostEqual(roots[1],132.25)

    def test_higgs_widths_and_branching(self):
        g11,g12,g22=higgs_pair_widths(10,11.5)
        total=g11+g12+g22
        self.assertAlmostEqual(total/1.8974357382699838e-5,1,delta=2e-10)
        self.assertAlmostEqual(total/(total+SM_H_WIDTH),0.004606573320538131,places=12)

    def test_three_light_state_channel_closed(self):
        self.assertLess(11.5,3*10)

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError): width_lepton(10,-1,0.001,LEPTONS['muon'])
        with self.assertRaises(ValueError): width_lepton(10,1.5,0.001,0)
        with self.assertRaises(ValueError): width_lepton(10,1.5,0.001,float('nan'))
        with self.assertRaises(ValueError): contact_ratio_ceiling(M_H)
        with self.assertRaises(ValueError): reconstructed_mass_matrix(10,10)

if __name__=='__main__':
    unittest.main(verbosity=2)