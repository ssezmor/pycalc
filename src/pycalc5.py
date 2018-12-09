"""Pure-python command-line calculator."""

import argparse
import sys
import operator
import builtins
import math

from collections import namedtuple

from exceptions import CalculatorError


UNARY_OPERATORS = {'-': '-@', '+': '+@'}

COMPARISON_SYMBOLS = ('!', '<', '>', '=')

OPERATOR = namedtuple('OPERATOR', 'priority function params_quantity')

OPERATORS = {
    '+': OPERATOR(1, operator.add, 2), '-': OPERATOR(1, operator.sub, 2),
    '*': OPERATOR(2, operator.mul, 2), '/': OPERATOR(2, operator.truediv, 2),
    '//': OPERATOR(2, operator.floordiv, 2), '%': OPERATOR(2, operator.mod, 2),
    '^': OPERATOR(3, operator.pow, 2),
    'sin': OPERATOR(4, math.sin, 1), 'cos': OPERATOR(4, math.cos, 1),
    'asin': OPERATOR(4, math.asin, 1), 'acos': OPERATOR(4, math.acos, 1),
    'sinh': OPERATOR(4, math.sinh, 1), 'cosh': OPERATOR(4, math.cosh, 1),
    'asinh': OPERATOR(4, math.asinh, 1), 'acosh': OPERATOR(4, math.acosh, 1),
    'tanh': OPERATOR(4, math.tanh, 1), 'atanh': OPERATOR(4, math.atanh, 1),
    'tan': OPERATOR(4, math.tan, 1), 'atan': OPERATOR(4, math.atan, 1),
    'hypot': OPERATOR(4, math.hypot, 3), 'atan2': OPERATOR(4, math.atan2, 3),
    'exp': OPERATOR(4, math.exp, 1), 'expm1': OPERATOR(4, math.expm1, 1),
    'log10': OPERATOR(4, math.log10, 1), 'log2': OPERATOR(4, math.log2, 1),
    'log1p': OPERATOR(4, math.log1p, 1), 'sqrt': OPERATOR(4, math.sqrt, 1),
    'abs': OPERATOR(4, builtins.abs, 1),
    'round': OPERATOR(4, builtins.round, 3), 'log': OPERATOR(4, math.log, 3),
    '<': OPERATOR(0, operator.lt, 2), '<=': OPERATOR(0, operator.le, 2),
    '==': OPERATOR(0, operator.eq, 2), '!=': OPERATOR(0, operator.ne, 2),
    '>=': OPERATOR(0, operator.ge, 2), '>': OPERATOR(0, operator.gt, 2),
    ',': OPERATOR(0, None, 0),
    '(': OPERATOR(0, None, 0), ')': OPERATOR(8, None, 0),
    '-@': OPERATOR(2, None, 0), '+@': OPERATOR(2, None, 0)
}

CONSTANTS = {'e': math.e, 'pi': math.pi, 'tau': math.tau}


