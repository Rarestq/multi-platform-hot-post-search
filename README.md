# Cross-Platform Search Project

This project implements a cross-platform search API that allows users to search for hottest posts by keyword across multiple platforms including Reddit, Hacker News, GitHub, V2EX, and TheresAnAIForThat.

## Features

- Search across multiple platforms with a single API call
- Caching mechanism for improved performance
- Rate limiting to prevent abuse
- Keyword translation for non-English queries
- Performance monitoring
- Swagger documentation

## Project Structure

```
.
├── api
│   ├── error_handlers.py
│   ├── routes.py
│   └── schemas.py
├── core
│   ├── emails
│   └── platforms
│       ├── __init__.py
│       ├── github_repos_search.py
│       ├── hackernews_search.py
│       ├── platform.py
│       ├── reddit_search.py
│       ├── theresanaifforthat_search.py
│       ├── twitter_search_v2_oauth.py
│       ├── twitter_search.py
│       ├── v2ex_search_google.py
│       └── v2ex_search.py
│   ├── __init__.py
│   ├── cache.py
│   ├── cli.py
│   ├── models.py
│   ├── performance.py
│   ├── posts_search.py
│   ├── tasks.py
│   ├── translator.py
│   └── utils.py
├── tests
│   ├── conftest.py
│   └── test_search_api.py
├── utils
│   └── env_manager.py
├── venv
├── .env
├── .gitignore
├── app.py
├── config.py
├── main.py
├── pytest.ini
├── README.md
├── requirements.txt
└── run.py
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Rarestq/multi-platform-hot-post-search.git
   cd multi-platform-hot-post-search
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy the `.env.example` file to `.env`
   - Fill in the necessary API keys and configuration options

## Usage

1. Start the Flask server:
   ```
   python run.py
   ```

2. The API will be available at `http://localhost:5000`

3. Use the `/v1/search` endpoint to perform searches:
   ```
   POST /v1/search
   Content-Type: application/json

   {
     "keyword": "artificial intelligence",
     "platforms": ["reddit", "hackernews", "github"]
   }
   ```
   you can use `curl` command to send post request:
   ```bash
   curl -X POST http://127.0.0.1:5000/search \
     -H "Content-Type: application/json" \
     -d '{"keyword": "AI", "platforms": ["reddit", "hackernews", "github"]}'
   ```
   if your computer's system is Windows, then use `curl` command like below:
   ```bash
   curl -X POST http://127.0.0.1:5000/search -H "Content-Type: application/json" -d "{\"keyword\": \"AI\", \"platforms\": [\"reddit\", \"hackernews\", \"github\"]}"
   ```

4. View the Swagger documentation at `http://localhost:5000/apidocs`

## Configuration

The following environment variables can be used to configure the application:

- `RATELIMIT_DEFAULT`: Default rate limit (e.g., "100 per day, 20 per hour")
- `CACHE_TYPE`: Type of cache to use (default: "simple")
- `CACHE_DEFAULT_TIMEOUT`: Default cache timeout in seconds (default: 600)
- `HOT_KEYWORDS`: Comma-separated list of hot keywords for cache preheating
- `ENABLE_PERFORMANCE_MONITORING`: Enable/disable performance monitoring (default: True)
- `LOG_LEVEL`: Logging level (default: INFO)
- `DEFAULT_PLATFORMS`: Comma-separated list of default platforms to search
- etc.

## Testing

This project uses pytest for testing. To run the tests:

```
pytest
```

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature`)
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`)
5. Push to the branch (`git push origin feature`)
6. Create a new Pull Request.

## Sponsor

<a href='https://ko-fi.com/rarestzhou' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi5.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

![Sponsor me by wechat](https://img.mini-url.top/file/7571504552e403f309a0b.jpg)

## Contact

- Email: rarestzhou@gmail.com
- DM me on [twitter](https://twitter.com/rarestzhou) is also welcome.
- Wechat: zjc111369
![WeChat QR Code](https://mmbiz.qpic.cn/mmbiz_jpg/KhD0fibB4GCDFlkCNLH5B7xiaIlGSWFSbXEtCYRJQ7fzsvb447XhJm35pkgjN75e0IfAbIBp5hdfl15ke3VJkdog/640?wx_fmt=jpeg)

---

Feel free to customize this README further based on your specific project details and requirements!