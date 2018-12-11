"""Pure-python command-line calculator."""

import argparse
import sys

sys.path.append('src') 

from calculator import Calculator

def main():
    """Docstring."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    args = parser.parse_args()

    pycalc = Calculator(args.EXPRESSION)
    print(pycalc.calculate())


if __name__ == '__main__':
    main()
