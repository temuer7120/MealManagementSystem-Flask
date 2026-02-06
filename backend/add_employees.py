#!/usr/bin/env python3
"""
添加20名符合权限要求的员工
"""

from extensions import db
from models import User, Role, UserRole
from datetime import datetime
import random

def add_employees():
    """添加20名符合权限要求的员工"""
    print("开始添加员工...")
    
    # 获取角色
    admin_role = Role.query.filter_by(name='admin').first() or Role.query.filter_by(name='admin_staff').first()
    nutritionist_role = Role.query.filter_by(name='nutritionist').first() or Role.query.filter_by(name='nutr').first()
    chef_role = Role.query.filter_by(name='chef').first()
    nurse_role = Role.query.filter_by(name='nurse').first()
    caregiver_role = Role.query.filter_by(name='caregiver').first()
    
    if not all([admin_role, nutritionist_role, chef_role, nurse_role, caregiver_role]):
        print("错误：缺少必要的角色")
        return
    
    # 员工数据
    employees = []
    
    # 1. 管理人员 2名
    employees.extend([
        {"username": "manager1", "full_name": "李经理", "department": "管理部", "position": "总经理", "role": admin_role},
        {"username": "manager2", "full_name": "王经理", "department": "管理部", "position": "副总经理", "role": admin_role}
    ])
    
    # 2. 营养师 2名
    employees.extend([
        {"username": "nutritionist1", "full_name": "张营养师", "department": "营养部", "position": "高级营养师", "role": nutritionist_role},
        {"username": "nutritionist2", "full_name": "刘营养师", "department": "营养部", "position": "营养师", "role": nutritionist_role}
    ])
    
    # 3. 厨师 3名
    employees.extend([
        {"username": "chef1", "full_name": "陈厨师长", "department": "厨房", "position": "厨师长", "role": chef_role},
        {"username": "chef2", "full_name": "林厨师", "department": "厨房", "position": "主厨", "role": chef_role},
        {"username": "chef3", "full_name": "黄厨师", "department": "厨房", "position": "副主厨", "role": chef_role}
    ])
    
    # 4. 护士 10名
    nurse_names = ["赵护士", "钱护士", "孙护士", "李护士", "周护士", "吴护士", "郑护士", "王护士", "冯护士", "陈护士"]
    for i, name in enumerate(nurse_names, 1):
        employees.append({
            "username": f"nurse{i}",
            "full_name": name,
            "department": "护理部",
            "position": "护士",
            "role": nurse_role
        })
    
    # 5. 护士张 2名
    employees.extend([
        {"username": "nurse_zhang1", "full_name": "张护士1", "department": "护理部", "position": "护士", "role": nurse_role},
        {"username": "nurse_zhang2", "full_name": "张护士2", "department": "护理部", "position": "护士", "role": nurse_role}
    ])
    
    # 6. 其他人员 1名
    employees.append({
        "username": "caregiver1",
        "full_name": "照顾员",
        "department": "护理部",
        "position": "护理员",
        "role": caregiver_role
    })
    
    # 验证数量
    print(f"准备添加 {len(employees)} 名员工")
    
    # 添加员工
    added_count = 0
    for emp in employees:
        # 检查是否已存在
        existing = User.query.filter_by(username=emp["username"]).first()
        if existing:
            print(f"员工 {emp['username']} 已存在，跳过")
            continue
        
        # 创建用户
        user = User(
            username=emp["username"],
            full_name=emp["full_name"],
            department=emp["department"],
            position=emp["position"],
            email=f"{emp['username']}@example.com",
            phone=f"138{random.randint(1000, 9999)}{random.randint(1000, 9999)}",
            is_active=True
        )
        
        # 设置密码
        user.set_password("123456")
        
        # 添加到数据库
        db.session.add(user)
        db.session.flush()  # 获取用户ID
        
        # 分配角色
        user_role = UserRole(
            user_id=user.id,
            role_id=emp["role"].id
        )
        db.session.add(user_role)
        
        added_count += 1
        print(f"添加员工：{emp['full_name']} ({emp['username']}) - {emp['role'].name}")
    
    # 提交事务
    try:
        db.session.commit()
        print(f"\n成功添加 {added_count} 名员工")
    except Exception as e:
        db.session.rollback()
        print(f"\n错误：{e}")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        add_employees()
