"""Unittest for pure-python command-line calculator."""

import unittest

import pycalc5


class TestStringMethods(unittest.TestCase):
    """Docstring."""

    def test_convert_to_number__valid_expressions(self):
        """Docstring."""
        test_cases = {'5': 5,
                      '2.3': 2.3,
                      '95655979433245659': 95655979433245659,
                      '7964577455575.9898': 7964577455575.9898,
                      #  '87.88.89': 0,
                      #  'string': 0
                      }

        for k, v in test_cases.items():
            func_result = pycalc5.convert_to_number(k)
            self.assertEqual(func_result, v)

    def test_convert_to_number__invalid_expressions(self):
        pass

    def test_preprocessing(self):
        """Docstring."""
        test_cases = {'    8 + 9   ': '8+9',
                      '++++++++++++': '+',
                      'SIN(9) + 1': 'sin(9)+1'
                      }

        for k, v in test_cases.items():
            calc = pycalc5.Calculator(k)
            calc._preprocessing()
            self.assertEqual(calc.expression, v)

        calc = pycalc5.Calculator('(()')
        with self.assertRaises(pycalc5.CalculatorError):
            calc._preprocessing()

        calc = pycalc5.Calculator('(()')
        with self.assertRaisesRegex(pycalc5.CalculatorError, 'Brackets are not balanced'):
            calc._preprocessing()


if __name__ == '__main__':
    unittest.main()
