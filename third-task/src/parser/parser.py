import argparse as ap


def get_parser():

    parser = ap.ArgumentParser(description='Image compression/decompression tool.')
    parser.add_argument('--mode', '-m', choices=['compress', 'decompress'], required=True,
                        help='Mode: compress or decompress.')
    parser.add_argument('--method', '-mt', choices=['numpy', 'simple', 'advanced'],
                        help='Method for singular value decomposition (required if --mode=compress).')
    parser.add_argument('--compression', '-c', type=int,
                        help='Compression factor (required if --mode=compress).')
    parser.add_argument('--in_file', '-i', required=True,
                        help='Input file path.')
    parser.add_argument('--out_file', '-o', required=True,
                        help='Output file path.')
    return parser

