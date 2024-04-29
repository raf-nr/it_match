from pathlib import Path

from PIL import Image

from src.compressor.input_image import InputImage
from src.compressor.serialization import Serialization
from src.params import Method


class Compressor:

    @staticmethod
    def compress(input_name: Path, output_name: Path, n: int, method: Method):
        image = InputImage(input_name)
        svd_channels = image.get_svd_channels(method, n)
        Serialization.serialize(output_name, svd_channels)

    @staticmethod
    def decompress(input_name: Path, output_name: Path):
        svd_channels = Serialization.deserialize(input_name)
        image = svd_channels.regular_channels()
        image.save(output_name)
