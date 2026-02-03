from extensions import db
from models import User
from app import app

with app.app_context():
    # 查询所有用户
    users = User.query.all()
    
    print("数据库中的用户信息：")
    print("-" * 80)
    print(f"{'ID':<5} {'用户名':<20} {'密码哈希':<60}")
    print("-" * 80)
    
    for user in users:
        print(f"{user.id:<5} {user.username:<20} {user.password_hash:<60}")
    
    print("-" * 80)
    print(f"共 {len(users)} 个用户")
    print("注意：密码是以哈希形式存储的，不是明文密码")
