from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from werkzeug.exceptions import BadRequest
from main import optimized_search_hot_posts

app = Flask(__name__)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["100 per day", "20 per hour"]
)

# Cache Configuration
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="Rate limit exceeded", description=str(e.description)), 429

@app.route('/search', methods=['POST'])
@limiter.limit("5 per minute")
def search():
    try:
        data = request.json
        if not data:
            raise BadRequest("Missing JSON data in request body")

        keyword = data.get('keyword')
        platforms = data.get('platforms', ['reddit', 'hackernews', 'github'])

        if not keyword:
            raise BadRequest("Missing 'keyword' in request")

        if not isinstance(keyword, str):
            raise BadRequest("'keyword' must be a string")

        if not isinstance(platforms, list):
            raise BadRequest("'platforms' must be a list")

        valid_platforms = {'reddit', 'hackernews', 'github', 'theresanaiforthat', 'v2ex'}
        if not set(platforms).issubset(valid_platforms):
            raise BadRequest(f"Invalid platform(s). Valid platforms are: {', '.join(valid_platforms)}")
        
        # try get cache result
        cache_key = f"{keyword}_{'_'.join(platforms)}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return jsonify(cached_result)

        
        results, search_times = optimized_search_hot_posts(keyword, platforms)
        response = {
            "results": results,
            "search_times": search_times
        }
        cache.set(cache_key, response, timeout=600)  # cache 10 mins
        
        # results = search_hot_posts(keyword, platforms)
        return jsonify(response)

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)