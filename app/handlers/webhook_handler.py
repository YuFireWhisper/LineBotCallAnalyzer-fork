"""
Webhook handler for Line Bot events.
"""
import logging
from flask import request, abort
from linebot.v3.webhooks import MessageEvent, AudioMessageContent
from app.core.config import ApplicationConfig
from app.services.transcription_service import WhisperTranscriptionService
from app.services.summarization_service import GeminiSummarizationService
from app.services.messaging_service import LineMessagingServiceImpl
from app.services.file_storage_service import LocalFileStorageService
from app.services.audio_analysis_workflow import AudioAnalysisWorkflow

logger = logging.getLogger(__name__)

class LineWebhookHandler:
    """Handles Line Bot webhook events."""
    
    def __init__(self, config: ApplicationConfig):
        """
        Initialize the webhook handler with required services.
        
        Args:
            config: Application configuration
        """
        self.config = config
        
        # Initialize services
        self.transcription_service = WhisperTranscriptionService()
        self.summarization_service = GeminiSummarizationService(config.gemini_api_key)
        self.messaging_service = LineMessagingServiceImpl(
            config.line_channel_access_token,
            config.line_channel_secret
        )
        self.file_storage_service = LocalFileStorageService()
        
        # Initialize workflow
        self.audio_workflow = AudioAnalysisWorkflow(
            self.transcription_service,
            self.summarization_service,
            self.messaging_service,
            self.file_storage_service
        )
        
        # Setup webhook handler
        self.webhook_handler = self.messaging_service.get_webhook_handler()
        self._register_event_handlers()
        
        logger.info("Line webhook handler initialized")
    
    def handle_webhook(self):
        """
        Handle incoming webhook requests from Line.
        
        Returns:
            Flask response
        """
        signature = request.headers.get("X-Line-Signature")
        if not signature:
            logger.warning("Missing X-Line-Signature header")
            abort(400)
        
        body = request.get_data(as_text=True)
        
        try:
            self.webhook_handler.handle(body, signature)
            logger.info("Webhook handled successfully")
            return "OK"
            
        except Exception as e:
            logger.error(f"Error handling webhook: {e}")
            abort(400)
    
    def _register_event_handlers(self):
        """Register event handlers with the webhook handler."""
        
        @self.webhook_handler.add(MessageEvent, message=AudioMessageContent)
        def handle_audio_message(event):
            """Handle audio message events."""
            logger.info(f"Received audio message: {event.message.id}")
            
            try:
                self.audio_workflow.process_audio_message(
                    event.message.id,
                    event.reply_token
                )
            except Exception as e:
                logger.error(f"Error processing audio message: {e}")
                # Error handling is done within the workflow
        
        logger.info("Event handlers registered successfully")
