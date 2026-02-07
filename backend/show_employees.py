from app import create_app
from models import User, Role, UserRole

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f'总用户数: {len(users)}')
    print('\n员工列表:')
    print('-' * 80)
    
    for user in users:
        user_roles = UserRole.query.filter_by(user_id=user.id).all()
        role_names = []
        for ur in user_roles:
            role = Role.query.get(ur.role_id)
            if role:
                role_names.append(role.name)
        
        print(f'ID: {user.id:3d} | 用户名: {user.username:20s} | 角色: {", ".join(role_names) if role_names else "无"}')
    
    print('-' * 80)
    print(f'\n总计: {len(users)} 名员工')
