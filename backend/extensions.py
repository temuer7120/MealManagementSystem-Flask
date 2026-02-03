from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# 创建数据库实例
db = SQLAlchemy()

# 创建JWT实例
jwt = JWTManager()

# 创建CORS实例
cors = CORS()
