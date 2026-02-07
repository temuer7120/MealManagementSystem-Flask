from extensions import db
from models import Role

# 角色数据
roles = [
    {"name": "nutritionist", "description": "营养师", "is_system_role": True},
    {"name": "chef", "description": "厨师", "is_system_role": True},
    {"name": "nurse", "description": "护士", "is_system_role": True},
    {"name": "caregiver", "description": "护理员", "is_system_role": True}
]

def create_roles():
    """创建必要的角色"""
    print("开始创建角色...")
    
    for role_data in roles:
        # 检查是否已存在
        existing = Role.query.filter_by(name=role_data["name"]).first()
        if existing:
            print(f"角色 {role_data['name']} 已存在，跳过")
            continue
        
        # 创建角色
        role = Role(
            name=role_data["name"],
            description=role_data["description"],
            is_system_role=role_data["is_system_role"]
        )
        db.session.add(role)
        print(f"创建角色 {role_data['name']} 成功")
    
    # 提交事务
    db.session.commit()
    print("角色创建完成！")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        create_roles()
