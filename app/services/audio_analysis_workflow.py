"""
Main audio processing workflow orchestrator.
"""
import logging
from app.core.interfaces import (
    AudioTranscriptionService, 
    TextSummarizationService,
    LineMessagingService,
    FileStorageService
)
from app.core.exceptions import ApplicationError

logger = logging.getLogger(__name__)

class AudioAnalysisWorkflow:
    """Orchestrates the audio analysis workflow."""
    
    def __init__(
        self,
        transcription_service: AudioTranscriptionService,
        summarization_service: TextSummarizationService,
        messaging_service: LineMessagingService,
        file_storage_service: FileStorageService
    ):
        """
        Initialize the workflow with required services.
        
        Args:
            transcription_service: Service for audio transcription
            summarization_service: Service for text summarization
            messaging_service: Service for Line messaging
            file_storage_service: Service for file operations
        """
        self.transcription_service = transcription_service
        self.summarization_service = summarization_service
        self.messaging_service = messaging_service
        self.file_storage_service = file_storage_service
        logger.info("Audio analysis workflow initialized")
    
    def process_audio_message(self, message_id: str, reply_token: str) -> None:
        """
        Process an audio message through the complete analysis workflow.
        
        Args:
            message_id: Line message ID for the audio
            reply_token: Line reply token
        """
        temp_audio_path = None
        
        try:
            logger.info(f"Starting audio analysis workflow for message: {message_id}")
            
            # Step 1: Create temporary file for audio
            temp_audio_path = self.file_storage_service.create_temporary_file(
                prefix="audio", 
                suffix=".m4a"
            )
            
            # Step 2: Download audio content
            self.messaging_service.download_audio_content(message_id, temp_audio_path)
            
            # Step 3: Transcribe audio to text
            transcribed_text = self.transcription_service.transcribe_audio_file(temp_audio_path)
            
            # Step 4: Summarize the transcribed text
            summary = self.summarization_service.summarize_text(transcribed_text)
            
            # Step 5: Send summary back to user
            self.messaging_service.send_reply_message(reply_token, summary)
            
            logger.info("Audio analysis workflow completed successfully")
            
        except ApplicationError as e:
            logger.error(f"Application error in workflow: {e}")
            self._send_error_message(reply_token, str(e))
            
        except Exception as e:
            logger.error(f"Unexpected error in workflow: {e}")
            self._send_error_message(reply_token, "抱歉，服務發生問題。請稍後再試。")
            
        finally:
            # Clean up temporary file
            if temp_audio_path:
                self.file_storage_service.delete_file(temp_audio_path)
    
    def _send_error_message(self, reply_token: str, error_message: str) -> None:
        """
        Send an error message to the user.
        
        Args:
            reply_token: Line reply token
            error_message: Error message to send
        """
        try:
            self.messaging_service.send_reply_message(reply_token, error_message)
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
