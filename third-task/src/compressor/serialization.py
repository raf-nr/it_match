import struct
from pathlib import Path

import numpy as np

from src.compressor.compressed_image import CompressedImage
from src.params import FLOAT_SIZE
from src.svd.svd_result import SVDResult


class Serialization:

    @staticmethod
    def serialize(file_path: Path, compressed_image: CompressedImage) -> None:
        with open(file_path, 'wb') as f:
            # Write file marker
            f.write(b'MSVD')
            svd_channels = [compressed_image.r, compressed_image.g, compressed_image.b]
            # Write dimensions
            u_shape = svd_channels[0].u.shape
            s_shape = svd_channels[1].s.shape
            v_shape = svd_channels[2].v.shape

            # Write shapes
            f.write(struct.pack('III', u_shape[0], s_shape[0], v_shape[1]))

            # Write SVD results for each channel
            for svd_result in svd_channels:
                # Write data
                f.write(svd_result.u.astype(np.float32).flatten().tobytes())
                f.write(svd_result.s.astype(np.float32).flatten().tobytes())
                f.write(svd_result.v.astype(np.float32).flatten().tobytes())

    @staticmethod
    def deserialize(file_path: Path) -> CompressedImage:
        with open(file_path, 'rb') as file:
            # Read file marker
            marker = file.read(4)
            if marker != b'MSVD':
                raise ValueError("Invalid file format")

            # Read dimensions
            u_n, s_n, v_m = struct.unpack('III', file.read(3 * 4))

            svd_results = []
            for _ in range(3):
                # Read data
                u_data = np.frombuffer(file.read(u_n * s_n * FLOAT_SIZE), dtype=np.float32)
                s_data = np.frombuffer(file.read(s_n * FLOAT_SIZE), dtype=np.float32)
                v_data = np.frombuffer(file.read(s_n * v_m * FLOAT_SIZE), dtype=np.float32)

                u = np.reshape(u_data, (u_n, s_n))
                s = np.reshape(s_data, (s_n,))
                v = np.reshape(v_data, (s_n, v_m))

                svd_results.append(SVDResult(u, s, v))

            result = CompressedImage(svd_results[0], svd_results[1], svd_results[2])
            return result