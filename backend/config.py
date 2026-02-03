import os

# 数据库配置
SQLALCHEMY_DATABASE_URI = 'sqlite:///meal_management.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT配置
JWT_SECRET_KEY = 'your-secret-key-here'

# 上传文件配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
