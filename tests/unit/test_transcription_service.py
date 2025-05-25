"""
Unit tests for audio transcription service.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
from app.services.transcription_service import WhisperTranscriptionService
from app.core.exceptions import TranscriptionError

class TestWhisperTranscriptionService(unittest.TestCase):
    """Test cases for WhisperTranscriptionService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = WhisperTranscriptionService("base")
    
    @patch('app.services.transcription_service.whisper.load_model')
    def test_model_lazy_loading(self, mock_load_model):
        """Test that model is loaded lazily."""
        mock_model = Mock()
        mock_load_model.return_value = mock_model
        
        # Model should not be loaded initially
        self.assertIsNone(self.service._model)
        
        # Access model property should trigger loading
        model = self.service.model
        
        mock_load_model.assert_called_once_with("base")
        self.assertEqual(model, mock_model)
        self.assertEqual(self.service._model, mock_model)
    
    @patch('app.services.transcription_service.whisper.load_model')
    def test_model_loading_error(self, mock_load_model):
        """Test model loading error handling."""
        mock_load_model.side_effect = Exception("Model loading failed")
        
        with self.assertRaises(TranscriptionError) as context:
            _ = self.service.model
        
        self.assertIn("Failed to load Whisper model", str(context.exception))
    
    def test_transcribe_audio_file_success(self):
        """Test successful audio transcription."""
        # Mock the model
        mock_model = Mock()
        mock_model.transcribe.return_value = {"text": "Hello world"}
        self.service._model = mock_model
        
        result = self.service.transcribe_audio_file("test.wav")
        
        self.assertEqual(result, "Hello world")
        mock_model.transcribe.assert_called_once_with("test.wav")
    
    def test_transcribe_audio_file_empty_result(self):
        """Test transcription with empty result."""
        mock_model = Mock()
        mock_model.transcribe.return_value = {"text": "   "}
        self.service._model = mock_model
        
        result = self.service.transcribe_audio_file("test.wav")
        
        self.assertEqual(result, "無法識別語音內容。")
    
    def test_transcribe_audio_file_error(self):
        """Test transcription error handling."""
        mock_model = Mock()
        mock_model.transcribe.side_effect = Exception("Transcription failed")
        self.service._model = mock_model
        
        with self.assertRaises(TranscriptionError) as context:
            self.service.transcribe_audio_file("test.wav")
        
        self.assertIn("音訊轉錄失敗", str(context.exception))

if __name__ == '__main__':
    unittest.main()
