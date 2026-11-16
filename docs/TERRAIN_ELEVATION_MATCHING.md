# Digital Elevation Model (DEM) & Horizon Profile Matching

## Horizon Extraction
1. Extract horizon profile curve from landscape images using edge detection and depth gradient filters.
2. Generate synthetic 360-degree horizon silhouettes from SRTM 30m Digital Elevation Model rasters.
3. Compute 2D cross-correlation to find optimal camera azimuth and geographic coordinates.
