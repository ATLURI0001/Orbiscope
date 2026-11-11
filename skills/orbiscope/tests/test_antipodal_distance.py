import math
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import geo


def test_distance_antipodal_no_domain_error():
    # Exact antipodal equator points previously risked h > 1.0 float overshoot -> ValueError
    d = geo.distance((0.0, 0.0), (0.0, 180.0))
    assert math.isclose(d, math.pi * geo._R, rel_tol=1e-9)

    # Arbitrary near-antipodal points must remain finite
    d2 = geo.distance((37.774929, -122.419416), (-37.774929, 57.580584))
    assert math.isfinite(d2)
    assert d2 > 20_000_000.0


def test_vincenty_distance_precision_and_antipodal_fallback():
    # Identical points -> 0.0
    assert geo.vincenty_distance((22.6, 114.0), (22.6, 114.0)) == 0.0

    # Short baseline sanity vs spherical distance (Seattle to Portland ~233 km)
    seattle = (47.6062, -122.3321)
    portland = (45.5152, -122.6784)
    v_dist = geo.vincenty_distance(seattle, portland)
    h_dist = geo.distance(seattle, portland)
    assert math.isclose(v_dist, h_dist, rel_tol=0.005)

    # Exact antipodal equator triggers clean fallback to finite spherical distance
    antipodal = geo.vincenty_distance((0.0, 0.0), (0.0, 180.0))
    assert math.isfinite(antipodal)
    assert antipodal > 20_000_000.0
