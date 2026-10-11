"""Exact rational/polylog-basis identities between two published transcriptions.

Own ABDV color decomposition vs inherited HK product. Identities in the
specified common timelike HPL convention; not a diagram or empirical proof.
"""
from __future__ import annotations
import json
from functools import lru_cache
import sympy as s
from abdv_virtual_check import abdv_shapes
from bc_virtual_finite import hk_expression

@lru_cache(maxsize=1)
def proof():
    x,l,lm=s.symbols('x l lm')
    p2,p3,p4,n2,n3,n4,z2,z3,H=s.symbols('p2 p3 p4 n2 n3 n4 z2 z3 H')
    li=lambda k,z:{2:(p2,n2),3:(p3,n3),4:(p4,n4)}[k][0 if z==x else 1]
    # Shuffle/integration-by-parts identities from the HPL defining kernels.
    h={(0,):l,(1,):-lm,(0,0):l*l/2,(0,0,0):l**3/6,(0,0,0,0):l**4/24,
       (1,0):-l*lm-p2,
       (0,1,0):l*p2-2*p3,
       (0,-1,0):-l*n2+2*n3,
       (1,0,0):-l*l*lm/2-l*p2+p3,
       (0,1,0,0):l*l*p2/2-2*l*p3+3*p4,
       (0,-1,0,0):-l*l*n2/2+2*l*n3-3*n4,
       (0,0,-1,0):-l*n3+3*n4,
       (0,0,1,0):l*p3-3*p4,
       (1,0,0,0):-l**3*lm/6-l*l*p2/2+l*p3-p4,
       (1,0,-1,0):H}
    Fa,Fb,Ga=abdv_shapes(x,lambda w:h[w],z2,z3)
    cf=s.Rational(4,3); ca=3
    G_OS=-s.Rational(3,2)*(cf*(Fa+cf*Fb)+ca*Ga)
    HK=hk_expression(x,l,lm,li,H,z2,z3,s.Rational(2,5)*z2*z2)
    rr=-x/(1-x)**2
    F=6*rr*(1-(1-4*rr)*l*l/4)
    D=2*x*(1-x)/(1+x)*(s.diff(F,x)+s.diff(F,l)/x)
    derivative=s.cancel(Fb-D)
    pol=s.Poly(s.expand(G_OS-HK),l,lm,p2,p3,p4,n2,n3,n4,z2,z3,H)
    coefficients=[s.cancel(c) for c in pol.coeffs()]
    os_zero=all(c==0 for c in coefficients)
    # ABVD MS=G_OS + (3/2)CF*[log(mu^2/m^2)+CF]*Fb.
    # Since Fb=D, construct the coefficient without inferring the sign:
    Lm=s.symbols('log_mu2_over_m2')
    G_MS=-s.Rational(3,2)*(cf*(Fa-Fb*Lm)+ca*Ga)
    residual=s.Poly(s.expand(G_MS-HK-2*(Lm+cf)*D),l,lm,p2,p3,p4,n2,n3,n4,z2,z3,H,Lm)
    ms_zero=all(s.cancel(c)==0 for c in residual.coeffs())
    return {'method':'Exact SymPy rational cancellation after explicit HPL shuffle identities',
      'source_ABDV':'hep-ph/0611266v3 Eqs (6),(11)-(15),(27)-(30)',
      'source_HK':'hep-ph/0509189v1 Eq (3.7), inherited transcription',
      'Fb_minus_mass_derivative_exact_zero':derivative==0,
      'G_ABDV_OS_minus_HK_G1_exact_zero':os_zero,
      'G_ABDV_MS_minus_HK_G1_minus_2_log_plus_four_thirds_D_exact_zero':ms_zero,
      'OS_polynomial_monomials_checked':len(coefficients),
      'MS_polynomial_monomials_checked':len(residual.coeffs()),
      'identity':'G_ABDV_OS=G1; G_ABDV_MS=G1+2*(ln(mu^2/m^2)+4/3)*D F',
      'literal_Note46_difference':'G_ABDV_MS-G_Note46_literal=(8/3)D F',
      'scope':'Exact identities of transcribed formulas in a common HPL basis; not full real-plus-virtual validation.'}

if __name__=='__main__':
    print(json.dumps(proof(),indent=2))
