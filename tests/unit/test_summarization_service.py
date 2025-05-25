"""
Unit tests for text summarization service.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from app.services.summarization_service import GeminiSummarizationService
from app.core.exceptions import SummarizationError

class TestGeminiSummarizationService(unittest.TestCase):
    """Test cases for GeminiSummarizationService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_api_key"
        
    @patch('app.services.summarization_service.genai.configure')
    def test_initialization_success(self, mock_configure):
        """Test successful service initialization."""
        service = GeminiSummarizationService(self.api_key)
        
        mock_configure.assert_called_once_with(api_key=self.api_key)
        self.assertEqual(service.api_key, self.api_key)
        self.assertEqual(service.model_name, "gemini-1.5-flash")
    
    @patch('app.services.summarization_service.genai.configure')
    def test_initialization_error(self, mock_configure):
        """Test initialization error handling."""
        mock_configure.side_effect = Exception("API configuration failed")
        
        with self.assertRaises(SummarizationError) as context:
            GeminiSummarizationService(self.api_key)
        
        self.assertIn("Failed to configure Gemini API", str(context.exception))
    
    @patch('app.services.summarization_service.genai.configure')
    @patch('app.services.summarization_service.genai.GenerativeModel')
    def test_model_lazy_loading(self, mock_generative_model, mock_configure):
        """Test that model is loaded lazily."""
        mock_model = Mock()
        mock_generative_model.return_value = mock_model
        
        service = GeminiSummarizationService(self.api_key)
        
        # Model should not be loaded initially
        self.assertIsNone(service._model)
        
        # Access model property should trigger loading
        model = service.model
        
        mock_generative_model.assert_called_once_with("gemini-1.5-flash")
        self.assertEqual(model, mock_model)
    
    @patch('app.services.summarization_service.genai.configure')
    def test_summarize_text_empty_input(self, mock_configure):
        """Test summarization with empty text."""
        service = GeminiSummarizationService(self.api_key)
        
        result = service.summarize_text("")
        self.assertEqual(result, "無法對空內容進行摘要。")
        
        result = service.summarize_text("   ")
        self.assertEqual(result, "無法對空內容進行摘要。")
    
    @patch('app.services.summarization_service.genai.configure')
    def test_summarize_text_success(self, mock_configure):
        """Test successful text summarization."""
        service = GeminiSummarizationService(self.api_key)
        
        # Mock the model and response
        mock_model = Mock()
        mock_response = Mock()
        mock_candidate = Mock()
        mock_content = Mock()
        mock_part = Mock()
        
        mock_part.text = "This is a summary"
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        mock_model.generate_content.return_value = mock_response
        
        service._model = mock_model
        
        result = service.summarize_text("This is a long text to summarize")
        
        self.assertEqual(result, "This is a summary")
        mock_model.generate_content.assert_called_once()
    
    @patch('app.services.summarization_service.genai.configure')
    def test_summarize_text_no_candidates(self, mock_configure):
        """Test summarization when API returns no candidates."""
        service = GeminiSummarizationService(self.api_key)
        
        mock_model = Mock()
        mock_response = Mock()
        mock_response.candidates = []
        mock_model.generate_content.return_value = mock_response
        
        service._model = mock_model
        
        result = service.summarize_text("Test text")
        
        self.assertEqual(result, "摘要服務暫時無法提供，請稍後再試。")
    
    @patch('app.services.summarization_service.genai.configure')
    def test_summarize_text_error(self, mock_configure):
        """Test summarization error handling."""
        service = GeminiSummarizationService(self.api_key)
        
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API call failed")
        service._model = mock_model
        
        with self.assertRaises(SummarizationError) as context:
            service.summarize_text("Test text")
        
        self.assertIn("文本摘要失敗", str(context.exception))
    
    @patch('app.services.summarization_service.genai.configure')
    def test_create_summarization_prompt(self, mock_configure):
        """Test prompt creation."""
        service = GeminiSummarizationService(self.api_key)
        
        text = "Test text"
        prompt = service._create_summarization_prompt(text)
        
        self.assertIn(text, prompt)
        self.assertIn("摘要", prompt)
        self.assertIn("100字以內", prompt)

if __name__ == '__main__':
    unittest.main()
