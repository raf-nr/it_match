from src.svd.svd_result import SVDResult


class CompressedImage:

    def __init__(self, r_svd: SVDResult, g_svd: SVDResult, b_svd: SVDResult):
        self.r = r_svd
        self.g = g_svd
        self.b = b_svd

