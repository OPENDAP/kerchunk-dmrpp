#!/usr/bin/env python3
"""
Generate a 1024x1024 GeoTIFF with an easily verifiable data pattern
(alternating rows of 0 and 1), compressed with 'deflate'.

Uses tifffile (available in the kerchunk_env conda environment) rather
than requiring GDAL/rasterio. Writes minimal but valid GeoTIFF georeferencing
tags (geographic, WGS84) so the file is recognized as a real GeoTIFF by
gdalinfo/QGIS/etc.

Run with:
    conda run -n kerchunk_env python3 make_test_geotiff.py
"""

import numpy as np
import tifffile

WIDTH = 1024
HEIGHT = 1024
OUTPUT_PATH = "test_pattern_1024_deflate.tif"

# Upper-left corner and pixel size for the geographic (WGS84) reference.
# Values are arbitrary but plausible (a 1x1 degree scene near 0,0).
ORIGIN_LON = -10.0
ORIGIN_LAT = 10.0
PIXEL_SIZE_X = 1.0 / WIDTH
PIXEL_SIZE_Y = 1.0 / HEIGHT

# GeoTIFF tag IDs (see the GeoTIFF spec)
TAG_MODEL_PIXEL_SCALE = 33550
TAG_MODEL_TIEPOINT = 33922
TAG_GEO_KEY_DIRECTORY = 34735


def build_pattern(width, height, dtype=np.uint8):
    """Row i is filled entirely with (i % 2): rows alternate 0, 1, 0, 1, ..."""
    row_values = (np.arange(height, dtype=dtype) % 2).astype(dtype)
    return np.repeat(row_values[:, np.newaxis], width, axis=1)


def geotiff_extratags():
    # ModelPixelScaleTag: (ScaleX, ScaleY, ScaleZ)
    pixel_scale = (TAG_MODEL_PIXEL_SCALE, "d", 3,
                   (PIXEL_SIZE_X, PIXEL_SIZE_Y, 0.0), False)

    # ModelTiepointTag: (I, J, K, X, Y, Z) - pixel (0,0) maps to (ORIGIN_LON, ORIGIN_LAT)
    tiepoint = (TAG_MODEL_TIEPOINT, "d", 6,
                (0.0, 0.0, 0.0, ORIGIN_LON, ORIGIN_LAT, 0.0), False)

    # GeoKeyDirectoryTag: minimal set of keys declaring a geographic (lon/lat)
    # coordinate system using WGS84 (EPSG:4326).
    geo_keys = (
        1, 1, 0, 4,        # KeyDirectoryVersion, KeyRevision, MinorRevision, NumberOfKeys
        1024, 0, 1, 2,     # GTModelTypeGeoKey = 2 (Geographic)
        1025, 0, 1, 1,     # GTRasterTypeGeoKey = 1 (RasterPixelIsArea)
        2048, 0, 1, 4326,  # GeographicTypeGeoKey = 4326 (WGS84)
        2054, 0, 1, 9102,  # GeogAngularUnitsGeoKey = 9102 (degree)
    )
    geo_key_directory = (TAG_GEO_KEY_DIRECTORY, "H", len(geo_keys), geo_keys, False)

    return [pixel_scale, tiepoint, geo_key_directory]


def main():
    data = build_pattern(WIDTH, HEIGHT, dtype=np.uint8)

    tifffile.imwrite(
        OUTPUT_PATH,
        data,
        photometric="minisblack",
        compression="deflate",
        tile=(256, 256),
        extratags=geotiff_extratags(),
        software="make_test_geotiff.py",
    )

    print(f"Wrote {OUTPUT_PATH}: {data.shape[1]}x{data.shape[0]}, dtype={data.dtype}, "
          f"compression=deflate")


if __name__ == "__main__":
    main()
