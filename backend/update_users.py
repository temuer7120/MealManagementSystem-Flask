from extensions import db
from models import User, Role, UserRole
from app import app

# 用户数据
users_data = [
    {'username': 'admin', 'password': 'admin123', 'role': 'admin', 'color_theme': '蓝色'},
    {'username': 'nutritionist', 'password': 'nutr123', 'role': 'nutr', 'color_theme': '蓝色'},
    {'username': 'chef', 'password': 'chef123', 'role': 'chef', 'color_theme': '绿色'},
    {'username': 'admin_staff', 'password': 'admin', 'role': 'admin_staff', 'color_theme': '绿色'},
    {'username': 'head_nurse', 'password': 'nurse', 'role': 'head_nurse', 'color_theme': '绿色'},
    {'username': 'nurse', 'password': 'nurse', 'role': 'nurse', 'color_theme': '绿色'},
    {'username': 'caregiver', 'password': 'care', 'role': 'caregiver', 'color_theme': '绿色'},
    {'username': 'customer', 'password': 'cust123', 'role': 'cust', 'color_theme': '浅粉色'},
    {'username': 'guest', 'password': 'guest123', 'role': 'guest', 'color_theme': '浅粉色'}
]

with app.app_context():
    try:
        # 删除所有用户角色关联
        UserRole.query.delete()
        db.session.flush()
        
        # 删除所有用户
        User.query.delete()
        db.session.flush()
        
        print("已删除所有现有用户数据")
        print("-" * 80)
        
        # 为每个用户创建账号
        for user_info in users_data:
            # 创建用户
            user = User(
                username=user_info['username'],
                color_theme=user_info['color_theme']
            )
            user.set_password(user_info['password'])
            db.session.add(user)
            db.session.flush()
            
            # 检查角色是否存在
            role = Role.query.filter_by(name=user_info['role']).first()
            if not role:
                # 创建新角色
                role = Role(
                    name=user_info['role'],
                    description=f'{user_info["role"]} role'
                )
                db.session.add(role)
                db.session.flush()
            
            # 创建用户角色关联
            user_role = UserRole(
                user_id=user.id,
                role_id=role.id
            )
            db.session.add(user_role)
            
            print(f"创建用户: {user_info['username']}, 角色: {user_info['role']}, 颜色: {user_info['color_theme']}")
        
        # 提交所有更改
        db.session.commit()
        
        print("-" * 80)
        print(f"成功创建 {len(users_data)} 个用户")
        
        # 验证创建结果
        users = User.query.all()
        print("\n创建的用户列表：")
        print("-" * 80)
        print(f"{'ID':<5} {'用户名':<20} {'角色':<15} {'颜色主题':<10}")
        print("-" * 80)
        
        for user in users:
            role_name = user.role if hasattr(user, 'role') else '无'
            color_theme = user.color_theme or '无'
            print(f"{user.id:<5} {user.username:<20} {role_name:<15} {color_theme:<10}")
        
        print("-" * 80)
        print(f"共 {len(users)} 个用户")
        
    except Exception as e:
        db.session.rollback()
        print(f"错误: {str(e)}")
