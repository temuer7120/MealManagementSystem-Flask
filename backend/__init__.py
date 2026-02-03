from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# 创建数据库实例
db = SQLAlchemy()

# 创建JWT实例
jwt = JWTManager()

# 创建应用实例
def create_app():
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_pyfile('config.py')
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化JWT
    jwt.init_app(app)
    
    # 注册蓝图
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    return app
