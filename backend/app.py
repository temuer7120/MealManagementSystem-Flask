from flask import Flask, send_from_directory, request, jsonify
import os
import threading
import time
from extensions import db, jwt, configure_cache
import config
from utils.monitoring import start_monitoring_server, collect_system_metrics, health_check

# 创建应用实例
def create_app():
    app = Flask(__name__)
    
    # 加载配置
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = config.ALLOWED_EXTENSIONS
    app.config['CACHE_TYPE'] = os.getenv('CACHE_TYPE', 'simple')
    app.config['CACHE_REDIS_URL'] = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379/0')
    
    # 确保上传文件夹存在
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化JWT
    jwt.init_app(app)
    
    # 初始化CORS
    from extensions import cors
    # 安全的CORS配置，只允许特定来源
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
    cors.init_app(app, resources={r"/api/*": {"origins": cors_origins}})
    
    # 初始化缓存
    configure_cache(app)
    
    # 启动监控服务器
    def start_monitoring():
        start_monitoring_server()
        # 定期收集系统指标
        while True:
            collect_system_metrics()
            time.sleep(30)  # 每30秒收集一次
    
    # 在后台线程中启动监控
    monitoring_thread = threading.Thread(target=start_monitoring, daemon=True)
    monitoring_thread.start()
    
    # 注册蓝图
    from routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    # 健康检查端点
    @app.route('/health')
    def health_check_endpoint():
        status = health_check()
        return jsonify(status)
    
    # 监控指标端点
    @app.route('/metrics')
    def metrics():
        from prometheus_client import generate_latest
        return generate_latest(), 200, {'Content-Type': 'text/plain'}
    
    # 静态文件服务
    @app.route('/')
    def serve_index():
        return send_from_directory('../frontend/dist', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static_or_index(path):
        # 检查是否是实际的静态文件
        static_path = os.path.join('../frontend/dist', path)
        if os.path.exists(static_path) and os.path.isfile(static_path):
            return send_from_directory('../frontend/dist', path)
        # 否则返回 index.html，让前端路由处理
        return send_from_directory('../frontend/dist', 'index.html')
    
    return app

app = create_app()

# 初始化数据库
with app.app_context():
    # 导入所有模型，确保它们被注册到SQLAlchemy
    from models import *
    db.create_all()

if __name__ == '__main__':
    print("启动Flask应用程序...")
    print("监听地址: 0.0.0.0:5000")
    print("API基础路径: http://localhost:5000/api")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
