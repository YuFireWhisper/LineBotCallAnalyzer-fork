"""
Whisper-based audio transcription service implementation.
"""
import logging
import whisper
from app.core.interfaces import AudioTranscriptionService
from app.core.exceptions import TranscriptionError

logger = logging.getLogger(__name__)

class WhisperTranscriptionService(AudioTranscriptionService):
    """Whisper implementation of audio transcription service."""
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize the Whisper transcription service.
        
        Args:
            model_name: Whisper model name (base, small, medium, large)
        """
        self.model_name = model_name
        self._model = None
        logger.info(f"Initializing Whisper service with model: {model_name}")
    
    @property
    def model(self):
        """Lazy load the Whisper model."""
        if self._model is None:
            try:
                logger.info(f"Loading Whisper model: {self.model_name}")
                self._model = whisper.load_model(self.model_name)
                logger.info("Whisper model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}")
                raise TranscriptionError(f"Failed to load Whisper model: {e}")
        return self._model
    
    def transcribe_audio_file(self, file_path: str) -> str:
        """
        Transcribe audio file using Whisper.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Transcribed text
            
        Raises:
            TranscriptionError: If transcription fails
        """
        try:
            logger.info(f"Starting transcription for file: {file_path}")
            result = self.model.transcribe(file_path)
            text = result["text"].strip()
            
            if not text:
                logger.warning("Transcription resulted in empty text")
                return "無法識別語音內容。"
            
            logger.info(f"Transcription completed successfully. Text length: {len(text)}")
            return text
            
        except Exception as e:
            logger.error(f"Transcription failed for file {file_path}: {e}")
            raise TranscriptionError(f"音訊轉錄失敗：{str(e)}")
