import numpy as np
from PIL import Image

from src.svd.svd_result import SVDResult


class CompressedImage:

    def __init__(self, r_svd: SVDResult, g_svd: SVDResult, b_svd: SVDResult):
        self.r = r_svd
        self.g = g_svd
        self.b = b_svd

    def _svd_to_channel(self, svd: SVDResult) -> np.ndarray:
        return svd.u @ np.diag(svd.s) @ svd.v

    def get_image(self):
        rgb_list = [self._svd_to_channel(self.r), self._svd_to_channel(self.g), self._svd_to_channel(self.b)]
        merged = np.clip(np.dstack(rgb_list), 0, 255).astype(np.uint8)
        return Image.fromarray(merged, mode='RGB')