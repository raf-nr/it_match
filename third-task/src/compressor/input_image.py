import numpy as np
from PIL import Image as Im

from src.compressor.compressed_image import CompressedImage
from src.params import Method
from src.svd.svd import SVD


class InputImage:

    def __init__(self, image: Im.Image):
        r, g, b = image.convert("RGB").split()

        self.image = image
        self.image_data = np.array(image)
        self.shape = self.image_data.shape[:2]
        self.r_channel = np.array(r)
        self.g_channel = np.array(g)
        self.b_channel = np.array(b)

    def _get_k(self, compress_factor: int) -> int:
        m, n = self.shape
        original_size = m * n * 3
        min_k = min(m, n)
        compressed_size = lambda k: 3 * (m * k + k + k * n) * 8
        return next((k for k in range(min_k, 1, -1) if original_size / compressed_size(k) >= compress_factor), min_k)

    def get_svd_channels(self, method_name: Method, compress_factor: int) -> CompressedImage:
        k = self._get_k(compress_factor)
        match method_name:
            case Method.NUMPY:
                svd_r = SVD.get_svd_numpy(self.r_channel, k)
                svd_g = SVD.get_svd_numpy(self.g_channel, k)
                svd_b = SVD.get_svd_numpy(self.b_channel, k)
                return CompressedImage(svd_r, svd_g, svd_b)
            case Method.SIMPLE:
                pass
            case Method.ADVANCED:
                pass
