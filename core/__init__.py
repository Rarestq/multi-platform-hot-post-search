from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flasgger import Swagger
from flask_apscheduler import APScheduler

from .config import Config
from .performance_monitor import setup_performance_monitoring
from .api import app
from .main import optimized_search_hot_posts

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    # Initialize the Flask application
    app = Flask(__name__)
    
    # Load configuration from Config object
    app.config.from_object(Config)

    # Initialize Flask extensions
    CORS(app)  # Enable Cross-Origin Resource Sharing
    Limiter(app, key_func=get_remote_address)  # Set up rate limiting
    Cache(app)  # Initialize caching
    Swagger(app)  # Set up Swagger for API documentation
    
    # Initialize and start the scheduler for background tasks
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    # Set up performance monitoring
    setup_performance_monitoring(app)

    # Register the API blueprint
    from .api import api_bp
    app.register_blueprint(api_bp)

    return app