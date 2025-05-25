"""
Line messaging service implementation.
"""
import logging
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, MessagingApiBlob,
    ReplyMessageRequest, TextMessage
)
from app.core.interfaces import LineMessagingService
from app.core.exceptions import DownloadError, SendMessageError

logger = logging.getLogger(__name__)

class LineMessagingServiceImpl(LineMessagingService):
    """Line Bot SDK implementation of messaging service."""
    
    def __init__(self, access_token: str, channel_secret: str):
        """
        Initialize the Line messaging service.
        
        Args:
            access_token: Line channel access token
            channel_secret: Line channel secret
        """
        self.configuration = Configuration(access_token=access_token)
        self.webhook_handler = WebhookHandler(channel_secret)
        logger.info("Line messaging service initialized")
    
    def download_audio_content(self, message_id: str, output_path: str) -> None:
        """
        Download audio content from Line servers.
        
        Args:
            message_id: Line message ID
            output_path: Path to save the audio file
            
        Raises:
            DownloadError: If download fails
        """
        try:
            logger.info(f"Downloading audio content for message ID: {message_id}")
            
            with ApiClient(self.configuration) as api_client:
                messaging_api = MessagingApiBlob(api_client)
                
                with messaging_api.get_message_content(message_id) as audio_content:
                    with open(output_path, "wb") as f:
                        for chunk in audio_content.iter_content():
                            f.write(chunk)
            
            logger.info(f"Audio content downloaded successfully to: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to download audio content: {e}")
            raise DownloadError(f"音訊下載失敗：{str(e)}")
    
    def send_reply_message(self, reply_token: str, message: str) -> None:
        """
        Send a reply message to Line.
        
        Args:
            reply_token: Line reply token
            message: Message content to send
            
        Raises:
            SendMessageError: If sending fails
        """
        try:
            logger.info(f"Sending reply message with token: {reply_token}")
            
            with ApiClient(self.configuration) as api_client:
                messaging_api = MessagingApi(api_client)
                messaging_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=message)]
                    )
                )
            
            logger.info("Reply message sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send reply message: {e}")
            raise SendMessageError(f"訊息發送失敗：{str(e)}")
    
    def get_webhook_handler(self) -> WebhookHandler:
        """
        Get the webhook handler instance.
        
        Returns:
            WebhookHandler instance
        """
        return self.webhook_handler
