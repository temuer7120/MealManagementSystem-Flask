import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:MySQL@localhost:3306/meal_management')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT配置
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'MySQL')

# 上传文件配置
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'xlsx,xls').split(','))

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
