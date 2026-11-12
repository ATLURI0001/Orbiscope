import math
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import geo
import board


def test_normalize_lon():
    assert geo.normalize_lon(0) == 0
    assert geo.normalize_lon(180) == -180
    assert geo.normalize_lon(-180) == -180
    assert geo.normalize_lon(185) == -175
    assert geo.normalize_lon(-185) == 175


def test_clamp_lat():
    assert geo.clamp_lat(45.0) == 45.0
    assert geo.clamp_lat(95.0) == 90.0
    assert geo.clamp_lat(-95.0) == -90.0


def test_bbox_lon_span():
    # Standard non-crossing span
    assert math.isclose(geo.bbox_lon_span(10.0, 20.0), 10.0)
    # Anti-meridian crossing span (e.g. 179 to -179 is 2 degrees, not 358)
    assert math.isclose(geo.bbox_lon_span(179.0, -179.0), 2.0)
    # 175 to -175 is 10 degrees
    assert math.isclose(geo.bbox_lon_span(175.0, -175.0), 10.0)


def test_bbox_km2_antimeridian():
    # Normal 1x1 degree box near equator
    area_normal = geo.bbox_km2([-0.5, 0.0, 0.5, 1.0])
    # Same 1x1 degree box crossing anti-meridian [179.5 to -179.5]
    area_crossing = geo.bbox_km2([-0.5, 179.5, 0.5, -179.5])
    assert math.isclose(area_normal, area_crossing, rel_tol=1e-3)


def test_point_in_bbox_antimeridian():
    # Box crossing anti-meridian from 178 to -178 (lat -10 to 10)
    bbox = [-10.0, 178.0, 10.0, -178.0]

    # Point at 179 is inside
    assert geo.point_in_bbox([0.0, 179.0], bbox) is True
    # Point at -179 is inside
    assert geo.point_in_bbox([0.0, -179.0], bbox) is True
    # Point at 180 is inside
    assert geo.point_in_bbox([0.0, 180.0], bbox) is True
    # Point at 100 is outside
    assert geo.point_in_bbox([0.0, 100.0], bbox) is False
    # Point at 0 is outside
    assert geo.point_in_bbox([0.0, 0.0], bbox) is False
    # Point with out-of-range latitude is outside
    assert geo.point_in_bbox([15.0, 179.0], bbox) is False


def test_board_inside_and_pages_antimeridian():
    c = {"bbox": [-10.0, 178.0, 10.0, -178.0]}
    assert board._inside(c, 0.0, 179.0) is True
    assert board._inside(c, 0.0, -179.0) is True
    assert board._inside(c, 0.0, 50.0) is False

    # Check pages calculation across anti-meridian is reasonable and positive
    pages = board._pages(c["bbox"], zoom=14, cell=640, cols=4)
    assert pages > 0
    assert pages < 100_000  # previously would calculate negative or absurd numbers


def test_full_globe_lon_span_and_padded_antimeridian_bbox():
    # Full [-180, 180] longitude span must be 360 degrees, not 0
    assert math.isclose(geo.bbox_lon_span(-180.0, 180.0), 360.0)
    assert math.isclose(geo.bbox_lon_span(10.0, 10.0), 0.0)
    assert geo.bbox_km2([-1.0, -180.0, 1.0, 180.0]) > 1_000_000.0

    # Padding crossing -180 should match points on the +180 side within pad_m
    bbox_near_dateline = [-1.0, -179.99, 1.0, -179.0]
    assert geo.point_in_bbox([0.0, 179.98], bbox_near_dateline, pad_m=5000.0) is True
    assert geo.point_in_bbox([0.0, 170.0], bbox_near_dateline, pad_m=5000.0) is False

