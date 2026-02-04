from app import app
from extensions import db
from models import User, Role, UserRole

def create_test_users():
    with app.app_context():
        # 检查用户是否已存在
        existing_users = User.query.all()
        existing_usernames = [user.username for user in existing_users]
        
        # 确保角色表存在必要的角色
        def get_or_create_role(role_name):
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name, description=f'{role_name} role')
                db.session.add(role)
                db.session.commit()
            return role
        
        # 创建必要的角色
        admin_role = get_or_create_role('admin')
        nutritionist_role = get_or_create_role('nutritionist')
        user_role = get_or_create_role('user')
        guest_role = get_or_create_role('guest')
        chef_role = get_or_create_role('chef')
        
        # 创建管理员用户
        if 'admin' not in existing_usernames:
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.flush()  # 获取用户ID
            
            # 关联角色
            user_role = UserRole(user_id=admin.id, role_id=admin_role.id)
            db.session.add(user_role)
            print('创建管理员用户: admin / admin123')
        else:
            print('管理员用户已存在')
        
        # 创建营养师用户
        if 'nutritionist' not in existing_usernames:
            nutritionist = User(username='nutritionist')
            nutritionist.set_password('nutr123')
            db.session.add(nutritionist)
            db.session.flush()  # 获取用户ID
            
            # 关联角色
            user_role = UserRole(user_id=nutritionist.id, role_id=nutritionist_role.id)
            db.session.add(user_role)
            print('创建营养师用户: nutritionist / nutr123')
        else:
            print('营养师用户已存在')
        
        # 创建普通用户
        if 'user' not in existing_usernames:
            normal_user = User(username='user')
            normal_user.set_password('user123')
            db.session.add(normal_user)
            db.session.flush()  # 获取用户ID
            
            # 关联角色
            user_role = UserRole(user_id=normal_user.id, role_id=user_role.id)
            db.session.add(user_role)
            print('创建普通用户: user / user123')
        else:
            print('普通用户已存在')
        
        # 创建访客用户
        if 'guest' not in existing_usernames:
            guest = User(username='guest')
            guest.set_password('guest123')
            db.session.add(guest)
            db.session.flush()  # 获取用户ID
            
            # 关联角色
            user_role = UserRole(user_id=guest.id, role_id=guest_role.id)
            db.session.add(user_role)
            print('创建访客用户: guest / guest123')
        else:
            print('访客用户已存在')
        
        # 创建厨师用户
        if 'chef' not in existing_usernames:
            chef = User(username='chef')
            chef.set_password('chef123')
            db.session.add(chef)
            db.session.flush()  # 获取用户ID
            
            # 关联角色
            user_role = UserRole(user_id=chef.id, role_id=chef_role.id)
            db.session.add(user_role)
            print('创建厨师用户: chef / chef123')
        else:
            print('厨师用户已存在')
        
        # 提交更改
        db.session.commit()
        print('\n所有测试用户创建完成！')
        print('\n用户列表：')
        users = User.query.all()
        for user in users:
            roles = [ur.role.name for ur in user.user_roles]
            role_str = ', '.join(roles) if roles else 'user'
            print(f'  - {user.username} ({role_str})')

if __name__ == '__main__':
    create_test_users()
