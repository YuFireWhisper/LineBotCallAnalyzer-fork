#!/usr/bin/env python3
"""
Entry point for the Line Bot Call Analyzer application.
"""
import logging
from app.core.application import create_application

def configure_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main entry point for the application."""
    configure_logging()
    logger = logging.getLogger(__name__)
    
    try:
        app = create_application()
        logger.info("Starting Line Bot Call Analyzer server on port 5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

if __name__ == "__main__":
    main()
