from flask import jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError
from api.schemas import SearchSchema
from core.performance import performance_monitor
from core.cache import generate_cache_key, cache_get, cache_set
from core.posts_search import optimized_search_hot_posts
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def register_routes(app):
    limiter = Limiter(
      get_remote_address,
      app=app,
      storage_uri=app.config['CACHE_REDIS_URL'],
      storage_options={"socket_connect_timeout": 30},
      strategy=app.config['RATELIMIT_STRATEGY'],
    )

    @app.route('/v1/search', methods=['POST'])
    @limiter.limit("5 per minute")
    @performance_monitor
    def search():
        """
        Handle POST requests to the /v1/search endpoint.
        Perform a search across platforms based on the provided keyword and platforms.
    
        Returns:
            JSON response with search results or cached results if available.
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
        schema = SearchSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            logger.error(f"search function invalid input: {err.messages}")
            raise BadRequest(str(err.messages))
        
        keyword = data['keyword']
        platforms = data.get('platforms', app.config['DEFAULT_PLATFORMS'])

        cache_key = generate_cache_key(keyword, platforms)
        cached_result = cache_get(cache_key)
        if cached_result:
            return jsonify(cached_result)

        results, search_times = optimized_search_hot_posts(keyword, platforms)
        response = {
            "results": results,
            "search_times": search_times
        }
        # cache for 1hr
        cache_set(cache_key, response, 3600)
        
        return jsonify(response)