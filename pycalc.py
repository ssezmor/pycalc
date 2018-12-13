"""Pure-python command-line calculator."""

import argparse

from src import calculator

def main():
    """Docstring."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    args = parser.parse_args()

    pycalc = calculator.Calculator(args.EXPRESSION)
    print(pycalc.calculate())


if __name__ == '__main__':
    main()
