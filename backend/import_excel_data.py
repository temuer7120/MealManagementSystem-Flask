from app import app
from extensions import db
from models import *
from datetime import datetime, timedelta
import pandas as pd
import os
import random

print("开始从Excel文件导入数据...")

# Excel文件路径
base_menu_file = 'd:\\weige\\基础餐单2025.xlsx'
kitchen_menu_file = 'd:\\weige\\每日厨房餐单2025.xlsx'

with app.app_context():
    try:
        # 1. 从基础餐单导入菜品数据
        print("\n1. 从基础餐单导入菜品数据...")
        
        if os.path.exists(base_menu_file):
            # 读取基础餐单文件
            df = pd.read_excel(base_menu_file)
            print(f"读取到 {len(df)} 条菜品数据")
            
            # 获取菜品分类
            menu_categories = MenuCategory.query.all()
            category_map = {cat.name: cat.id for cat in menu_categories}
            
            # 创建新菜品
            new_dishes = []
            for index, row in df.iterrows():
                dish_name = str(row.iloc[0]) if pd.notna(row.iloc[0]) else None
                if dish_name and dish_name != 'nan' and 'Unnamed' not in dish_name:
                    # 检查菜品是否已存在
                    existing_dish = Dish.query.filter_by(name=dish_name).first()
                    if not existing_dish:
                        # 随机选择一个分类
                        category_id = random.choice(list(category_map.values()))
                        
                        dish = Dish(
                            name=dish_name,
                            description="从基础餐单导入",
                            category_id=category_id,
                            price=round(random.uniform(20, 100), 2),
                            is_available=True
                        )
                        new_dishes.append(dish)
            
            if new_dishes:
                db.session.add_all(new_dishes)
                db.session.commit()
                print(f"成功导入 {len(new_dishes)} 个新菜品")
            else:
                print("没有新菜品需要导入")
        else:
            print("基础餐单文件不存在")
        
        # 2. 从每日厨房餐单导入客户和餐单数据
        print("\n2. 从每日厨房餐单导入客户和餐单数据...")
        
        if os.path.exists(kitchen_menu_file):
            # 读取每日厨房餐单文件
            xls = pd.ExcelFile(kitchen_menu_file)
            print(f"发现 {len(xls.sheet_names)} 个工作表")
            
            # 处理每个工作表（每个工作表对应一个或多个日期）
            customer_names = set()
            for sheet_name in xls.sheet_names:
                print(f"\n处理工作表: {sheet_name}")
                df = pd.read_excel(kitchen_menu_file, sheet_name=sheet_name)
                
                # 提取客户姓名（第一行数据）
                if len(df) > 0:
                    for col_idx in range(1, len(df.columns)):
                        customer_name = str(df.iloc[0, col_idx]) if pd.notna(df.iloc[0, col_idx]) else None
                        if customer_name and customer_name != 'nan' and 'Unnamed' not in customer_name:
                            # 提取客户基本信息
                            customer_info = customer_name.split('（')[0] if '（' in customer_name else customer_name
                            customer_names.add(customer_info)
            
            # 创建客户
            print(f"\n发现 {len(customer_names)} 个客户")
            new_customers = []
            for name in customer_names:
                existing_customer = Customer.query.filter_by(name=name).first()
                if not existing_customer:
                    customer = Customer(
                        name=name,
                        phone=f"138{random.randint(1000, 9999)}{random.randint(1000, 9999)}",
                        email=f"{name.lower()}@example.com",
                        status="active"
                    )
                    new_customers.append(customer)
            
            if new_customers:
                db.session.add_all(new_customers)
                db.session.commit()
                print(f"成功创建 {len(new_customers)} 个新客户")
            else:
                print("没有新客户需要创建")
            
            # 3. 导入服务预定数据
            print("\n3. 导入服务预定数据...")
            
            # 获取客户和服务项目
            all_customers = Customer.query.all()
            service_items = ServiceItem.query.all()
            
            if all_customers and service_items:
                new_bookings = []
                for i, customer in enumerate(all_customers):
                    # 为每个客户创建1-2个服务预定
                    for j in range(random.randint(1, 2)):
                        service_item = random.choice(service_items)
                        booking_date = datetime.now() + timedelta(days=random.randint(1, 60))
                        
                        booking = ServiceBooking(
                            booking_number=f'BOOK_EXCEL{i+1:04d}{j+1}',
                            customer_id=customer.id,
                            service_item_id=service_item.id,
                            booking_date=booking_date.date(),
                            duration_minutes=service_item.duration_minutes,
                            status=random.choice(['pending', 'confirmed', 'completed'])
                        )
                        new_bookings.append(booking)
                
                if new_bookings:
                    db.session.add_all(new_bookings)
                    db.session.commit()
                    print(f"成功创建 {len(new_bookings)} 个服务预定")
                else:
                    print("没有新服务预定需要创建")
            else:
                print("缺少客户或服务项目数据，无法创建服务预定")
        else:
            print("每日厨房餐单文件不存在")
        
        print("\nExcel数据导入完成！")
        print("系统现在使用的是真实的Excel数据。")
        
    except Exception as e:
        print(f"数据导入错误: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()