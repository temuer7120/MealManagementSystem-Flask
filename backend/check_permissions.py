from app import app, db
from models import Role, Permission, RolePermission

with app.app_context():
    # 检查所有角色
    print('=== 角色列表 ===')
    roles = Role.query.all()
    for role in roles:
        print(f'角色: {role.name} - {role.description}')
        # 检查角色的权限
        role_perms = RolePermission.query.filter_by(role_id=role.id).all()
        if role_perms:
            perm_ids = [rp.permission_id for rp in role_perms]
            permissions = Permission.query.filter(Permission.id.in_(perm_ids)).all()
            print(f'  权限数量: {len(permissions)}')
            for perm in permissions:
                print(f'    - {perm.name} ({perm.code})')
        else:
            print(f'  权限数量: 0 (无权限)')
        print()
    
    # 检查所有权限
    print('=== 权限列表 ===')
    permissions = Permission.query.all()
    print(f'总权限数: {len(permissions)}')
    for perm in permissions:
        print(f'  - {perm.name} ({perm.code}) - 模块: {perm.module}')
