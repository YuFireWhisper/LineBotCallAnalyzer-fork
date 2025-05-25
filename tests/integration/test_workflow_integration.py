"""
Integration tests for the complete audio analysis workflow.
"""
import unittest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from app.core.config import ApplicationConfig
from app.services.audio_analysis_workflow import AudioAnalysisWorkflow
from app.services.transcription_service import WhisperTranscriptionService
from app.services.summarization_service import GeminiSummarizationService
from app.services.messaging_service import LineMessagingServiceImpl
from app.services.file_storage_service import LocalFileStorageService

class TestAudioAnalysisIntegration(unittest.TestCase):
    """Integration test cases for audio analysis workflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_config = ApplicationConfig(
            line_channel_access_token="test_token",
            line_channel_secret="test_secret",
            gemini_api_key="test_gemini_key"
        )
    
    @patch('app.services.transcription_service.whisper.load_model')
    @patch('app.services.summarization_service.genai.configure')
    @patch('app.services.summarization_service.genai.GenerativeModel')
    def test_workflow_integration_success(self, mock_genai_model, mock_genai_configure, mock_whisper_load):
        """Test complete workflow integration with mocked external services."""
        # Mock Whisper model
        mock_whisper = Mock()
        mock_whisper.transcribe.return_value = {"text": "這是一段測試語音內容，包含重要資訊。"}
        mock_whisper_load.return_value = mock_whisper
        
        # Mock Gemini model
        mock_gemini = Mock()
        mock_response = Mock()
        mock_candidate = Mock()
        mock_content = Mock()
        mock_part = Mock()
        mock_part.text = "測試語音摘要：包含重要資訊。"
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        mock_gemini.generate_content.return_value = mock_response
        mock_genai_model.return_value = mock_gemini
        
        # Initialize services
        transcription_service = WhisperTranscriptionService()
        summarization_service = GeminiSummarizationService(self.test_config.gemini_api_key)
        messaging_service = Mock(spec=LineMessagingServiceImpl)
        file_storage_service = LocalFileStorageService()
        
        # Create workflow
        workflow = AudioAnalysisWorkflow(
            transcription_service,
            summarization_service,
            messaging_service,
            file_storage_service
        )
        
        # Create a temporary audio file for testing
        with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as tmp_file:
            tmp_file.write(b"fake audio content")
            tmp_path = tmp_file.name
        
        try:
            # Mock file storage to return our test file
            file_storage_service.create_temporary_file = Mock(return_value=tmp_path)
            
            # Execute workflow
            workflow.process_audio_message("test_message_id", "test_reply_token")
            
            # Verify messaging service was called with summary
            messaging_service.send_reply_message.assert_called_once_with(
                "test_reply_token", "測試語音摘要：包含重要資訊。"
            )
            
            # Verify transcription was called
            mock_whisper.transcribe.assert_called_once_with(tmp_path)
            
            # Verify summarization was called
            mock_gemini.generate_content.assert_called_once()
            
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

if __name__ == '__main__':
    unittest.main()
