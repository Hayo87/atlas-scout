from pathlib import Path

import numpy as np
import rasterio
from affine import Affine


def load_tif(path, resize=1, bands=(1, 2, 3), normalize=True):
    """
    Load a TIFF as an image array, with optional downsampling.

    Parameters
    ----------
    path : str or Path
        Path to the TIFF file.
    resize : int, default=1
        Downsampling factor. If > 1, keeps every nth pixel in row/col.
    bands : tuple[int], default=(1, 2, 3)
        Band indices to read.
    normalize : bool, default=True
        If True, scales image values to [0, 1] using the image max.

    Returns
    -------
    img : np.ndarray
        Image array of shape (H, W, C).
    crs : rasterio.crs.CRS
        Coordinate reference system.
    transform : affine.Affine
        Affine transform for the returned image.
    """
    path = Path(path)

    with rasterio.open(path) as src:
        crs = src.crs
        transform = src.transform

        img = src.read(bands).astype(np.float32)
        img = np.transpose(img, (1, 2, 0))  # (bands, H, W) -> (H, W, bands)

    if normalize:
        img = img / (img.max() + 1e-9)

    if resize > 1:
        img = img[::resize, ::resize]
        transform = transform * Affine.scale(resize, resize)

    return img, crs, transform