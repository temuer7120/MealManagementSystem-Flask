from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache

# 创建数据库实例
db = SQLAlchemy()

# 创建JWT实例
jwt = JWTManager()

# 创建CORS实例
cors = CORS()

# 创建缓存实例
cache = Cache(config={
    'CACHE_TYPE': 'simple',  # 默认使用简单缓存
    'CACHE_DEFAULT_TIMEOUT': 300  # 默认缓存超时时间为300秒
})

# 配置Redis缓存选项
def configure_cache(app):
    """配置缓存"""
    cache_type = app.config.get('CACHE_TYPE', 'simple')
    if cache_type == 'redis':
        cache_config = {
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_URL': app.config.get('CACHE_REDIS_URL', 'redis://localhost:6379/0'),
            'CACHE_DEFAULT_TIMEOUT': 300
        }
        cache.init_app(app, config=cache_config)
    else:
        cache.init_app(app)
