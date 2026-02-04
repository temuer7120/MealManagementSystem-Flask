from app import app
from extensions import db

with app.app_context():
    # 获取数据库连接
    conn = db.engine.connect()
    
    # 检查user表的结构
    result = conn.execute("PRAGMA table_info(user)")
    columns = result.fetchall()
    
    print("User table structure:")
    for column in columns:
        print(f"  {column[1]}: {column[2]}")
    
    conn.close()