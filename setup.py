from setuptools import setup, find_packages

setup(
    name="cross_platform_search",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-Limiter',
        'Flask-Caching',
        'marshmallow',
        'Flask-CORS',
        'flasgger',
        'Flask-APScheduler',
        'google-cloud-translate',
        'python-dotenv',
    ],
)