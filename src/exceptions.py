class ShortenerBaseError(Exception):
    """Base class for all exceptions in the URL shortener application."""
    pass


class NoLongUrlProvidedError(ShortenerBaseError):
    """Raised when no long URL is provided for shortening."""
    pass


class SlugAlreadyExistsError(ShortenerBaseError):
    """Raised when the generated slug already exists in the database."""
    pass
