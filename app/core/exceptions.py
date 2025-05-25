"""
Custom exception classes for the application.
"""

class ApplicationError(Exception):
    """Base exception for application errors."""
    pass

class TranscriptionError(ApplicationError):
    """Exception raised when audio transcription fails."""
    pass

class SummarizationError(ApplicationError):
    """Exception raised when text summarization fails."""
    pass

class DownloadError(ApplicationError):
    """Exception raised when downloading content fails."""
    pass

class SendMessageError(ApplicationError):
    """Exception raised when sending message fails."""
    pass

class ConfigurationError(ApplicationError):
    """Exception raised when configuration is invalid."""
    pass
