"""
Unit tests for audio analysis workflow.
"""
import unittest
from unittest.mock import Mock, patch
from app.services.audio_analysis_workflow import AudioAnalysisWorkflow
from app.core.exceptions import TranscriptionError, SummarizationError, DownloadError

class TestAudioAnalysisWorkflow(unittest.TestCase):
    """Test cases for AudioAnalysisWorkflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.transcription_service = Mock()
        self.summarization_service = Mock()
        self.messaging_service = Mock()
        self.file_storage_service = Mock()
        
        self.workflow = AudioAnalysisWorkflow(
            self.transcription_service,
            self.summarization_service,
            self.messaging_service,
            self.file_storage_service
        )
    
    def test_process_audio_message_success(self):
        """Test successful audio message processing."""
        # Setup mocks
        self.file_storage_service.create_temporary_file.return_value = "temp_audio.m4a"
        self.transcription_service.transcribe_audio_file.return_value = "Transcribed text"
        self.summarization_service.summarize_text.return_value = "Summary text"
        
        # Execute
        self.workflow.process_audio_message("message_123", "reply_token_456")
        
        # Verify calls
        self.file_storage_service.create_temporary_file.assert_called_once_with(
            prefix="audio", suffix=".m4a"
        )
        self.messaging_service.download_audio_content.assert_called_once_with(
            "message_123", "temp_audio.m4a"
        )
        self.transcription_service.transcribe_audio_file.assert_called_once_with("temp_audio.m4a")
        self.summarization_service.summarize_text.assert_called_once_with("Transcribed text")
        self.messaging_service.send_reply_message.assert_called_once_with(
            "reply_token_456", "Summary text"
        )
        self.file_storage_service.delete_file.assert_called_once_with("temp_audio.m4a")
    
    def test_process_audio_message_transcription_error(self):
        """Test handling of transcription errors."""
        # Setup mocks
        self.file_storage_service.create_temporary_file.return_value = "temp_audio.m4a"
        self.transcription_service.transcribe_audio_file.side_effect = TranscriptionError("轉錄失敗")
        
        # Execute
        self.workflow.process_audio_message("message_123", "reply_token_456")
        
        # Verify error message was sent
        self.messaging_service.send_reply_message.assert_called_with(
            "reply_token_456", "轉錄失敗"
        )
        
        # Verify cleanup
        self.file_storage_service.delete_file.assert_called_once_with("temp_audio.m4a")
    
    def test_process_audio_message_summarization_error(self):
        """Test handling of summarization errors."""
        # Setup mocks
        self.file_storage_service.create_temporary_file.return_value = "temp_audio.m4a"
        self.transcription_service.transcribe_audio_file.return_value = "Transcribed text"
        self.summarization_service.summarize_text.side_effect = SummarizationError("摘要失敗")
        
        # Execute
        self.workflow.process_audio_message("message_123", "reply_token_456")
        
        # Verify error message was sent
        self.messaging_service.send_reply_message.assert_called_with(
            "reply_token_456", "摘要失敗"
        )
        
        # Verify cleanup
        self.file_storage_service.delete_file.assert_called_once_with("temp_audio.m4a")
    
    def test_process_audio_message_download_error(self):
        """Test handling of download errors."""
        # Setup mocks
        self.file_storage_service.create_temporary_file.return_value = "temp_audio.m4a"
        self.messaging_service.download_audio_content.side_effect = DownloadError("下載失敗")
        
        # Execute
        self.workflow.process_audio_message("message_123", "reply_token_456")
        
        # Verify error message was sent
        self.messaging_service.send_reply_message.assert_called_with(
            "reply_token_456", "下載失敗"
        )
        
        # Verify cleanup
        self.file_storage_service.delete_file.assert_called_once_with("temp_audio.m4a")
    
    def test_process_audio_message_unexpected_error(self):
        """Test handling of unexpected errors."""
        # Setup mocks
        self.file_storage_service.create_temporary_file.return_value = "temp_audio.m4a"
        self.messaging_service.download_audio_content.side_effect = Exception("Unexpected error")
        
        # Execute
        self.workflow.process_audio_message("message_123", "reply_token_456")
        
        # Verify generic error message was sent
        self.messaging_service.send_reply_message.assert_called_with(
            "reply_token_456", "抱歉，服務發生問題。請稍後再試。"
        )
        
        # Verify cleanup
        self.file_storage_service.delete_file.assert_called_once_with("temp_audio.m4a")
    
    def test_cleanup_always_called(self):
        """Test that file cleanup is always called even when error message sending fails."""
        # Setup mocks
        self.file_storage_service.create_temporary_file.return_value = "temp_audio.m4a"
        self.transcription_service.transcribe_audio_file.side_effect = TranscriptionError("轉錄失敗")
        self.messaging_service.send_reply_message.side_effect = Exception("Failed to send message")
        
        # Execute
        self.workflow.process_audio_message("message_123", "reply_token_456")
        
        # Verify cleanup still happened
        self.file_storage_service.delete_file.assert_called_once_with("temp_audio.m4a")

if __name__ == '__main__':
    unittest.main()
