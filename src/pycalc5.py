"""Pure-python command-line calculator."""

import argparse

from exceptions import CalculatorError

from operators import OPERATORS
from operators import CONSTANTS
from operators import UNARY_OPERATORS
from operators import COMPARISON_SYMBOLS

from preprocessing import Preprocessor


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
        if index <= len(self.expression):
            prev_symbol = self.expression[index - 1]
            if index == 0 or (prev_symbol in OPERATORS and prev_symbol != ')'):
                return True
        return False

    def _is_floor_div(self, index, symbol):
        if index <= len(self.expression):
            return symbol == self.expression[index - 1] == '/'
        return False

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
                raise CalculatorError("Not enough operand's for function {}".format(operator))

            second_operand = self.stack.pop()
            first_operand = self.stack.pop()
            self._calculate_result(operator_params.function, first_operand, second_operand)
        elif operator_params.params_quantity == 3:  # 'round' , 'log', 'hypot', 'atan2'
            if self.stack and self.stack[-1] == ',':
                if len(self.stack) < 3:
                    raise CalculatorError("Not enough operand's for function {}".format(operator))

                self.stack.pop()
                second_operand = self.stack.pop()
                first_operand = self.stack.pop()
                self._calculate_result(operator_params.function, first_operand, second_operand)
            else:
                if len(self.stack) < 1:
                    raise CalculatorError("Not enough operand's for function {}".format(operator))

                operand = self.stack.pop()
                self._calculate_result(operator_params.function, operand)

    def _calculate_result(self, function, first_operand, second_operand=None):

        try:
            if second_operand is None:
                result = function(first_operand)
            else:
                result = function(first_operand, second_operand)
        except ZeroDivisionError as e:
            raise CalculatorError(e)
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
                self.stack.append(convert_to_number('{}1'.format(unary_operator)))
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
        preproc = Preprocessor(self.expression)
        self.expression = preproc.prepare_expression()

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
