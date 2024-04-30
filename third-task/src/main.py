from src.compressor.compressor import Compressor
from src.params import Method
from src.parser.parser import get_parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    match args.mode:
        case "compress":
            if args.method not in {"numpy", "simple", "advanced"}:
                raise ValueError("Invalid method specified.")
            if not args.compression:
                raise ValueError("Compression level not specified.")
            if not args.in_file or not args.out_file:
                raise ValueError("Input or output file not specified.")

            match args.method:
                case "numpy":
                    Compressor.compress(args.in_file, args.out_file, args.compression, Method.NUMPY)
                case "simple":
                    Compressor.compress(args.in_file, args.out_file, args.compression, Method.SIMPLE)
                case "advanced":
                    Compressor.compress(args.in_file, args.out_file, args.compression, Method.ADVANCED)

        case "decompress":
            if not args.in_file or not args.out_file:
                raise ValueError("Input or output file not specified.")
            Compressor.decompress(args.in_file, args.out_file)

        case _:
            raise ValueError("Invalid mode specified.")
