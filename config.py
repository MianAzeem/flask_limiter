from flask_marshmallow import Marshmallow

from flask_caching import Cache
from manage import app
from flask_jwt_extended import JWTManager
import datetime

# app.config['JWT_SECRET_KEY'] = 'ZPFbC2Mbe8ipp79NqRUwO9BrFKE5ZKfx'
app.config['JWT_SECRET_KEY'] = 'abcdefg' # secret key for verification
jwt = JWTManager(app)


# create cache in redis supported by limiter
app.config['RATELIMIT_STORAGE_URL'] = 'redis://localhost:6379'

# for data serialization/render json response
marsh_app = Marshmallow(app)


# redis configuration
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'Company',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://localhost:6379'
})


class CompanySchema(marsh_app.Schema):
    class Meta:
        fields = ('name', 'identity','limit')

# for single company
company_schema = CompanySchema()
# for all companies
company_schema = CompanySchema(many=True)
