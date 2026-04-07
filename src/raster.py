from pathlib import Path

import numpy as np
import rasterio
from affine import Affine
from skimage.transform import resize as sk_resize


def load_tif(path, bands=(1, 2, 3), resize=1, normalize=True):
    path = Path(path)

    with rasterio.open(path) as src:
        crs = src.crs
        transform = src.transform

        img = src.read(bands).astype(np.float32)
        img = np.transpose(img, (1, 2, 0)) 

    if normalize:
        img = img / (img.max() + 1e-9)

    if resize > 1:
        h, w = img.shape[:2]
        new_h = h // resize
        new_w = w // resize

        img = np.asarray(
            sk_resize(
                img,
                (new_h, new_w, img.shape[2]),
                order=1,
                preserve_range=True,
                anti_aliasing=True,
            )
        ).astype(np.float32)

        transform = transform * Affine.scale(resize, resize)

    return img, crs, transform