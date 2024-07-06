import logging
from flask import request, g
from time import time
from functools import wraps

logger = logging.getLogger(__name__)

def setup_performance_monitoring(app):
    """
    Set up performance monitoring for the Flask application.
    
    Args:
        app (Flask): The Flask application instance.
    """
    @app.before_request
    def before_request():
        """Record the start time of each request."""
        g.start_time = time()

    @app.after_request
    def after_request(response):
        """
        Log the duration of each request after it's processed.
        
        Args:
            response: The response object.
        
        Returns:
            The unchanged response object.
        """
        if app.config['ENABLE_PERFORMANCE_MONITORING']:
            duration = (time() - g.start_time) * 1000  # Convert to milliseconds
            logger.info(f"Request to {request.path} took {duration:.2f} ms.")
        return response

def performance_monitor(f):
    """
    Decorator to monitor the performance of individual functions.
    
    Args:
        f: The function to be monitored.
    
    Returns:
        The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time()
        result = f(*args, **kwargs)
        if app.config['ENABLE_PERFORMANCE_MONITORING']:
            duration = (time() - start_time) * 1000  # Convert to milliseconds
            response_size = len(str(result))
            logger.info(f"API call to {request.path} took {duration:.2f} ms. Response size: {response_size} bytes.")
        return result
    return decorated_function