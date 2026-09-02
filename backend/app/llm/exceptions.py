"""
LLM-specific exceptions.

All LLM operations should raise these exceptions for consistent
error handling across the platform.
"""


class LLMException(Exception):
    """Base exception for all LLM-related errors."""

    def __init__(self, message: str, error_code: str = None, details: dict = None):
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
        super().__init__(self.message)


class LLMProviderError(LLMException):
    """Error communicating with LLM provider."""

    def __init__(self, message: str, provider: str = None, **kwargs):
        super().__init__(message, error_code="PROVIDER_ERROR", **kwargs)
        self.provider = provider


class LLMConnectionError(LLMProviderError):
    """Cannot connect to LLM provider."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="CONNECTION_ERROR", **kwargs)


class LLMTimeoutError(LLMProviderError):
    """LLM provider request timed out."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="TIMEOUT_ERROR", **kwargs)


class LLMRateLimitError(LLMProviderError):
    """Rate limited by LLM provider."""

    def __init__(self, message: str, retry_after: int = None, **kwargs):
        super().__init__(message, error_code="RATE_LIMIT_ERROR", **kwargs)
        self.retry_after = retry_after


class LLMAuthenticationError(LLMProviderError):
    """Authentication failed with LLM provider."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="AUTH_ERROR", **kwargs)


class LLMModelNotFoundError(LLMProviderError):
    """Requested model not found."""

    def __init__(self, model: str, **kwargs):
        message = f"Model '{model}' not found"
        super().__init__(message, error_code="MODEL_NOT_FOUND", **kwargs)
        self.model = model


class LLMInvalidRequestError(LLMException):
    """Invalid request to LLM."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="INVALID_REQUEST", **kwargs)


class LLMValidationError(LLMInvalidRequestError):
    """Validation failed for LLM request."""

    def __init__(self, message: str, field: str = None, **kwargs):
        super().__init__(message, error_code="VALIDATION_ERROR", **kwargs)
        self.field = field


class LLMContextLengthError(LLMException):
    """Context length exceeded."""

    def __init__(self, message: str, max_length: int = None, actual_length: int = None, **kwargs):
        super().__init__(message, error_code="CONTEXT_LENGTH_EXCEEDED", **kwargs)
        self.max_length = max_length
        self.actual_length = actual_length


class LLMProcessingError(LLMException):
    """Error processing LLM response."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="PROCESSING_ERROR", **kwargs)


class LLMConfigurationError(LLMException):
    """LLM configuration error."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="CONFIG_ERROR", **kwargs)

