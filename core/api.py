from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from werkzeug.exceptions import BadRequest
from marshmallow import Schema, fields, validate, ValidationError
from flask_cors import CORS
from flasgger import Swagger # use /apidocs to see swagger docs
from flask_apscheduler import APScheduler
from typing import List
from flask import Flask, request, jsonify, g
import time
from functools import wraps
from core.main import optimized_search_hot_posts
import logging
import os

app = Flask(__name__)
CORS(app)

# Load configuration from environment variables
app.config['RATELIMIT_DEFAULT'] = os.getenv('RATELIMIT_DEFAULT', "100 per day, 20 per hour")
app.config['CACHE_TYPE'] = os.getenv('CACHE_TYPE', 'simple')
app.config['CACHE_DEFAULT_TIMEOUT'] = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 600))
app.config['HOT_KEYWORDS'] = os.getenv('HOT_KEYWORDS', 'AI,Claude,Gemini').split(',')
app.config['ENABLE_PERFORMANCE_MONITORING'] = os.getenv('ENABLE_PERFORMANCE_MONITORING', 'True').lower() == 'true'
app.config['LOG_LEVEL'] = os.getenv('LOG_LEVEL', 'INFO')

# Setup logging
logging.basicConfig(level=app.config['LOG_LEVEL'])
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address, app=app)
cache = Cache(app)
swagger = Swagger(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

class SearchSchema(Schema):
    keyword = fields.Str(required=True, validate=validate.Length(min=1))
    platforms = fields.List(fields.Str(), validate=validate.ContainsOnly(['reddit', 'hackernews', 'github', 'theresanaiforthat', 'v2ex']))
    
def performance_monitor(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if app.config['ENABLE_PERFORMANCE_MONITORING']:
            start_time = time.time()
        
        result = f(*args, **kwargs)
        
        if app.config['ENABLE_PERFORMANCE_MONITORING']:
            duration = (time.time() - start_time) * 1000  # Convert to milliseconds
            response_size = len(str(result))
            logger.info(f"API call to {request.path} took {duration:.2f} ms. Response size: {response_size} bytes.")
        
        return result
    return decorated_function

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    if app.config['ENABLE_PERFORMANCE_MONITORING']:
        duration = (time.time() - g.start_time) * 1000
        logger.info(f"Request to {request.path} took {duration:.2f} ms.")
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, BadRequest):
        return jsonify(error=str(e)), 400
    logger.error(f"An error occurred: {str(e)}")
    return jsonify(error="An internal server error occurred"), 500

@app.route('/v1/search', methods=['POST'])
@limiter.limit("5 per minute")
@performance_monitor
def search():
    """
    Search for posts across multiple platforms
    ---
    tags:
      - Search
    parameters:
      - in: body
        name: body
        schema:
          id: SearchInput
          required:
            - keyword
          properties:
            keyword:
              type: string
              description: The keyword to search for
            platforms:
              type: array
              items:
                type: string
              description: List of platforms to search (optional)
    responses:
      200:
        description: Successful search results
      400:
        description: Bad request (invalid input)
      429:
        description: Rate limit exceeded
      500:
        description: Internal server error
    """
    start_time = time.time()

    schema = SearchSchema()  
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        logger.error(f"search function invalid input: {err.messages}")
        raise BadRequest(str(err.messages))
    
    keyword = data['keyword']
    platforms = data.get('platforms', get_default_platforms())

    cache_key = generate_cache_key(keyword, platforms)
    cached_result = cache.get(cache_key)
    if cached_result:
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        logger.info(f"Cache hit for {cache_key}. Response time: {response_time:.2f} ms")
        return jsonify(cached_result)

    results, search_times = optimized_search_hot_posts(keyword, platforms)
    response = {
        "results": results,
        "search_times": search_times
    }
    cache.set(cache_key, response)
    
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    response_size = len(str(response))
    app.logger.info(f"Search completed for {cache_key}. Response time: {response_time:.2f}ms, Size: {response_size} bytes")

    return jsonify(response)

@scheduler.task('cron', id='cache_preheating', minute='*/30')
@performance_monitor
def cache_preheating():
    """Preheat cache for hot keywords every 30 minutes"""
    logger.info("Starting cache preheating...")
    default_platforms = get_default_platforms()
    for keyword in app.config['HOT_KEYWORDS']:
        cache_key = generate_cache_key(keyword, default_platforms)
        if not cache.get(cache_key):
            results, search_times = optimized_search_hot_posts(keyword, default_platforms)
            response = {
                "results": results,
                "search_times": search_times
            }
            cache.set(cache_key, response)
            app.logger.info(f"Preheated cache for keyword: {keyword}")
    app.logger.info("Cache preheating completed")
    
def get_default_platforms() -> List[str]:
    return os.getenv('DEFAULT_PLATFORMS', 'reddit,hackernews,github,v2ex,theresanaiforthat').split(',')

def generate_cache_key(keyword: str, platforms: List[str] = None) -> str:
    if platforms is None:
        platforms = get_default_platforms()
    platforms_str = '_'.join(sorted(platforms))  # Sort to ensure consistency
    return f"{keyword}_cross_platforms_{platforms_str}"

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')