class Calculator:
    """Docstring."""

    def __init__(self, expression):
        """Docstring."""
        self.expression = expression
        self.number = ''
        self.operator = ''
        self.unary_operator = ''
        self.rpn = []
        self.stack = []

    def _preprocessing(self):

        if not self.expression:
            raise CalculatorError('Expression is empty')

        if not isinstance(self.expression, str):
            raise CalculatorError('Expression is not a string')

        if self.expression.count('(') != self.expression.count(')'):
            raise CalculatorError('Brackets are not balanced')

        self.expression = self.expression.lower()

        if not self._is_operators_available():
            raise CalculatorError('There are no operators in the expression')

        self.expression = self.expression.replace(' ', '')
        self._clean_repeatable_operators()

    def _is_operators_available(self):
        for statement in OPERATORS:
            if statement in self.expression:
                return True
        return False

    def _clean_repeatable_operators(self):
        repeatable_operators = {'+-': '-', '--': '+', '++': '+', '-+': '-'}

        while True:
            old_exp = self.expression
            for old, new in repeatable_operators.items():
                self.expression = self.expression.replace(old, new)
            if old_exp == self.expression:
                break

    def _process_number_and_constant(self):
        if self.unary_operator:
            self.unary_operator = self._replace_unary_operator(self.unary_operator)

        if self.number:
            self.rpn.append(convert_to_number('{}{}'.format(self.unary_operator,
                                                            self.number)))
            self.number = ''

        if self.operator in CONSTANTS:
            if self.unary_operator == '-':
                self.rpn.append(0 - CONSTANTS[self.operator])
            else:
                self.rpn.append(CONSTANTS[self.operator])
            self.operator = ''

        self.unary_operator = ''

    def _process_operator(self):
        if self.unary_operator:
            self.stack.append(self.unary_operator)

        if self.operator:
            if self.operator not in OPERATORS:
                raise CalculatorError('Operator not supported')
            self.stack.append(self.operator)

        self.unary_operator = ''
        self.operator = ''

    def _process_stack(self, symbol):
        while self.stack:
            if symbol == self.stack[-1] == '^':
                break

            if OPERATORS[symbol].priority <= OPERATORS[self.stack[-1]].priority:
                self.rpn.append(self.stack.pop())
            else:
                break

        self.stack.append(symbol)

    def _process_comparison(self, symbol):
        self._process_number_and_constant()

        if self.stack and self.stack[-1] in COMPARISON_SYMBOLS:
            self.stack[-1] += symbol
        else:
            while self.stack:
                self.rpn.append(self.stack.pop())

            self.stack.append(symbol)

    def _process_brackets_and_comma(self, symbol):
        if symbol == ',':
            self._process_number_and_constant()
            while self.stack:
                if OPERATORS[symbol].priority < OPERATORS[self.stack[-1]].priority:
                    self.rpn.append(self.stack.pop())
                else:
                    break
            self.stack.append(symbol)
        elif symbol == '(':
            self._process_operator()
            self.stack.append(symbol)
        elif symbol == ')':
            self._process_number_and_constant()
            while self.stack:
                element = self.stack.pop()
                if element == '(':
                    break
                self.rpn.append(element)

    def _is_unary_operator(self, index, symbol):
        if symbol not in UNARY_OPERATORS:
            return False
        if index == 0 or (self.expression[index - 1] in OPERATORS and self.expression[index - 1] != ')'):
            return True
        return False

    def _is_floor_div(self, index, symbol):
        if index <= 0:
            return False
        return symbol == self.expression[index - 1] == '/'

    def _process_expression(self):
        for index, symbol in enumerate(self.expression):
            if self.operator in CONSTANTS:
                self._process_number_and_constant()

            if symbol in COMPARISON_SYMBOLS:
                self._process_comparison(symbol)
                continue

            if symbol.isdigit() and self.operator:
                self.operator += symbol
            elif symbol.isdigit() or symbol == '.':
                self.number += symbol
            elif symbol in ('(', ',', ')'):
                self._process_brackets_and_comma(symbol)
            elif symbol in OPERATORS:
                if self._is_floor_div(index, symbol):
                    self.stack[-1] += symbol
                    continue

                if self._is_unary_operator(index, symbol):
                    self.unary_operator = UNARY_OPERATORS[symbol]
                    continue

                self._process_number_and_constant()
                self._process_stack(symbol)
            elif symbol.isalpha() or symbol == '=':
                self.operator += symbol

        self._process_number_and_constant()
        self.rpn.extend(reversed(self.stack))

        if not self.rpn:
            raise CalculatorError('Not enough data to calculate')

        del self.stack[:]

    def _calculate_operator(self, operator):

        operator_params = OPERATORS[operator]

        if operator_params.params_quantity == 1:
            if len(self.stack) < 1:
                raise CalculatorError("Not enough operand's for function {}".format(operator))

            operand = self.stack.pop()
            self._calculate_result(operator_params.function, operand)
        elif operator_params.params_quantity == 2:
            if len(self.stack) < 2:
                raise CalculatorError("Not enough operand's for function {0}".format(operator))

            second_operand = self.stack.pop()
            first_operand = self.stack.pop()
            self._calculate_result(operator_params.function, first_operand, second_operand)
        elif operator_params.params_quantity == 3:  # 'round' , 'log', 'hypot', 'atan2'
            if self.stack and self.stack[-1] == ',':
                if len(self.stack) < 3:
                    raise CalculatorError("Not enough operand's for function {0}".format(operator))

                self.stack.pop()
                second_operand = self.stack.pop()
                first_operand = self.stack.pop()
                self._calculate_result(operator_params.function, first_operand, second_operand)
            else:
                if len(self.stack) < 1:
                    raise CalculatorError("Not enough operand's for function {0}".format(operator))

                operand = self.stack.pop()
                self._calculate_result(operator_params.function, operand)

    def _calculate_result(self, function, first_operand, second_operand=None):

        try:
            if second_operand is None:
                result = function(first_operand)
            else:
                result = function(first_operand, second_operand)
        except ZeroDivisionError as e:
            raise CalculatorError(e)  # Ant: Why did you incapsulate original exception?
        except ArithmeticError as e:
            raise CalculatorError(e)
        except Exception as e:
            raise CalculatorError(e)
        else:
            self.stack.append(result)

    def _calculate_rpn(self):

        for item in self.rpn:
            if item == ',':
                self.stack.append(item)
            elif item in UNARY_OPERATORS.values():
                unary_operator = self._replace_unary_operator(item)
                self.stack.append(convert_to_number('{0}1'.format(unary_operator)))
                self._calculate_operator('*')
            elif item in OPERATORS:
                self._calculate_operator(item)
            else:
                self.stack.append(item)

    def _replace_unary_operator(self, unary_operator):

        for key, value in UNARY_OPERATORS.items():
            if value == unary_operator:
                return key

    def calculate(self):
        """Docstring."""
        self._preprocessing()
        self._process_expression()
        self._calculate_rpn()
        return self.stack[-1]


def convert_to_number(number):
    """Docstring."""
    if not isinstance(number, str):
        return 0
    return float(number) if '.' in number else int(number)


def main():
    """Docstring."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    args = parser.parse_args()

    pycalc = Calculator(args.EXPRESSION)
    print(pycalc.calculate())


if __name__ == '__main__':
    main()
