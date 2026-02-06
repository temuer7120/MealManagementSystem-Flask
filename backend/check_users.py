from app import app
from models import User, Role, UserRole

with app.app_context():
    print("用户列表:")
    users = User.query.all()
    for user in users:
        roles = [ur.role.name for ur in user.user_roles]
        print(f"  - {user.username} ({user.full_name}): 角色={roles}, 部门={user.department}, 职位={user.position}")
