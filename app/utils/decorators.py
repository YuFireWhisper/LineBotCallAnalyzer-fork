"""
Utility functions for the application.
"""
import logging
import functools
from typing import Callable, Any

logger = logging.getLogger(__name__)

def log_execution_time(func: Callable) -> Callable:
    """
    Decorator to log function execution time.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        import time
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f} seconds: {e}")
            raise
    
    return wrapper

def safe_execute(func: Callable, default_return: Any = None, log_errors: bool = True) -> Callable:
    """
    Decorator to safely execute functions with error handling.
    
    Args:
        func: Function to decorate
        default_return: Default return value on error
        log_errors: Whether to log errors
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if log_errors:
                logger.error(f"Error in {func.__name__}: {e}")
            return default_return
    
    return wrapper
