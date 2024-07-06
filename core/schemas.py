from marshmallow import Schema, fields, validate
from .config import Config

class SearchSchema(Schema):
    """
    Schema for validating search requests.
    
    Attributes:
        keyword (str): The search keyword (required).
        platforms (list): List of platforms to search (optional, must be from the allowed list).
    """
    keyword = fields.Str(required=True, validate=validate.Length(min=1))
    platforms = fields.List(
        fields.Str(),
        validate=validate.ContainsOnly(Config.DEFAULT_PLATFORMS)
    )