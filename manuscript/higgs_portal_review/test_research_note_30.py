"""Synthetic-fixture tests only; not a run on any upstream Omnes file."""
import hashlib
import math
from pathlib import Path
import tempfile
import unittest
from omnes_grid_gate import authenticated_bytes, endpoint_gate, first_grid, git_blob_sha1, inspect_folder

GRID = '[' + ', '.join(repr(i/100) for i in range(601)) + ']'
PAYLOAD = ('[' + GRID + ', [[Complex(1.,0.)]]]').encode()

class GridTests(unittest.TestCase):
    def test_grid(self):
        g=first_grid(PAYLOAD)
        self.assertEqual(len(g),601)
        self.assertEqual((g[0],g[225],g[-1]),(0.,2.25,6.))
    def test_no_eval(self):
        evil=("[[__import__('os').system('false')],[]]").encode()
        with self.assertRaises(ValueError): first_grid(evil)
    def test_reject_non_numeric(self):
        with self.assertRaises(ValueError): first_grid(('[[None]' + ',0]'*600).encode())
    def test_missing_outer_prefix(self):
        with self.assertRaises(ValueError): first_grid(b'not-a-grid')
    def test_missing_delimiter(self):
        with self.assertRaises(ValueError): first_grid(('['+GRID+']').encode())
    def test_invalid_node(self):
        altered=('[' + GRID.replace('2.25','2.26',1) + ', [[0.]]]').encode()
        with self.assertRaises(ValueError): first_grid(altered)
    def test_long_prefix(self):
        with self.assertRaises(ValueError): first_grid(b'[[' + b'0,'*20000 + b'], []]')
    def test_blob_and_authentication(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'file';p.write_bytes(PAYLOAD)
            sha=git_blob_sha1(PAYLOAD)
            self.assertEqual(authenticated_bytes(p,len(PAYLOAD),sha),PAYLOAD)
            self.assertNotEqual(sha,hashlib.sha1(PAYLOAD).hexdigest())
            with self.assertRaises(ValueError): authenticated_bytes(p,len(PAYLOAD),'0'*40)
    def test_size_guard(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'file';p.write_bytes(PAYLOAD)
            with self.assertRaises(ValueError): authenticated_bytes(p,len(PAYLOAD)+1,'0'*40)
    def test_symlink_guard(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'real';p.write_bytes(PAYLOAD);q=Path(d)/'link';q.symlink_to(p)
            with self.assertRaises(ValueError): authenticated_bytes(q,len(PAYLOAD),git_blob_sha1(PAYLOAD))
    def test_four_matching_files(self):
        with tempfile.TemporaryDirectory() as d:
            manifest={}
            for name in ('a','b','c','d'):
                (Path(d)/name).write_bytes(PAYLOAD)
                manifest[name]=(len(PAYLOAD),git_blob_sha1(PAYLOAD))
            self.assertEqual(len(inspect_folder(Path(d),expected=manifest)),4)
    def test_one_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a=PAYLOAD;b=PAYLOAD.replace(b'2.25',b'2.26',1)
            (Path(d)/'a').write_bytes(a);(Path(d)/'b').write_bytes(b)
            manifest={'a':(len(a),git_blob_sha1(a)),'b':(len(b),git_blob_sha1(b))}
            with self.assertRaises(ValueError):inspect_folder(Path(d),expected=manifest)
    def test_endpoints(self):
        self.assertEqual(endpoint_gate(10,11.5)['s_endpoint_GeV2'],2.25)
        self.assertTrue(endpoint_gate(10,11.5)['within_provisional_2_GeV_window'])
        self.assertFalse(endpoint_gate(10,25)['within_grid'])
    def test_invalid_mass(self):
        with self.assertRaises(ValueError): endpoint_gate(11.5,10)
        with self.assertRaises(ValueError): endpoint_gate(10,math.nan)

if __name__ == '__main__':unittest.main(verbosity=2)
