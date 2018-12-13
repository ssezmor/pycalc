
from .exceptions import PreprocessingError

from .operators import OPERATORS
from .operators import CONSTANTS

def preprocessing(expression):

    if not expression:
        raise PreprocessingError('expression is empty')

    if not isinstance(expression, str):
        raise PreprocessingError('expression is not a string')

    if expression.count('(') != expression.count(')'):
        raise PreprocessingError('brackets are not balanced')

    expression = expression.lower()

    if not is_operators_available(expression):
        raise PreprocessingError('there are no operators in the expression')

    expression = expression.replace('**', '^')

    expression = clean_repeatable_operators(expression)

    return expression


def is_operators_available(expression):
    for statement in OPERATORS:
        if statement in expression:
            return True

    for statement in CONSTANTS:
        if statement in expression:
            return True
    return False


def clean_repeatable_operators(expression):
    repeatable_operators = {'+-': '-', '--': '+', '++': '+', '-+': '-'}

    while True:
        old_exp = expression
        for old, new in repeatable_operators.items():
            expression = expression.replace(old, new)
        if old_exp == expression:
            break

    return expression


def prepare_expression(expression):
    """Docstring."""

    return preprocessing(expression)
