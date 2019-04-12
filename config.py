import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_caching import Cache

# creating flask app
app = Flask(__name__)


# database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')
db = SQLAlchemy(app)

# for limiter to create cache in redis
app.config['RATELIMIT_STORAGE_URL'] = 'redis://localhost:6379'

# for data serialization/render json response
marsh_app = Marshmallow(app)


cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'Company',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://localhost:6379'
})

DEFAULT_LIMIT = "0/day, 0/minute"