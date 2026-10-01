"""Synthetic-input checks for Note 21; no third-party Omnes bytes used."""
import hashlib
import math
from pathlib import Path
import tempfile
import unittest

from safe_omnes_manifest import check_folder, git_blob_sha1, verify_file, EXPECTED

F_W = 0.004138912  # Note 20: toy kinematic-weight fraction, 0<=s<=4 of 0<=s<=225


def fraction_with_spectral_ratio(ratio):
    """ratio = W-weighted mean nonnegative spectral strength (low/high)."""
    if not math.isfinite(ratio) or ratio < 0:
        raise ValueError('nonnegative finite ratio required')
    return F_W*ratio/(F_W*ratio+1-F_W)


def ratio_for_target(target):
    if not math.isfinite(target) or not 0 < target < 1:
        raise ValueError('target must be finite and between zero and one')
    return target*(1-F_W)/(F_W*(1-target))


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.folder = Path(self.dir.name)
        self.synthetic = {
            name: bytes([idx + 1])* (11+idx)
            for idx, name in enumerate(EXPECTED)
        }
        self.expected = {name: (len(data), git_blob_sha1(data))
                         for name, data in self.synthetic.items()}
        for name, data in self.synthetic.items():
            (self.folder/name).write_bytes(data)

    def test_streaming_git_blob_sha1(self):
        data = self.synthetic['hips_c1.txt']
        reference = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii')
                                 + b'\0' + data).hexdigest()
        self.assertEqual(git_blob_sha1(data), reference)
        self.assertEqual(git_blob_sha1(b''), hashlib.sha1(b'blob 0\0').hexdigest())

    def test_all_synthetic_files_valid(self):
        result = check_folder(self.folder, expected=self.expected, sample_bytes=4)
        self.assertEqual(len(result), 4)
        self.assertEqual(result['hips_c1.txt'][0], self.synthetic['hips_c1.txt'][:4])
        self.assertEqual(result['hips_c1.txt'][1], hashlib.sha256(self.synthetic['hips_c1.txt']).hexdigest())

    def test_modified_byte_rejected(self):
        path = self.folder/'hips_c1.txt'
        path.write_bytes(b'Z'+path.read_bytes()[1:])
        with self.assertRaisesRegex(ValueError, 'SHA-1 mismatch'):
            check_folder(self.folder, expected=self.expected)

    def test_truncation_rejected(self):
        path = self.folder/'hips_c2.txt'
        path.write_bytes(path.read_bytes()[:-1])
        with self.assertRaisesRegex(ValueError, 'byte count mismatch'):
            check_folder(self.folder, expected=self.expected)

    def test_missing_file_rejected(self):
        (self.folder/'hips_d2.txt').unlink()
        with self.assertRaises(FileNotFoundError):
            check_folder(self.folder, expected=self.expected)

    def test_symlink_rejected(self):
        path = self.folder/'hips_d1.txt'
        target = self.folder/'target.dat'
        target.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(target)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            check_folder(self.folder, expected=self.expected)

    def test_max_size_rejected(self):
        name = 'hips_c1.txt'
        with self.assertRaisesRegex(ValueError, 'file-size cap'):
            verify_file(self.folder/name, expected_size=self.expected[name][0],
                        expected_blob=self.expected[name][1], max_bytes=1)

    def test_invalid_manifest_name_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unsafe filename'):
            check_folder(self.folder, expected={'../escape': (1, '0'*40)})

    def test_sample_size_guard(self):
        name = 'hips_c1.txt'
        with self.assertRaisesRegex(ValueError, 'sample_bytes'):
            verify_file(self.folder/name, expected_size=self.expected[name][0],
                        expected_blob=self.expected[name][1], sample_bytes=300)


class SpectralSensitivityTests(unittest.TestCase):
    def test_unit_ratio_recovers_kinematic_fraction(self):
        self.assertAlmostEqual(fraction_with_spectral_ratio(1), F_W, places=14)

    def test_ratio_threshold_inversion(self):
        for target in (0.01, 0.1, 0.5, 0.9):
            self.assertAlmostEqual(fraction_with_spectral_ratio(ratio_for_target(target)),
                                   target, places=14)

    def test_ratio_10_and_100(self):
        self.assertAlmostEqual(fraction_with_spectral_ratio(10), 0.039902735, delta=1e-9)
        self.assertAlmostEqual(fraction_with_spectral_ratio(100), 0.293591437, delta=1e-9)

    def test_ratio_0_and_large(self):
        self.assertEqual(fraction_with_spectral_ratio(0), 0)
        self.assertGreater(fraction_with_spectral_ratio(1e12), 0.999999)

    def test_ratio_rejects_negative_or_nonfinite(self):
        for x in (-1, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                fraction_with_spectral_ratio(x)

    def test_target_rejects_boundary_and_nonfinite(self):
        for x in (0, 1, -0.1, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                ratio_for_target(x)


if __name__ == '__main__':
    print('f_W=', F_W)
    for target in (0.01, 0.1, 0.5, 0.9):
        print(f'weighted mean spectrum ratio needed for {target:.0%} contribution: {ratio_for_target(target):.9f}')
    unittest.main()
