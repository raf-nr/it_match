# import math
# import struct
# from enum import StrEnum, auto
# from pathlib import Path
# from typing import Tuple
#
# import numpy as np
# from PIL.Image import Image
# from PIL import Image as im
#
# from src.svd.svd import NumpySVD
# from src.svd.svd import SVDResult
# MODE = "RGB"
# NUMBER_OF_CHANNELS = len(MODE)
# INT_SIZE = 4
# FLOAT_SIZE = 4
# class Method(StrEnum):
#     NUMPY = auto()
#
# class Channel:
#
#     @staticmethod
#     def get_k(raw_size: int, compression: float, shape: Tuple[int, int]):
#         new_size = raw_size / compression
#         n, m = shape
#         k = (new_size - 3 * INT_SIZE) / (NUMBER_OF_CHANNELS * FLOAT_SIZE * (n + 1 + m))
#         if k < 1:
#             raise ValueError(
#                 "Compression factor too high, maximum is",
#                 raw_size / (NUMBER_OF_CHANNELS * FLOAT_SIZE * (n + 1 + m) + 3 * INT_SIZE),
#             )
#         return math.floor(k)
#
#     @staticmethod
#     def get_initial_channels(image: Image) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
#         r, g, b = image.convert("RGB").split()
#         return np.array(r), np.array(g), np.array(b)
#
#     @staticmethod
#     def get_svd_channels(initial_channels: Tuple[np.ndarray, np.ndarray, np.ndarray], method_name: Method, k: int) -> Tuple[SVDResult, SVDResult, SVDResult]:
#         r, g, b = initial_channels
#         match method_name:
#             case Method.NUMPY:
#                 svd_r = NumpySVD.get_svd(r)
#                 svd_r.change_under_k(k)
#                 svd_g = NumpySVD.get_svd(g)
#                 svd_g.change_under_k(k)
#                 svd_b = NumpySVD.get_svd(b)
#                 svd_b.change_under_k(k)
#         return svd_r, svd_g, svd_b
#
#
# class Serialization:
#
#     @staticmethod
#     def serialize(file_path: Path, svd_results: Tuple[SVDResult, SVDResult, SVDResult]):
#         with open(file_path, 'wb') as file:
#             # Write file marker
#             file.write(b'MSVD')
#             # Write dimensions
#             u_shape = svd_results[0].u.shape
#             s_shape = svd_results[0].s.shape
#             v_shape = svd_results[0].v.shape
#
#             # Write shapes
#             file.write(struct.pack('III', u_shape[0], s_shape[0], v_shape[1]))
#
#             # Write SVD results for each channel
#             for svd_result in svd_results:
#                 # Write data
#                 file.write(svd_result.u.flatten().tobytes())
#                 file.write(svd_result.s.flatten().tobytes())
#                 file.write(svd_result.v.flatten().tobytes())
#
#     @staticmethod
#     def deserialize(file_path: Path) -> Tuple[SVDResult, SVDResult, SVDResult]:
#         with open(file_path, 'rb') as file:
#             # Read file marker
#             marker = file.read(4)
#             if marker != b'MSVD':
#                 raise ValueError("Invalid file format")
#
#             # Read dimensions
#             u_n, s_n, v_m = struct.unpack('III', file.read(3 * 4))
#
#             svd_results = []
#             for _ in range(3):
#                 # Read data
#                 u_data = np.frombuffer(file.read(u_n * s_n * FLOAT_SIZE), dtype=np.float32)
#                 s_data = np.frombuffer(file.read(s_n * FLOAT_SIZE), dtype=np.float32)
#                 v_data = np.frombuffer(file.read(s_n * v_m * FLOAT_SIZE), dtype=np.float32)
#
#                 u = np.reshape(u_data, (u_n, s_n))
#                 s = np.reshape(s_data, (s_n,))
#                 v = np.reshape(v_data, (s_n, v_m))
#
#                 svd_results.append(SVDResult(u, s, v))
#
#             return tuple(svd_results)
#
# class Compressor:
#
#     @staticmethod
#     def svd_to_matrix(svd: SVDResult) -> np.ndarray:
#         return svd.u @ np.diag(svd.s) @ svd.v
#
#     @staticmethod
#     def save_image(out_file: Path, image: im.Image):
#         FORMAT = "PNG"
#         try:
#             image.save(out_file)
#         except ValueError:
#             image.save(out_file, format=FORMAT)
#     @staticmethod
#     # def compress(image: Image, l: int, method_name, size):
#     def compress(image: Image, l: int, size):
#         channels = Channel.get_initial_channels(image)
#         k = Channel.get_k(size, l, channels[0].shape)
#         result = Channel.get_svd_channels(channels, Method.NUMPY, k)
#         Serialization.serialize("src/pizda.sss", result)
#
#     @staticmethod
#     def decompress():
#         r, g, b = Serialization.deserialize("src/pizda.sss")
#         R = Compressor.svd_to_matrix(r)
#         G = Compressor.svd_to_matrix(g)
#         B = Compressor.svd_to_matrix(b)
#         print(G)
# #         f = np.dstack((R, G, B)).astype(np.uint8)
# #         image = im.fromarray(f, mode='RGB')
# #         Compressor.save_image('src/ppp.bmp', image)