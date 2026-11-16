# Multi-Stage Geolocation Inference Pipeline Guide

## Pipeline Architecture
1. **Visual Feature Extraction**: Architectural style, vegetation flora classification, road infrastructure markers, signage script detection.
2. **Environmental Priors**: Shadow azimuth, sun angle estimation, approximate latitude bounds.
3. **Geographic Cross-Referencing**: Intersecting visual classifications against OpenStreetMap tags and satellite elevation contours.
4. **Candidate Ranking**: Confidence scoring over candidate coordinates with uncertainty bounding ellipses.
