from app import app
from extensions import db
from models import User, Role, UserRole

def add_admin():
    with app.app_context():
        # 创建管理员角色
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(
                name='admin',
                description='系统管理员，拥有所有权限',
                is_system_role=True
            )
            db.session.add(admin_role)
            db.session.commit()
            print('创建管理员角色成功')
        else:
            print('管理员角色已存在')
        
        # 创建管理员用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                full_name='系统管理员',
                is_active=True,
                is_superuser=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.flush()  # 获取用户ID
            
            # 关联管理员角色
            user_role = UserRole(user_id=admin.id, role_id=admin_role.id)
            db.session.add(user_role)
            db.session.commit()
            print('创建管理员用户成功')
            print('用户名: admin')
            print('密码: admin123')
        else:
            print('管理员用户已存在')

if __name__ == '__main__':
    add_admin()
