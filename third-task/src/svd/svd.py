import numpy as np

from src.svd.svd_result import SVDResult


class SVD:

    @staticmethod
    def get_svd_numpy(init_matrix: np.ndarray, k: int) -> SVDResult:
        u, s, v = np.linalg.svd(init_matrix, full_matrices=False)
        result = SVDResult(u, s, v)
        result.apply_k(k)
        return result

    @staticmethod
    def get_svd_simple(init_matrix: np.ndarray, k: int) -> SVDResult:
        u, s, v = np.linalg.svd(init_matrix, full_matrices=False)
        result = SVDResult(u, s, v)
        result.apply_k(k)
        return result

    @staticmethod
    def get_svd_advanced(init_matrix: np.ndarray, k: int) -> SVDResult:
        u, s, v = np.linalg.svd(init_matrix, full_matrices=False)
        result = SVDResult(u, s, v)
        result.apply_k(k)
        return result