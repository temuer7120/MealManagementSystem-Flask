from app import app
from extensions import db
from models import User, Role, UserRole

def verify_admin():
    with app.app_context():
        # 查询管理员用户
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print('管理员账号信息：')
            print(f'用户名: {admin.username}')
            print(f'邮箱: {admin.email}')
            print(f'姓名: {admin.full_name}')
            print(f'是否激活: {"是" if admin.is_active else "否"}')
            print(f'是否超级管理员: {"是" if admin.is_superuser else "否"}')
            print(f'创建时间: {admin.created_at}')
            
            # 查询角色
            roles = [ur.role for ur in admin.user_roles]
            if roles:
                print(f'角色: {", ".join([role.name for role in roles])}')
                for role in roles:
                    print(f'  - {role.name}: {role.description}')
            else:
                print('角色: 未分配')
        else:
            print('未找到管理员账号')

if __name__ == '__main__':
    verify_admin()
