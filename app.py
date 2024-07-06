from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flasgger import Swagger
from config import Config
from api.routes import register_routes
from api.error_handlers import register_error_handlers
from core.performance import setup_performance_monitoring
from api.routes import register_routes
from core.tasks import init_scheduler, register_cache_preheat, shutdown_scheduler_and_thread_pool
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# TODO by rarestzhou: set config by env: prod, dev
# config = ProductionConfig() if os.environ.get("FLASK_ENV") == "production" else DevelopmentConfig()

class EnvFileHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_modified(self, event):
        if event.src_path.endswith('.env'):
            with self.app.app_context():
                Config.reload()
                logger.info("Reloaded configuration from .env file.")

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
    Cache(app)  # Initialize caching
    Swagger(app)  # Set up Swagger for API documentation, use /apidocs to see swagger docs
        
    # Register routes, error handlers, performance_monitoring
    register_routes(app)
    register_error_handlers(app)
    setup_performance_monitoring(app)
    
    # set .env file monitor
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    event_handler = EnvFileHandler(app)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(env_path), recursive=False)
    observer.start()
    
    # Initialize and start the scheduler for background tasks
    init_scheduler(app)
    register_cache_preheat(app)
    shutdown_scheduler_and_thread_pool(app)

    return app

def create_test_app():
    app = Flask(__name__)
    app.config.from_object(Config) 
    CORS(app)
    Cache(app)
    register_routes(app)
    register_error_handlers(app)
    
    return app