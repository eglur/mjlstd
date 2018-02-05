class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class Not3DError(Exception):
    """Raised when array is not three-dimensional."""
    def __init__(self, message):
        self.message = message
