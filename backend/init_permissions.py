from extensions import db
from models import Permission, Role, RolePermission

# 权限数据
permissions = [
    # 系统管理
    {"name": "系统管理", "code": "system_manage", "module": "system", "description": "系统管理权限"},
    
    # 用户管理
    {"name": "用户管理", "code": "user_manage", "module": "user", "description": "用户管理权限"},
    {"name": "创建用户", "code": "user_create", "module": "user", "description": "创建用户权限"},
    {"name": "修改用户", "code": "user_update", "module": "user", "description": "修改用户权限"},
    {"name": "删除用户", "code": "user_delete", "module": "user", "description": "删除用户权限"},
    
    # 食材管理
    {"name": "食材管理", "code": "ingredient_manage", "module": "ingredient", "description": "食材管理权限"},
    {"name": "创建食材", "code": "ingredient_create", "module": "ingredient", "description": "创建食材权限"},
    {"name": "修改食材", "code": "ingredient_update", "module": "ingredient", "description": "修改食材权限"},
    {"name": "删除食材", "code": "ingredient_delete", "module": "ingredient", "description": "删除食材权限"},
    
    # 菜品管理
    {"name": "菜品管理", "code": "dish_manage", "module": "dish", "description": "菜品管理权限"},
    {"name": "创建菜品", "code": "dish_create", "module": "dish", "description": "创建菜品权限"},
    {"name": "修改菜品", "code": "dish_update", "module": "dish", "description": "修改菜品权限"},
    {"name": "删除菜品", "code": "dish_delete", "module": "dish", "description": "删除菜品权限"},
    
    # 菜单管理
    {"name": "菜单管理", "code": "menu_manage", "module": "menu", "description": "菜单管理权限"},
    {"name": "创建菜单", "code": "menu_create", "module": "menu", "description": "创建菜单权限"},
    {"name": "修改菜单", "code": "menu_update", "module": "menu", "description": "修改菜单权限"},
    {"name": "删除菜单", "code": "menu_delete", "module": "menu", "description": "删除菜单权限"},
    
    # 客户管理
    {"name": "客户管理", "code": "customer_manage", "module": "customer", "description": "客户管理权限"},
    {"name": "创建客户", "code": "customer_create", "module": "customer", "description": "创建客户权限"},
    {"name": "修改客户", "code": "customer_update", "module": "customer", "description": "修改客户权限"},
    {"name": "删除客户", "code": "customer_delete", "module": "customer", "description": "删除客户权限"},
    
    # 订单管理
    {"name": "订单管理", "code": "order_manage", "module": "order", "description": "订单管理权限"},
    {"name": "创建订单", "code": "order_create", "module": "order", "description": "创建订单权限"},
    {"name": "修改订单", "code": "order_update", "module": "order", "description": "修改订单权限"},
    {"name": "删除订单", "code": "order_delete", "module": "order", "description": "删除订单权限"},
    
    # 排餐管理
    {"name": "排餐管理", "code": "meal_schedule_manage", "module": "meal_schedule", "description": "排餐管理权限"},
    {"name": "创建排餐", "code": "meal_schedule_create", "module": "meal_schedule", "description": "创建排餐权限"},
    {"name": "修改排餐", "code": "meal_schedule_update", "module": "meal_schedule", "description": "修改排餐权限"},
    {"name": "删除排餐", "code": "meal_schedule_delete", "module": "meal_schedule", "description": "删除排餐权限"},
    
    # 报表中心
    {"name": "报表中心", "code": "report_view", "module": "report", "description": "查看报表权限"},
    
    # 个人中心
    {"name": "个人中心", "code": "profile_view", "module": "profile", "description": "个人中心权限"},
    {"name": "修改个人信息", "code": "profile_update", "module": "profile", "description": "修改个人信息权限"},
    {"name": "修改密码", "code": "password_change", "module": "profile", "description": "修改密码权限"},
    
    # 上传Excel
    {"name": "上传Excel", "code": "excel_upload", "module": "data_import", "description": "上传Excel权限"}
]

# 角色权限映射
role_permissions_map = {
    "admin": [p["code"] for p in permissions],  # admin拥有所有权限
    
    "nutritionist": [
        "ingredient_manage", "ingredient_create", "ingredient_update", "ingredient_delete",
        "dish_manage", "dish_create", "dish_update", "dish_delete",
        "menu_manage", "menu_create", "menu_update", "menu_delete",
        "customer_manage", "customer_update",
        "meal_schedule_manage", "meal_schedule_create", "meal_schedule_update", "meal_schedule_delete",
        "report_view",
        "profile_view", "profile_update", "password_change",
        "excel_upload"
    ],
    
    "chef": [
        "ingredient_manage", "ingredient_create", "ingredient_update", "ingredient_delete",
        "dish_manage", "dish_create", "dish_update", "dish_delete",
        "menu_manage", "menu_create", "menu_update", "menu_delete",
        "meal_schedule_manage", "meal_schedule_create", "meal_schedule_update", "meal_schedule_delete",
        "report_view",
        "profile_view", "profile_update", "password_change",
        "excel_upload"
    ],
    
    "nurse": [
        "customer_manage", "customer_create", "customer_update",
        "meal_schedule_manage", "meal_schedule_create", "meal_schedule_update", "meal_schedule_delete",
        "report_view",
        "profile_view", "profile_update", "password_change"
    ],
    
    "caregiver": [
        "customer_manage", "customer_create", "customer_update",
        "meal_schedule_manage", "meal_schedule_create", "meal_schedule_update", "meal_schedule_delete",
        "report_view",
        "profile_view", "profile_update", "password_change"
    ]
}

def init_permissions():
    """初始化权限数据"""
    print("开始初始化权限数据...")
    
    # 创建权限
    for perm_data in permissions:
        existing = Permission.query.filter_by(code=perm_data["code"]).first()
        if existing:
            print(f"权限 {perm_data['name']} 已存在，跳过")
            continue
        
        perm = Permission(
            name=perm_data["name"],
            code=perm_data["code"],
            module=perm_data["module"],
            description=perm_data["description"]
        )
        db.session.add(perm)
        print(f"创建权限 {perm_data['name']} 成功")
    
    db.session.commit()
    print("权限创建完成！")
    
    # 分配权限给角色
    print("\n开始分配权限给角色...")
    for role_name, perm_codes in role_permissions_map.items():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            print(f"角色 {role_name} 不存在，跳过")
            continue
        
        # 获取权限对象
        perms = Permission.query.filter(Permission.code.in_(perm_codes)).all()
        
        # 删除角色现有权限
        RolePermission.query.filter_by(role_id=role.id).delete()
        
        # 添加新权限
        for perm in perms:
            role_perm = RolePermission(role_id=role.id, permission_id=perm.id)
            db.session.add(role_perm)
        
        print(f"为角色 {role_name} 分配 {len(perms)} 个权限")
    
    db.session.commit()
    print("权限分配完成！")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        init_permissions()
