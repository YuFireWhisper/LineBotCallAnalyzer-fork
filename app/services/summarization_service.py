"""
Gemini-based text summarization service implementation.
"""
import logging
import google.generativeai as genai
from app.core.interfaces import TextSummarizationService
from app.core.exceptions import SummarizationError

logger = logging.getLogger(__name__)

class GeminiSummarizationService(TextSummarizationService):
    """Gemini implementation of text summarization service."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the Gemini summarization service.
        
        Args:
            api_key: Gemini API key
            model_name: Gemini model name
        """
        self.api_key = api_key
        self.model_name = model_name
        self._model = None
        
        try:
            genai.configure(api_key=api_key)
            logger.info(f"Gemini API configured with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
            raise SummarizationError(f"Failed to configure Gemini API: {e}")
    
    @property
    def model(self):
        """Lazy load the Gemini model."""
        if self._model is None:
            try:
                self._model = genai.GenerativeModel(self.model_name)
                logger.info("Gemini model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini model: {e}")
                raise SummarizationError(f"Failed to initialize Gemini model: {e}")
        return self._model
    
    def summarize_text(self, text: str) -> str:
        """
        Summarize text using Gemini.
        
        Args:
            text: Text to summarize
            
        Returns:
            Summarized text
            
        Raises:
            SummarizationError: If summarization fails
        """
        if not text.strip():
            logger.warning("Attempted to summarize empty text")
            return "無法對空內容進行摘要。"
        
        prompt = self._create_summarization_prompt(text)
        
        try:
            logger.info(f"Starting summarization for text of length: {len(text)}")
            response = self.model.generate_content(
                prompt,
                safety_settings={
                    'HARASSMENT': 'BLOCK_NONE',
                    'HATE': 'BLOCK_NONE',
                    'SEXUAL': 'BLOCK_NONE',
                    'DANGEROUS': 'BLOCK_NONE'
                }
            )
            
            if not response.candidates:
                logger.warning("Gemini API returned no candidates")
                return "摘要服務暫時無法提供，請稍後再試。"
            
            summary = response.candidates[0].content.parts[0].text.strip()
            logger.info(f"Summarization completed successfully. Summary length: {len(summary)}")
            return summary
            
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            raise SummarizationError(f"文本摘要失敗：{str(e)}")
    
    def _create_summarization_prompt(self, text: str) -> str:
        """
        Create a summarization prompt for the given text.
        
        Args:
            text: Text to create prompt for
            
        Returns:
            Formatted prompt string
        """
        return f"""請將以下文本內容進行簡潔的摘要。重點提取關鍵資訊，並以條列式或一段話的形式呈現，控制在100字以內。

文本內容：
{text}

摘要：
"""
