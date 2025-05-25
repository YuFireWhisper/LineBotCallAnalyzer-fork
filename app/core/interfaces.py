"""
Abstract base classes for services to ensure testability and loose coupling.
"""
from abc import ABC, abstractmethod
from typing import Union, BinaryIO

class AudioTranscriptionService(ABC):
    """Abstract base class for audio transcription services."""
    
    @abstractmethod
    def transcribe_audio_file(self, file_path: str) -> str:
        """
        Transcribe audio file to text.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Transcribed text
            
        Raises:
            TranscriptionError: If transcription fails
        """
        pass

class TextSummarizationService(ABC):
    """Abstract base class for text summarization services."""
    
    @abstractmethod
    def summarize_text(self, text: str) -> str:
        """
        Summarize the given text.
        
        Args:
            text: Text to summarize
            
        Returns:
            Summarized text
            
        Raises:
            SummarizationError: If summarization fails
        """
        pass

class LineMessagingService(ABC):
    """Abstract base class for Line messaging operations."""
    
    @abstractmethod
    def download_audio_content(self, message_id: str, output_path: str) -> None:
        """
        Download audio content from Line servers.
        
        Args:
            message_id: Line message ID
            output_path: Path to save the audio file
            
        Raises:
            DownloadError: If download fails
        """
        pass
    
    @abstractmethod
    def send_reply_message(self, reply_token: str, message: str) -> None:
        """
        Send a reply message to Line.
        
        Args:
            reply_token: Line reply token
            message: Message content to send
            
        Raises:
            SendMessageError: If sending fails
        """
        pass

class FileStorageService(ABC):
    """Abstract base class for file storage operations."""
    
    @abstractmethod
    def create_temporary_file(self, prefix: str = "temp", suffix: str = "") -> str:
        """
        Create a temporary file and return its path.
        
        Args:
            prefix: File name prefix
            suffix: File name suffix/extension
            
        Returns:
            Path to the created temporary file
        """
        pass
    
    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        """
        Delete a file.
        
        Args:
            file_path: Path to the file to delete
        """
        pass
    
    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        pass
