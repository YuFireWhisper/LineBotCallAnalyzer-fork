"""
Configuration management for the application.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class ApplicationConfig:
    """Configuration class for the Line Bot application."""
    
    line_channel_access_token: str
    line_channel_secret: str
    gemini_api_key: str
    
    @classmethod
    def from_environment(cls) -> 'ApplicationConfig':
        """
        Create configuration from environment variables.
        
        Returns:
            ApplicationConfig instance
            
        Raises:
            ValueError: If required environment variables are missing
        """
        line_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        line_secret = os.getenv("LINE_CHANNEL_SECRET")
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        missing_vars = []
        if not line_token:
            missing_vars.append("LINE_CHANNEL_ACCESS_TOKEN")
        if not line_secret:
            missing_vars.append("LINE_CHANNEL_SECRET")
        if not gemini_key:
            missing_vars.append("GEMINI_API_KEY")
            
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
        return cls(
            line_channel_access_token=line_token,
            line_channel_secret=line_secret,
            gemini_api_key=gemini_key
        )
