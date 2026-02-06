from app import app
from models import Role

with app.app_context():
    roles = Role.query.all()
    print("数据库中的角色:")
    for role in roles:
        print(f"  - {role.name}: {role.description}")
