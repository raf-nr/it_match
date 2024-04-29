import numpy as np

from src.svd.svd_result import SVDResult


class SVD:

    @staticmethod
    def get_svd_numpy(init_matrix: np.ndarray, k: int) -> SVDResult:
        u, s, v = np.linalg.svd(init_matrix, full_matrices=False)
        return SVDResult(u, s, v, k)
