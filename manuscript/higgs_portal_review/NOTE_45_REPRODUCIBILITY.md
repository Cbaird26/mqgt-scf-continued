# Research Note 45 reproducibility

This addendum calculates only the finite, collinear-subtracted real light-quark-pair radiation term induced by coherent bottom/charm loops. It is not the complete bottom/charm-square NLO current, a standalone physical partial width, or a relic-abundance result.

The declared emitted flavors are massless u, d and s. The internal massive loops are b and c. The unchanged benchmark is m1=10 GeV, m2=11.5 GeV, with the previous portal, propagator and historical QCD inputs. The central thermal calculation uses T=0.5 GeV and the finite window w in [0,90].

Run the tests and numerical output with:

```sh
python -m unittest -v test_research_note_40.py test_research_note_42.py test_research_note_43.py test_research_note_44.py test_research_note_45.py
python bc_real_radiation.py
```

The original Note-41 standalone suite is not part of this command. The accompanying execution record distinguishes local execution, packaged-source hashes, and remote publication. No earlier scientific note or source module is silently replaced.
