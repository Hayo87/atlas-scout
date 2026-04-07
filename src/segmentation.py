
import numpy as np
import pandas as pd
import geopandas as gpd

from skimage.segmentation import felzenszwalb

from rasterio.features import shapes
from shapely.geometry import shape


def build_segments(img, scale=250, sigma=0.5, min_size=150):
    """
    Build image segments from an input image.

    Parameters
    ----------
    img : np.ndarray
        Input image as (H, W, C).
    scale : float, default=250
        Higher values give larger segments.
    sigma : float, default=0.5
        Smoothing before segmentation.
    min_size : int, default=150
        Minimum segment size in pixels.

    Returns
    -------
    np.ndarray
        2D integer label image with one segment ID per pixel.
    """
    return felzenszwalb(
        img,
        scale=scale,
        sigma=sigma,
        min_size=min_size,
    ).astype(np.int32)

def segment_attributes(img, segments):
    """
    Compute simple per-segment attributes from the image.

    Parameters
    ----------
    img : np.ndarray
        Input image as (H, W, C).
    segments : np.ndarray
        2D label array with one segment ID per pixel.

    Returns
    -------
    pd.DataFrame
        Table with one row per segment and summary statistics.
    """
    rows = []

    for seg_id in np.unique(segments):
        mask = segments == seg_id
        pixels = img[mask]

        row = {
            "segment_id": int(seg_id),
            "pixel_count": int(mask.sum()),
        }

        for b in range(pixels.shape[1]):
            row[f"band_{b+1}_mean"] = float(pixels[:, b].mean())
            row[f"band_{b+1}_std"] = float(pixels[:, b].std())

        rows.append(row)

    return pd.DataFrame(rows)

def segments_to_gdf(segments, transform, crs):
    """
    Convert segment labels into polygons stored in a GeoDataFrame.

    Parameters
    ----------
    segments : np.ndarray
        2D label array with one segment ID per pixel.
    transform : affine.Affine
        Spatial transform for the raster.
    crs : rasterio.crs.CRS
        Coordinate reference system.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame with one polygon per segment.
    """
    geoms = []

    for geom, value in shapes(segments.astype(np.int32), transform=transform):
        geoms.append({
            "segment_id": int(value),
            "geometry": shape(geom),
        })

    return gpd.GeoDataFrame(geoms, crs=crs)