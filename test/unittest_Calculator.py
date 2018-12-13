"""Unittest for pure-python command-line calculator."""

import unittest

import sys
sys.path.append('..')  # Ant: You don't need to add path like this, just add __init__.py in src

import math

from src import calculator
from src import exceptions

from collections import namedtuple


class TestStringMethods(unittest.TestCase):
    """Docstring."""

    def test_process_digit__valid_expressions(self):
        """Docstring."""
        valid_expression = namedtuple('valid_expression', 'expression index symbol result')
        valid_expressions = [valid_expression('5', 0, '5', '5'),
                             valid_expression(' .', 1, '.', '.'),
                             valid_expression('1 ', 0, '1', '1')
        ]

        for expression in valid_expressions:
            calc = calculator.Calculator(expression.expression)
            calc._process_digit(expression.index, expression.symbol)

            self.assertEqual(calc.number, expression.result)

    def test_process_digit__invalid_expressions(self):
        """Docstring."""

        expression = '1 2 3 4'

        calc = calculator.Calculator(expression)
        calc.number = '1'

        with self.assertRaises(exceptions.BaseCalculatorException):
            calc._process_digit(2, '2')

    def test_process_number_and_constant__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'unary_operator number operator result')
        valid_expressions = [valid_expression('', '54.55', '', 54.55),
                             valid_expression('-@', '5', '', -5),
                             valid_expression('', '', 'pi', math.pi),
                             valid_expression('-@', '', 'e', -math.e)
        ]

        for expression in valid_expressions:
            calc = calculator.Calculator('')
            calc.unary_operator = expression.unary_operator
            calc.number = expression.number
            calc.operator = expression.operator
            calc._process_number_and_constant()

            self.assertEqual(calc.rpn[-1], expression.result)

    def test_process_number_and_constant__invalid_expressions(self):
        """Docstring."""
        pass

    def test_process_operator__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'unary_operator operator result')
        valid_expressions = [valid_expression('', 'sin', ['sin']),
                             valid_expression('-@', 'log', ['-@', 'log'])
        ]

        for expression in valid_expressions:
            calc = calculator.Calculator('')
            calc.unary_operator = expression.unary_operator
            calc.operator = expression.operator
            calc._process_operator()

            self.assertEqual(calc.stack, expression.result)

    def test_process_operator__invalid_expressions(self):
        """Docstring."""

        invalid_expression = namedtuple('valid_expression', 'unary_operator operator')
        invalid_expressions = [invalid_expression('', 'log100'),
                               invalid_expression('-@', 'sin4')
        ]

        for expression in invalid_expressions:
            calc = calculator.Calculator('')
            calc.unary_operator = expression.unary_operator
            calc.operator = expression.operator

            with self.assertRaises(exceptions.BaseCalculatorException):
                calc._process_operator()

    def test_process_stack__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'stack symbol result_stack result_rpn')
        valid_expressions = [valid_expression(['^'], '^', ['^', '^'], []),
                             valid_expression(['*'], '+', ['+'], ['*']),
                             valid_expression(['-'], '/', ['-', '/'], []),
                             valid_expression(['sin', 'tan'], '/', ['/'], ['tan', 'sin'])
        ]

        for expression in valid_expressions:
            calc = calculator.Calculator('')
            calc.stack = expression.stack
            calc._process_stack(expression.symbol)

            self.assertEqual(calc.stack, expression.result_stack)
            self.assertEqual(calc.rpn, expression.result_rpn)

    def test_process_stack__invalid_expressions(self):
        """Docstring."""
        pass

    def test_process_comparison__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression stack index symbol result_stack result_rpn')
        valid_expressions = [valid_expression('5 >= 4', ['>'], 3, '=', ['>='], []),
                             valid_expression('5+1*2 > 4', ['+', '*'], 7, '>', ['>'], ['*', '+'])
        ]

        for expression in valid_expressions:
            calc = calculator.Calculator(expression.expression)
            calc.stack = expression.stack
            calc._process_comparison(expression.index, expression.symbol)

            self.assertEqual(calc.stack, expression.result_stack)
            self.assertEqual(calc.rpn, expression.result_rpn)

    def test_process_comparison__invalid_expressions(self):
        """Docstring."""

        invalid_expression = namedtuple('invalid_expression', 'expression stack index symbol')
        invalid_expressions = [invalid_expression('5 > = 4', ['>'], 4, '='),
                               invalid_expression('5+2 = = 4', ['='], 6, '=')
        ]

        for expression in invalid_expressions:
            calc = calculator.Calculator(expression.expression)
            calc.stack = expression.stack

            with self.assertRaises(exceptions.BaseCalculatorException):
                calc._process_comparison(expression.index, expression.symbol)

    def test_process_brackets_and_comma__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression stack symbol number result_stack result_rpn')
        valid_expressions = [
        valid_expression('round(1.22, 4)', ['round', '('], ',', '', ['round', '(', ','], []),
        valid_expression('round(1.22+2, 4)', ['round', '(', '+'], ',', '', ['round', '(', ','], ['+']),
        valid_expression('2 + (4)', ['+'], '(', '', ['+', '('], []),
        valid_expression('2 + 2(4)', ['+'], '(', '2', ['+', '*', '('], [2]),
        valid_expression('(4 + 3 * 2)', ['(', '+', '*'], ')', '', [], ['*', '+']),
        valid_expression('1 + (3 * 2)', ['+', '(', '*'], ')', '', ['+'], ['*'])
        ]

        for expression in valid_expressions:
            calc = calculator.Calculator(expression.expression)
            calc.stack = expression.stack
            calc.number = expression.number
            calc._process_brackets_and_comma(expression.symbol)

            self.assertEqual(calc.stack, expression.result_stack)
            self.assertEqual(calc.rpn, expression.result_rpn)

    def test_process_brackets_and_comma__invalid_expressions(self):
        """Docstring."""
        pass

    def test_is_unary_operator__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression index symbol result')
        valid_expressions = [valid_expression('-4', 0, '-', True),
                             valid_expression('!4', 0, '!', False),
                             valid_expression('-4', 4, '-', False),
                             valid_expression('1*-4', 2, '-', True),
                             valid_expression('(1*2)-4', 5, '-', False)
        ]

        for expression in valid_expressions:
            calc = calculator.Calculator(expression.expression)
            func_result = calc._is_unary_operator(expression.index, expression.symbol)

            if expression.result:
                self.assertTrue(func_result)
            else:
                self.assertFalse(func_result)

    def test_is_unary_operator__invalid_expressions(self):
        """Docstring."""
        pass

    def test_is_floordiv__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression index symbol result')
        valid_expressions = [valid_expression('5/5', 4, '', False),
                             valid_expression('4//3', 2, '/', True),
                             valid_expression('4/3', 1, '/', False)
        ]

        for expression in valid_expressions:
            calc = calculator.Calculator(expression.expression)
            func_result = calc._is_floordiv(expression.index, expression.symbol)

            if expression.result:
                self.assertTrue(func_result)
            else:
                self.assertFalse(func_result)


if __name__ == '__main__':
    unittest.main()
