"""Unittest for pure-python command-line calculator."""

import unittest

import sys

sys.path.append('src')

import math

from calculator import Calculator
from exceptions import CalculatorError
from exceptions import BaseCalculatorException

class TestStringMethods(unittest.TestCase):
    """Docstring."""

    def test_process_digit__valid_expressions(self):
        """Docstring."""

        expression = '5'

        calc = Calculator(expression)
        calc._process_digit(0, '5')

        self.assertEqual(calc.number, '5')

        expression = ' .'

        calc = Calculator(expression)
        calc._process_digit(1, '.')

        self.assertEqual(calc.number, '.')

        expression = '1 2 3 4'

        calc = Calculator(expression)
        calc.number = '1'

        with self.assertRaises(BaseCalculatorException):
            calc._process_digit(2, '2')

    def test_process_digit__invalid_expressions(self):
        pass

    def test_process_number_and_constant__valid_expressions(self):

        expression = '54.55'

        calc = Calculator(expression)
        calc.unary_operator = ''
        calc.number = '54.55'
        calc._process_number_and_constant()

        self.assertEqual(calc.rpn[-1], 54.55)

        expression = '-5'

        calc = Calculator(expression)
        calc.unary_operator = '-@'
        calc.number = '5'
        calc._process_number_and_constant()

        self.assertEqual(calc.rpn[-1], -5)

        expression = 'pi'

        calc = Calculator(expression)
        calc.unary_operator = ''
        calc.number = ''
        calc.operator = 'pi'
        calc._process_number_and_constant()

        self.assertEqual(calc.rpn[-1], math.pi)

        expression = '-e'

        calc = Calculator(expression)
        calc.unary_operator = '-@'
        calc.number = ''
        calc.operator = 'e'
        calc._process_number_and_constant()

        self.assertEqual(calc.rpn[-1], -math.e)

"""
    def test_convert_to_number__valid_expressions(self):

        test_cases = {'5': 5,
                      '2.3': 2.3,
                      '95655979433245659': 95655979433245659,
                      '7964577455575.9898': 7964577455575.9898
                      }

        for expression, result in test_cases.items():
            func_result = calculator.convert_to_number(expression)
            self.assertEqual(func_result, result)

    def test_convert_to_number__invalid_expressions(self):
        pass
"""




"""
    def test_preprocessing(self):
        Docstring.
        test_cases = {'+++++--+++--+++': '+',
                      'SIN(9) + 1': 'sin(9) + 1'
                      }

        for expression, result in test_cases.items():
            calc = pycalc5.Calculator(expression)
            calc._preprocessing()
            self.assertEqual(calc.expression, v)

        calc = pycalc5.Calculator('(()')
        with self.assertRaises(pycalc5.CalculatorError):
            calc._preprocessing()

        calc = pycalc5.Calculator('(()')
        with self.assertRaisesRegex(pycalc5.CalculatorError, 'Brackets are not balanced'):
            calc._preprocessing()
"""

if __name__ == '__main__':
    unittest.main()
