
from exceptions import PreprocessingError

from operators import OPERATORS

class Preprocessor:
   """Docstring."""

    def __init__(self, expression):
        """Docstring."""
        self.expression = expression

    def _preprocessing(self):

        if not self.expression:
            raise PreprocessingError('Expression is empty')

        if not isinstance(self.expression, str):
            raise PreprocessingError('Expression is not a string')

        if self.expression.count('(') != self.expression.count(')'):
            raise PreprocessingError('Brackets are not balanced')

        self.expression = self.expression.lower()

        if not self._is_operators_available():
            raise PreprocessingError('There are no operators in the expression')

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

    def prepare_expression():
        """Docstring."""
        self._preprocessing()
        return self.expression
