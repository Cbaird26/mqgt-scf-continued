"""Numerical, not interval-certified, same-radius spectral-profile example.

Preserves f(0), m1,m2,m3, f'(0), f''(0), P, P_R, J.
The last three constraints preserve the reference stationary radius,
cosmological subtraction, and gravitational coefficient.
"""
from decimal import Decimal as D, getcontext
from pathlib import Path
import json

getcontext().prec = 95
NODES = 10
LEVELS = 40
PI = D('3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117068')


def coeff(a, R, levels=LEVELS):
    """Return P(a), P_R(a), P_RR(a), J(a), Y(a)."""
    H = D(30)
    HR = D(0)
    HRR = D(0)
    Y = D(20)/3
    for n, mult, q in [(0,12,D(1)/3),(1,28,D(32)/3),(2,16,D(4)/3)]:
        for ell in range(1, levels+1):
            b = a*ell*(ell+n)
            e = (-b/R**2).exp()
            val = (2*ell+n)*e
            H += mult*val
            HR += mult*val*2*b/R**3
            HRR += mult*val*(4*b*b/R**6 - 6*b/R**4)
            Y += q*val
    return H/a**2, HR/a**2, HRR/a**2, H/a, Y


def weighted(coeffs, w, column):
    return sum((wi*co[column] for wi,co in zip(w,coeffs)),D(0))


def rref_null(matrix):
    """Nine full-rank equations in ten unknowns, one free coordinate."""
    m = [row[:] for row in matrix]
    pivots = []
    r = 0
    for c in range(len(m[0])):
        if r == len(m): break
        pivot = max(range(r,len(m)),key=lambda i:abs(m[i][c]))
        if abs(m[pivot][c]) < D('1e-65'): continue
        m[r],m[pivot] = m[pivot],m[r]
        scale = m[r][c]
        m[r] = [x/scale for x in m[r]]
        for i in range(len(m)):
            if i==r: continue
            factor=m[i][c]
            m[i]=[x-factor*y for x,y in zip(m[i],m[r])]
        pivots.append(c)
        r+=1
    free=[i for i in range(len(m[0])) if i not in pivots]
    if len(free)!=1: raise ValueError((pivots,free))
    v=[D(0)]*len(m[0]);v[free[0]]=D(1)
    for i,c in enumerate(pivots): v[c]=-m[i][free[0]]
    norm=max(map(abs,v));v=[x/norm for x in v]
    return v,pivots


def main():
    js=[D(i) for i in range(1,NODES+1)]
    scale=sum((1/j**2 for j in js),D(0))/sum((1/j for j in js),D(0))
    nodes=[scale*j for j in js]
    w0=[D(1)/NODES]*NODES
    R=D('1.30')
    iterlog=[]
    for it in range(25):
        cs=[coeff(a,R) for a in nodes]
        P=weighted(cs,w0,0);PR=weighted(cs,w0,1);PRR=weighted(cs,w0,2)
        F=R*PR-2*P
        delta=F/(R*PRR-PR)
        iterlog.append([str(R),str(F),str(delta)])
        R-=delta
        if abs(delta)<D('1e-85'): break
    cs=[coeff(a,R) for a in nodes]
    base_rows=[[a**k for a in nodes] for k in [-3,-2,-1,0,1,2]]
    all_rows=base_rows+[[co[k] for co in cs] for k in [0,1,3]]
    labels=['m3','m2','m1','f0','minus_fprime','fsecond','P','P_R','J']
    # Row scaling improves elimination without changing the kernel.
    rows=[[x/max(map(abs,row)) for x in row] for row in all_rows]
    v,pivots=rref_null(rows)
    amp=D('0.05')
    wm=[u-amp*x for u,x in zip(w0,v)]
    wp=[u+amp*x for u,x in zip(w0,v)]
    metrics={}
    for name,w in [('minus',wm),('baseline',w0),('plus',wp)]:
        P=weighted(cs,w,0);PR=weighted(cs,w,1);PRR=weighted(cs,w,2);J=weighted(cs,w,3);Y=weighted(cs,w,4)
        metrics[name]={
            'P':P,'P_R':PR,'F':R*PR-2*P,'J':J,'c':P/R**2,
            'potential_curvature_factor':PRR-2*P/R**2,
            'gY_inverse_squared_per_kappa':Y/(6*PI**2),
            'M4r_squared_per_kappa':R**2*J/(24*PI**2),
            'min_weight':min(w),'max_weight':max(w),'sum_weights':sum(w),
        }
    residuals={label:sum((x*y for x,y in zip(row,v)),D(0)) for label,row in zip(labels,all_rows)}
    differences={label:sum((x*(p-m) for x,p,m in zip(row,wp,wm)),D(0)) for label,row in zip(labels,all_rows)}
    deltaZ=metrics['plus']['gY_inverse_squared_per_kappa']-metrics['minus']['gY_inverse_squared_per_kappa']
    cs60=[coeff(a,R,60) for a in nodes]
    refinement=max(abs(x-y) for one,two in zip(cs,cs60) for x,y in zip(one,two))
    checks={
        'positive_normalized_weights':all(metrics[key]['min_weight']>0 and abs(metrics[key]['sum_weights']-1)<D('1e-80') for key in ['minus','plus']),
        'same_nine_constraint_data':max(map(abs,differences.values()))<D('1e-80'),
        'common_stationary_radius':all(abs(metrics[key]['F'])<D('1e-80') for key in ['minus','plus']),
        'positive_restricted_curvature':all(metrics[key]['potential_curvature_factor']>0 for key in ['minus','plus']),
        'resolved_hypercharge_difference':abs(deltaZ)>D('1e-10'),
        'internal_sum_refinement':refinement<D('1e-80'),
    }
    if not all(checks.values()):
        raise ArithmeticError({key:value for key,value in checks.items() if not value})
    out={
        'precision':getcontext().prec,'levels':LEVELS,'common_R':R,'node_scale':scale,'nodes':nodes,
        'null_vector':v,'weights_minus':wm,'weights_plus':wp,'pivots':pivots,'metrics':metrics,
        'constraints_residual':residuals,'constraints_pair_differences':differences,
        'delta_gY_inverse_squared_per_kappa':deltaZ,
        'relative_delta_to_minus':deltaZ/metrics['minus']['gY_inverse_squared_per_kappa'],
        '40_vs_60_levels_max_coefficient_change':refinement,
        'newton_iterations':len(iterlog),
        'checks':checks,
        'caveat':'High-precision numerical witness, not interval-certified. Infinite sums approximated by 40/60 levels.',
    }
    output=Path(__file__).with_name('stationary_profiles_results.json')
    output.write_text(json.dumps(out,default=str,indent=2))
    print(json.dumps({'status':'PASS','output':str(output.resolve()),'checks':checks,'common_R':str(R),'delta_z':str(deltaZ),'relative_difference':str(deltaZ/metrics['minus']['gY_inverse_squared_per_kappa'])},indent=2))


if __name__=='__main__': main()
