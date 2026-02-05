from app import app
from extensions import db
from models import Role, User, UserRole

with app.app_context():
    # 检查角色列表
    print('角色列表:')
    roles = Role.query.all()
    for role in roles:
        print(f'  - {role.name} (ID: {role.id})')
    
    # 检查用户角色关联
    print('\n用户角色关联:')
    users = User.query.all()
    for user in users:
        roles = [ur.role.name for ur in user.user_roles]
        print(f'  {user.username}: {roles}')
