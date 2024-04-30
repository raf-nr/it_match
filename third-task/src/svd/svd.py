import numpy as np

from src.params import SIMPLE, ADVANCED
from src.svd.svd_result import SVDResult


class SVD:

    @staticmethod
    def get_svd_numpy(init_matrix: np.ndarray, k: int) -> SVDResult:
        u, s, v = np.linalg.svd(init_matrix, full_matrices=False)
        result = SVDResult(u, s, v)
        result.apply_k(k)
        return result

    @staticmethod
    def _singular_vector_for_simple_svd(init_matrix, eps):
        m, n = init_matrix.shape
        v = np.random.normal(0, 1, size=n)

        while True:
            l_v = v
            v = init_matrix.T @ init_matrix @ v
            v = v / np.linalg.norm(v) if np.linalg.norm(v) > 0 else v
            if (abs(v @ l_v) > 1 - eps) or np.linalg.norm(v) == 0:
                break

        sigma = np.linalg.norm(init_matrix @ v)
        u = (init_matrix @ v) / sigma
        return np.reshape(u, (m, 1)), sigma, v.reshape(1, n)
    @staticmethod
    def get_svd_simple(init_matrix: np.ndarray, k: int) -> SVDResult:
        init_matrix = init_matrix.astype(np.float64)
        u_list = []
        s_list = []
        v_list = []

        for _ in range(min(init_matrix.shape)):
            u, s, v = SVD._singular_vector_for_simple_svd(init_matrix, SIMPLE)
            u_list.append(u)
            s_list.append(s)
            v_list.append(v)
            init_matrix -= (u @ v) * s

        u = np.hstack(u_list)
        s = np.array(s_list)
        v = np.vstack(v_list)

        result = SVDResult(u, s, v)
        result.apply_k(k)
        return result

    @staticmethod
    def get_svd_advanced(init_matrix: np.ndarray, k: float, tolerance: int = ADVANCED) -> SVDResult:
        m, n = init_matrix.shape
        err = tolerance + 1
        v = np.random.normal(0, 1, (n, m))

        while True:
            qr1 = np.linalg.qr(init_matrix @ v)
            u = qr1.Q[:, :k]
            qr2 = np.linalg.qr(init_matrix.T @ u)
            v = qr2.Q[:, :k]
            s = qr2.R[:k, :k]
            err = np.linalg.norm(init_matrix @ v - u @ s)
            if tolerance < err:
                break
        result = SVDResult(u, np.diag(s), v.T)
        return result
