"""
File storage service implementation.
"""
import os
import uuid
import logging
from app.core.interfaces import FileStorageService

logger = logging.getLogger(__name__)

class LocalFileStorageService(FileStorageService):
    """Local filesystem implementation of file storage service."""
    
    def create_temporary_file(self, prefix: str = "temp", suffix: str = "") -> str:
        """
        Create a temporary file and return its path.
        
        Args:
            prefix: File name prefix
            suffix: File name suffix/extension
            
        Returns:
            Path to the created temporary file
        """
        unique_id = str(uuid.uuid4())
        filename = f"{prefix}_{unique_id}{suffix}"
        logger.info(f"Creating temporary file: {filename}")
        return filename
    
    def delete_file(self, file_path: str) -> None:
        """
        Delete a file.
        
        Args:
            file_path: Path to the file to delete
        """
        try:
            if self.file_exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted successfully: {file_path}")
            else:
                logger.warning(f"Attempted to delete non-existent file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        return os.path.exists(file_path)
