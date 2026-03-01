"""Custom exceptions for the governance analysis engine."""


__all__ = ["ExternalAPIError"]


class ExternalAPIError(Exception):
    """Raised when an external API request fails.

    Attributes:
        message: Human-readable error description.
        original_error: The original exception that caused this error, if any.
    """

    def __init__(self, message: str, original_error: Exception | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error description.
            original_error: The original exception that caused this error.
        """
        super().__init__(message)
        self.original_error: Exception | None = original_error

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.original_error:
            return f"{super().__str__()} (caused by: {type(self.original_error).__name__})"
        return super().__str__()
