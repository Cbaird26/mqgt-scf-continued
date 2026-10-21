verify_package.py checks payload bytes using Python's standard library. It needs no network connection.

rebuild_public.py needs pikepdf 10.17.0 and uses the included assembly_plan.json. Install requirements in a fresh virtual environment if needed. Choose an output path outside the extracted package. It preserves source page content and rebuilds a flat document outline. It does not promise byte-identical serialization or an identical outline hierarchy.

The detailed assembly validation checked content streams and page geometry for every page in both expanded editions and the supplement, bookmark bounds, expected page counts and source hashes. qpdf and rendered sample checks are documented in VERIFICATION.json. No scientific calculations were rerun during packaging.
