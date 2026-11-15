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

    def test_cross_track_and_along_track_distance(self):
        # Equatorial path going due east from (0,0) to (0,10)
        start = (0.0, 0.0)
        end = (0.0, 10.0)

        # Point directly on path at (0, 5)
        on_path = (0.0, 5.0)
        xt_zero = geo.cross_track_distance(on_path, start, end)
        at_mid = geo.along_track_distance(on_path, start, end)
        self.assertAlmostEqual(xt_zero, 0.0, places=1)
        self.assertAlmostEqual(at_mid, geo.distance(start, on_path), places=1)

        # Point 1 degree north (to the left of track, so signed negative)
        north_pt = (1.0, 5.0)
        xt_north = geo.cross_track_distance(north_pt, start, end)
        self.assertLess(xt_north, 0.0)
        self.assertAlmostEqual(abs(xt_north), geo.distance((0.0, 5.0), north_pt), delta=500.0)

        # Point behind start: along-track is negative
        behind_pt = (0.0, -2.0)
        at_behind = geo.along_track_distance(behind_pt, start, end)
        self.assertLess(at_behind, 0.0)

        # Coincident start/end fallback
        self.assertEqual(geo.along_track_distance(on_path, start, start), 0.0)
        self.assertAlmostEqual(geo.cross_track_distance(on_path, start, start), geo.distance(on_path, start), places=1)

        # Non-finite inputs raise ValueError
        with self.assertRaises(ValueError):
            geo.cross_track_distance((float("nan"), 0.0), start, end)


if __name__ == "__main__":
    unittest.main()
