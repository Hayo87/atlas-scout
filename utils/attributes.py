from rasterstats import zonal_stats
import numpy as np

def compute_geometry_attributes(segments_gdf):
    """
    Add simple geometry-based attributes to the segment GeoDataFrame.
    """
    segments_gdf = segments_gdf.copy()

    segments_gdf["area"] = segments_gdf.geometry.area
    segments_gdf["perimeter"] = segments_gdf.geometry.length
    segments_gdf["centroid"] = segments_gdf.geometry.centroid

    segments_gdf["compactness"] = (
        4 * np.pi * segments_gdf["area"] /
        (segments_gdf["perimeter"] ** 2 + 1e-9)
    )

    bounds = segments_gdf.geometry.bounds
    segments_gdf["bbox_width"] = bounds["maxx"] - bounds["minx"]
    segments_gdf["bbox_height"] = bounds["maxy"] - bounds["miny"]
    segments_gdf["aspect_ratio"] = (
        segments_gdf["bbox_width"] / (segments_gdf["bbox_height"] + 1e-9)
    )

    return segments_gdf

def compute_image_attributes(segments_gdf):
    """
    Add simple image-derived summary attributes to the segment GeoDataFrame.
    """
    segments_gdf = segments_gdf.copy()

    segments_gdf["brightness"] = (
        segments_gdf["band_1_mean"] +
        segments_gdf["band_2_mean"] +
        segments_gdf["band_3_mean"]
    ) / 3

    segments_gdf["texture_score"] = (
        segments_gdf["band_1_std"] +
        segments_gdf["band_2_std"] +
        segments_gdf["band_3_std"]
    ) / 3

    return segments_gdf

def compute_raster_attributes(segments_gdf, raster_path, stats=("mean", "std"), prefix="raster"):
    """
    Add zonal statistics from a raster to each segment.

    Parameters
    ----------
    segments_gdf : gpd.GeoDataFrame
        Segment polygons.
    raster_path : str or Path
        Raster to summarize over each segment.
    stats : tuple[str], default=("mean", "std")
        Zonal statistics to compute.
    prefix : str, default="raster"
        Prefix for output column names.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame with added raster-derived attributes.
    """
    segments_gdf = segments_gdf.copy()

    zs = zonal_stats(
        segments_gdf,
        str(raster_path),
        stats=list(stats),
    )

    for stat in stats:
        segments_gdf[f"{prefix}_{stat}"] = [row.get(stat) for row in zs]

    return segments_gdf