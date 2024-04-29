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