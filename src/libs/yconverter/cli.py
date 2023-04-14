from argparse import ArgumentParser
from sys import stdout

from .client import YConverter


def main():
    parser = ArgumentParser(description="All fiat currency and crypto converter")
    parser.add_argument(
        "arguments", nargs="+", help="Amount source destination (1 usd try)"
    )
    parser.add_argument(
        "-k", "--key", help="Free api key for https://openexchangerates.org/signup/free"
    )

    args = parser.parse_args()
    arguments = args.arguments
    if len(arguments) != 3:
        raise ValueError("Valid format: amount source destination (1 usd try)")
    amount, source, destination = arguments
    key = args.key

    converter = YConverter(key)
    value = converter.convert(float(amount), source, destination)
    stdout.write(str(value) + "\n")
    stdout.flush()


if __name__ == "__main__":
    main()
