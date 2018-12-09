import sys

class BaseCalculatroExceptio(Exception):
    pass

class CalculatorError(BaseCalculatroExceptio):
    """Docstring."""

    def __init__(self, message=None):
        """Docstring."""

        if message is None:
            message = 'An error occured while working pycalc'
        self.message = 'ERROR: {}'.format(message)

        print(self.message)

        sys.exit(1)
