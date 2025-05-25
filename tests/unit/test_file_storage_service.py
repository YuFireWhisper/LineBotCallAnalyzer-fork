"""
Unit tests for file storage service.
"""
import unittest
import tempfile
import os
from unittest.mock import patch, Mock
from app.services.file_storage_service import LocalFileStorageService

class TestLocalFileStorageService(unittest.TestCase):
    """Test cases for LocalFileStorageService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = LocalFileStorageService()
    
    @patch('app.services.file_storage_service.uuid.uuid4')
    def test_create_temporary_file(self, mock_uuid):
        """Test temporary file creation."""
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid-123")
        
        result = self.service.create_temporary_file("audio", ".m4a")
        
        expected = "audio_test-uuid-123.m4a"
        self.assertEqual(result, expected)
    
    def test_create_temporary_file_default_params(self):
        """Test temporary file creation with default parameters."""
        result = self.service.create_temporary_file()
        
        self.assertTrue(result.startswith("temp_"))
        self.assertTrue(len(result) > 10)  # Should have UUID appended
    
    def test_file_exists_true(self):
        """Test file_exists returns True for existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            result = self.service.file_exists(tmp_path)
            self.assertTrue(result)
        finally:
            os.unlink(tmp_path)
    
    def test_file_exists_false(self):
        """Test file_exists returns False for non-existing file."""
        result = self.service.file_exists("/non/existent/file.txt")
        self.assertFalse(result)
    
    def test_delete_file_success(self):
        """Test successful file deletion."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        # Verify file exists
        self.assertTrue(os.path.exists(tmp_path))
        
        # Delete file
        self.service.delete_file(tmp_path)
        
        # Verify file is deleted
        self.assertFalse(os.path.exists(tmp_path))
    
    def test_delete_file_non_existent(self):
        """Test deleting non-existent file doesn't raise error."""
        # Should not raise an exception
        self.service.delete_file("/non/existent/file.txt")
    
    @patch('app.services.file_storage_service.os.remove')
    @patch('app.services.file_storage_service.os.path.exists')
    def test_delete_file_os_error(self, mock_exists, mock_remove):
        """Test delete_file handles OS errors gracefully."""
        mock_exists.return_value = True
        mock_remove.side_effect = OSError("Permission denied")
        
        # Should not raise an exception
        self.service.delete_file("test_file.txt")
        
        mock_remove.assert_called_once_with("test_file.txt")

if __name__ == '__main__':
    unittest.main()
