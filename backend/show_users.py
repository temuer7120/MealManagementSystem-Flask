from app import app
from models import User, Role, UserRole

with app.app_context():
    print("=" * 50)
    print("系统登录账号信息")
    print("=" * 50)
    
    users = User.query.all()
    
    if not users:
        print("数据库中没有用户！")
    else:
        print(f"\n总共有 {len(users)} 个用户\n")
        
        for i, user in enumerate(users, 1):
            print(f"{i}. 用户名: {user.username}")
            print(f"   姓名: {user.full_name or '未设置'}")
            print(f"   邮箱: {user.email or '未设置'}")
            print(f"   部门: {user.department or '未设置'}")
            print(f"   职位: {user.position or '未设置'}")
            print(f"   状态: {'激活' if user.is_active else '未激活'}")
            
            roles = [ur.role.name for ur in user.user_roles]
            print(f"   角色: {', '.join(roles) if roles else '未设置'}")
            print(f"   默认密码: 123456")
            print()
    
    print("=" * 50)
    print("注意：所有用户的默认密码都是: 123456")
    print("=" * 50)
