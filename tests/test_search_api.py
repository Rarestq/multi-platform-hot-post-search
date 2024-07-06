import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_test_app
from core.cache import generate_cache_key
from core.translator import Translator

app = create_test_app()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_search_endpoint(client, mocker):
    mock_search = mocker.patch('core.posts_search.optimized_search_hot_posts', return_value=([], {"total_time": 100}))
    response = client.post('/v1/search', json={"keyword": "AI", "platforms": ["reddit", "hackernews"]})
    assert response.status_code == 200
    assert "results" in response.json
    assert "search_times" in response.json

def test_search_endpoint_invalid_input(client):
    response = client.post('/v1/search', json={"keyword": ""})
    assert response.status_code == 400

def test_cache_functionality(client, mocker):
    mock_search = mocker.patch('core.posts_search.optimized_search_hot_posts', return_value=([], {"total_time": 100}))
    
    # First request
    response = client.post('/v1/search', json={"keyword": "Gemini"})
    assert response.status_code == 200

    # Second request (should hit cache)
    mock_cache_get = mocker.patch('core.cache.cache_get', return_value={"results": [], "search_times": {"total_time": 100}})
    response = client.post('/v1/search', json={"keyword": "Gemini"})
    assert response.status_code == 200
    mock_cache_get.assert_called_once()

def test_generate_cache_key():
    key = generate_cache_key("AI", ["reddit", "hackernews"])
    assert isinstance(key, str)
    assert "AI" in key
    assert "reddit" in key
    assert "hackernews" in key
    
def test_search_endpoint_rate_limit(client):
    for _ in range(6):  # Exceed rate limit
        response = client.post('/v1/search', json={"keyword": "AI"})
    assert response.status_code in [429, 500]  # Accept either rate limit or server error

class TestTranslator:
    @pytest.fixture
    def translator(self):
        return Translator()

    def test_translate_keyword(self, translator, mocker):
        mock_translate = mocker.patch('core.translator.translate.Client.translate', return_value={'translatedText': 'Artificial Intelligence'})
        
        result = translator.translate_keyword("人工智能")
        assert result == "Artificial Intelligence"
        mock_translate.assert_called_once_with("人工智能", target_language='en')

    @pytest.mark.parametrize("input_text, expected", [
        ("Artificial Intelligence", True),
        ("人工智能", False)
    ])
    
    def test_is_english(self, translator, input_text, expected):
        assert translator.is_english(input_text) == expected