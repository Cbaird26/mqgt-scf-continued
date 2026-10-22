"""Run every calculation in dependency order and report the assertion totals.

    python3 run_all.py            # stdlib scripts; independent_check.py if numpy+scipy are importable
    python3 run_all.py --no-float # skip the NumPy/SciPy cross-check

Each script regenerates only its own *_results.json.  Before rerunning, the
previous result files (if present) are hashed so that byte-level
reproducibility can be reported afterwards.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = ['inherited_inputs.py', 'scalar_sector.py', 'anomaly_sector.py', 'vacuum_matching.py']
RESULTS = {s: s.replace('.py', '_results.json') for s in ORDER + ['independent_check.py']}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def main():
    want_float = '--no-float' not in sys.argv
    if want_float:
        try:
            import numpy, scipy  # noqa: F401
        except Exception:
            print('numpy/scipy not importable: skipping independent_check.py')
            want_float = False
    scripts = ORDER + (['independent_check.py'] if want_float else [])
    before = {s: sha(HERE / RESULTS[s]) for s in scripts}
    total = 0
    n_numpy = 0
    for s in scripts:
        print('==> running', s)
        proc = subprocess.run([sys.executable, str(HERE / s)], cwd=str(HERE))
        if proc.returncode != 0:
            print('FAILED:', s)
            raise SystemExit(proc.returncode)
        res = json.loads((HERE / RESULTS[s]).read_text())
        n = len(res['checks'])
        bad = [k for k, v in res['checks'].items() if v is False]
        total += n
        if s == 'independent_check.py':
            n_numpy += n
        else:
            n_numpy += len([k for k in res.get('numpy_dependent_checks', []) if k in res['checks']])
        print('    %d checks recorded, %d failed' % (n, len(bad)))
    after = {s: sha(HERE / RESULTS[s]) for s in scripts}
    print('\nTotal recorded checks: %d (%d standard library only, %d need NumPy/SciPy)' % (total, total - n_numpy, n_numpy))
    for s in scripts:
        if before[s] is None:
            status = 'created'
        elif before[s] == after[s]:
            status = 'byte-identical to previous run'
        else:
            status = 'DIFFERS from previous run (expected for independent_check_results.json across NumPy versions; inspect otherwise)'
        print('  %-32s %s' % (RESULTS[s], status))


if __name__ == '__main__':
    main()
