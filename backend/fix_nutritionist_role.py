from app import app
from extensions import db
from models import User, UserRole, Role

with app.app_context():
    # 查找nutritionist用户
    nutritionist_user = User.query.filter_by(username='nutritionist').first()
    if nutritionist_user:
        print(f'找到nutritionist用户: {nutritionist_user.username}')
        
        # 查找当前关联的角色
        current_roles = [ur.role.name for ur in nutritionist_user.user_roles]
        print(f'当前关联角色: {current_roles}')
        
        # 删除当前的角色关联
        for ur in nutritionist_user.user_roles:
            db.session.delete(ur)
        print('已删除当前角色关联')
        
        # 查找nutritionist角色
        nutritionist_role = Role.query.filter_by(name='nutritionist').first()
        if nutritionist_role:
            print(f'找到nutritionist角色: {nutritionist_role.name} (ID: {nutritionist_role.id})')
            
            # 创建新的角色关联
            new_user_role = UserRole(user_id=nutritionist_user.id, role_id=nutritionist_role.id)
            db.session.add(new_user_role)
            print('已创建新的角色关联')
            
            # 提交更改
            db.session.commit()
            print('更改已提交')
            
            # 验证修改结果
            updated_roles = [ur.role.name for ur in nutritionist_user.user_roles]
            print(f'更新后的角色关联: {updated_roles}')
        else:
            print('未找到nutritionist角色')
    else:
        print('未找到nutritionist用户')
