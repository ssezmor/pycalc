import sys

class BaseCalculatorException(Exception):
    """Docstring."""

    def __init__(self, message=None):
        """Docstring."""

        if message is None:
            message = 'An error occured while working pycalc'
        self.message = 'ERROR: {}'.format(message)

        print(self.message)

        sys.exit(1)

class CalculatorError(BaseCalculatorException):
    """Docstring."""
    def __init__(self, message=None):
        """Docstring."""
        super().__init__()

class PreprocessingError(BaseCalculatorException):
    """Docstring."""
    def __init__(self, message=None):
        """Docstring."""
        super().__init__()



