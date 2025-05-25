"""
Core application module containing the main Flask application factory.
"""
import logging
from flask import Flask
from app.core.config import ApplicationConfig
from app.handlers.webhook_handler import LineWebhookHandler

logger = logging.getLogger(__name__)

def create_application() -> Flask:
    """
    Create and configure the Flask application.
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    try:
        config = ApplicationConfig.from_environment()
        webhook_handler = LineWebhookHandler(config)
        
        # Register webhook endpoint
        app.add_url_rule(
            '/callback',
            'callback',
            webhook_handler.handle_webhook,
            methods=['POST']
        )
        
        logger.info("Application created successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to create application: {e}")
        raise
