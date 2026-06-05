import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    DB_NAME = 'srmss_rbac.db'
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    CORS_ORIGINS = ["https://yourdomain.com"]

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DB_NAME = 'test_srmss.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}