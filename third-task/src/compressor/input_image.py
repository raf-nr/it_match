import math
import os
from pathlib import Path

import numpy as np
from PIL import Image as Im

from src.compressor.compressed_image import CompressedImage
from src.params import Method, FLOAT_SIZE
from src.svd.svd import SVD


class InputImage:

    def __init__(self, input_name: Path):
        image = Im.open(input_name)
        r, g, b = image.convert("RGB").split()

        self.image = image
        self.size = os.path.getsize(input_name)
        self.image_data = np.array(image)
        self.m, self.n = self.image_data.shape[:2]
        self.r_channel = np.array(r)
        self.g_channel = np.array(g)
        self.b_channel = np.array(b)

    def _get_k(self, compression: float):
        new_size = self.size / compression
        k = math.floor((new_size - 3 * FLOAT_SIZE) / (3 * FLOAT_SIZE * (self.n + 1 + self.m)))
        return k

    def get_svd_channels(self, method_name: Method, compress_factor: float) -> CompressedImage:
        k = self._get_k(compress_factor)
        match method_name:
            case Method.NUMPY:
                get_svd = SVD.get_svd_numpy
            case Method.SIMPLE:
                get_svd = SVD.get_svd_simple
            case Method.ADVANCED:
                get_svd = SVD.get_svd_advanced
        svd_r = get_svd(self.r_channel, k)
        svd_g = get_svd(self.g_channel, k)
        svd_b = get_svd(self.b_channel, k)
        return CompressedImage(svd_r, svd_g, svd_b)