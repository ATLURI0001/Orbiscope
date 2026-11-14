import argparse
import unittest
import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

import geo


class GeoCoordsTests(unittest.TestCase):
    def test_pair_valid_coordinates(self):
        lat, lon = geo._pair("22.6045,114.0520")
        self.assertAlmostEqual(lat, 22.6045)
        self.assertAlmostEqual(lon, 114.0520)

    def test_pair_handles_whitespace(self):
        lat, lon = geo._pair("  -33.8688 ,  151.2093  ")
        self.assertAlmostEqual(lat, -33.8688)
        self.assertAlmostEqual(lon, 151.2093)

    def test_pair_rejects_malformed_formats(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            geo._pair("single_value")
        with self.assertRaises(argparse.ArgumentTypeError):
            geo._pair("10,20,30")
        with self.assertRaises(argparse.ArgumentTypeError):
            geo._pair("abc,def")

    def test_pair_rejects_out_of_bounds_lat_lon(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            geo._pair("91.0,0.0")
        with self.assertRaises(argparse.ArgumentTypeError):
            geo._pair("-90.5,0.0")
        with self.assertRaises(argparse.ArgumentTypeError):
            geo._pair("0.0,181.0")
        with self.assertRaises(argparse.ArgumentTypeError):
            geo._pair("0.0,-185.0")

    def test_dest_antimeridian_wrap(self):
        # Walking east across the antimeridian (+180/-180)
        start = (0.0, 179.999)
        # Walk 500 meters east (bearing 90)
        end_lat, end_lon = geo.dest(start, 90.0, 500.0)
        self.assertGreaterEqual(end_lon, -180.0)
        self.assertLessEqual(end_lon, 180.0)

    def test_distance_and_bearing_basic(self):
        p1 = (0.0, 0.0)
        p2 = (0.0, 1.0)
        d = geo.distance(p1, p2)
        b = geo.bearing(p1, p2)
        self.assertAlmostEqual(b, 90.0, places=1)
        self.assertGreater(d, 100000.0)

    def test_dest_validation_and_negative_distance(self):
        with self.assertRaises(ValueError):
            geo.dest((0.0, 0.0), 90.0, -100.0)
        with self.assertRaises(ValueError):
            geo.dest((float("nan"), 0.0), 90.0, 100.0)
        with self.assertRaises(ValueError):
            geo.dest((0.0, 0.0), float("inf"), 100.0)

    def test_midpoint_calculation_and_antimeridian(self):
        # Basic equator midpoint
        p1 = (0.0, 0.0)
        p2 = (0.0, 10.0)
        mid = geo.midpoint(p1, p2)
        self.assertAlmostEqual(mid[0], 0.0)
        self.assertAlmostEqual(mid[1], 5.0)

        # Equal distance from midpoint to endpoints
        d1 = geo.distance(p1, mid)
        d2 = geo.distance(mid, p2)
        self.assertAlmostEqual(d1, d2, places=1)

        # Antimeridian midpoint across 180 degrees
        p_west = (0.0, 179.0)
        p_east = (0.0, -179.0)
        mid_anti = geo.midpoint(p_west, p_east)
        self.assertAlmostEqual(mid_anti[0], 0.0)
        self.assertAlmostEqual(abs(mid_anti[1]), 180.0)

        # Error on NaN
        with self.assertRaises(ValueError):
            geo.midpoint((float("nan"), 0.0), (0.0, 0.0))



if __name__ == "__main__":
    unittest.main()
