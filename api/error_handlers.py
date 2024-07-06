from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        
        if isinstance(e, HTTPException):
            return jsonify(error=str(e)), e.code
        
        return jsonify(error="An internal server error occurred"), 500