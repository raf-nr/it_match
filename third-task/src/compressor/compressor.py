from pathlib import Path

from PIL import Image

from src.compressor.input_image import InputImage
from src.compressor.serialization import Serialization
from src.params import Method


class Compressor:

    @staticmethod
    def compress(input_name: Path, output_name: Path, n: float, method: Method):
        input_name = Path(input_name)
        output_name = Path(output_name)
        if input_name.suffix != '.bmp':
            raise ValueError("Input file must be a .bmp image")
        image = InputImage(input_name)
        svd_channels = image.get_svd_channels(method, n)
        Serialization.serialize(output_name, svd_channels)

    @staticmethod
    def decompress(input_name: Path, output_name: Path):
        input_name = Path(input_name)
        output_name = Path(output_name)
        if output_name.suffix != '.bmp':
            output_name = output_name.with_suffix('.bmp')
        svd_channels = Serialization.deserialize(input_name)
        image = svd_channels.get_image()
        image.save(output_name)
