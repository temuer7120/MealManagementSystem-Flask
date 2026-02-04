from app import app
from extensions import db
from models import *

print("初始化数据库...")

with app.app_context():
    try:
        # 创建所有表
        db.create_all()
        print("数据库表创建成功！")
        
        # 检查创建的表
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"创建的表: {tables}")
        
    except Exception as e:
        print(f"数据库初始化错误: {str(e)}")
        import traceback
        traceback.print_exc()