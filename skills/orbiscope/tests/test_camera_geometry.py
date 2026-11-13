import math
import sys
import unittest
from pathlib import Path

scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

import geo


class CameraGeometryTests(unittest.TestCase):
    def test_focal_px_calculation(self):
        # 90 degree FOV with 1000px width -> (1000/2) / tan(45 deg) = 500 / 1 = 500
        f = geo.focal_px(1000.0, 90.0)
        self.assertAlmostEqual(f, 500.0)

    def test_focal_px_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            geo.focal_px(0.0, 90.0)
        with self.assertRaises(ValueError):
            geo.focal_px(-500.0, 90.0)
        with self.assertRaises(ValueError):
            geo.focal_px(1000.0, 0.0)
        with self.assertRaises(ValueError):
            geo.focal_px(1000.0, 180.0)
        with self.assertRaises(ValueError):
            geo.focal_px(1000.0, 190.0)
        with self.assertRaises(ValueError):
            geo.focal_px(float("nan"), 90.0)
        with self.assertRaises(ValueError):
            geo.focal_px(1000.0, float("nan"))

    def test_range_from_size_calculation(self):
        # Object 2m wide is 100px on sensor with f=500 -> 2 * 500 / 100 = 10m
        dist = geo.range_from_size(2.0, 100.0, 1000.0, 90.0)
        self.assertAlmostEqual(dist, 10.0)

    def test_range_from_size_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            geo.range_from_size(0.0, 100.0, 1000.0, 90.0)
        with self.assertRaises(ValueError):
            geo.range_from_size(-2.0, 100.0, 1000.0, 90.0)
        with self.assertRaises(ValueError):
            geo.range_from_size(2.0, 0.0, 1000.0, 90.0)
        with self.assertRaises(ValueError):
            geo.range_from_size(2.0, -10.0, 1000.0, 90.0)

    def test_angle_from_center(self):
        # Center point -> 0 deg
        self.assertAlmostEqual(geo.angle_from_center(500.0, 500.0, 1000.0, 90.0), 0.0)
        # Right edge (1000px, center 500px, f=500px) -> atan(1) = 45 deg
        self.assertAlmostEqual(geo.angle_from_center(1000.0, 500.0, 1000.0, 90.0), 45.0)

    def test_fov_from_equiv_focal_valid_and_guards(self):
        w_fov, h_fov = geo.fov_from_equiv_focal(24.0)
        self.assertGreater(w_fov, 0.0)
        self.assertGreater(h_fov, 0.0)
        with self.assertRaises(ValueError):
            geo.fov_from_equiv_focal(0.0)
        with self.assertRaises(ValueError):
            geo.fov_from_equiv_focal(-12.0)
        with self.assertRaises(ValueError):
            geo.fov_from_equiv_focal(24.0, (-4, 3))


if __name__ == "__main__":
    unittest.main()
