import os

from PIL import Image

from src.compressor.input_image import InputImage
from src.params import Method

# from src.compressor.compressor import Compressor

if __name__ == '__main__':
    image = Image.open('images/first.bmp')
    imageObj = InputImage(image)
    print(imageObj.shape)
    print(imageObj.get_svd_channels(Method.NUMPY, 2).g.v)
    # size = os.path.getsize('src/first.bmp')
    # Compressor.compress(image, 3, size)
    # Compressor.decompress()
    # # in_channels = image.convert("RGB").split()
    # # print(in_channels[0])
    # # print(numpy.array(in_channels[0]))
    # # print(numpy.array(in_channels[1]))
    # # print(numpy.array(in_channels[2]))