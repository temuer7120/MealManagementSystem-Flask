from app import app
from extensions import db
from models import *
from datetime import datetime, timedelta
import random

print("开始填充数据...")

with app.app_context():
    try:
        # 1. 填充角色和权限数据
        print("\n1. 填充角色和权限数据...")
        
        # 检查是否已有数据
        if Role.query.count() == 0:
            # 创建权限
            permissions = [
                Permission(name='Admin', description='管理员权限'),
                Permission(name='User', description='普通用户权限'),
                Permission(name='Menu', description='菜单管理权限'),
                Permission(name='Dish', description='菜品管理权限'),
                Permission(name='Ingredient', description='食材管理权限'),
                Permission(name='Order', description='订单管理权限'),
                Permission(name='Customer', description='客户管理权限'),
                Permission(name='Employee', description='员工管理权限'),
                Permission(name='Finance', description='财务管理权限'),
                Permission(name='Report', description='报表管理权限'),
                Permission(name='Service', description='服务管理权限')
            ]
            db.session.add_all(permissions)
            db.session.commit()
            print(f"创建了 {len(permissions)} 个权限")
            
            # 创建角色
            admin_role = Role(name='管理员', description='系统管理员')
            user_role = Role(name='普通用户', description='普通系统用户')
            db.session.add_all([admin_role, user_role])
            db.session.commit()
            print("创建了 2 个角色")
            
            # 分配权限
            admin_role.permissions.extend(permissions)
            user_role.permissions.extend(permissions[:3])  # 普通用户只分配部分权限
            db.session.commit()
            print("权限分配完成")
        else:
            print("角色和权限数据已存在，跳过...")
        
        # 2. 填充用户数据
        print("\n2. 填充用户数据...")
        
        if User.query.count() == 0:
            # 创建管理员用户
            admin_user = User(
                username='admin',
                password_hash='pbkdf2:sha256:260000$qVvWtX6q5vNf4R8G$c6d4a2b8c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0',
                email='admin@example.com',
                phone='13800138000',
                is_active=True
            )
            admin_user.roles.append(Role.query.filter_by(name='管理员').first())
            
            # 创建普通用户
            normal_user = User(
                username='user',
                password_hash='pbkdf2:sha256:260000$qVvWtX6q5vNf4R8G$c6d4a2b8c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0',
                email='user@example.com',
                phone='13900139000',
                is_active=True
            )
            normal_user.roles.append(Role.query.filter_by(name='普通用户').first())
            
            db.session.add_all([admin_user, normal_user])
            db.session.commit()
            print("创建了 2 个用户")
        else:
            print("用户数据已存在，跳过...")
        
        # 3. 填充菜品分类数据
        print("\n3. 填充菜品分类数据...")
        
        if MenuCategory.query.count() == 0:
            categories = [
                MenuCategory(name='主菜', description='主要菜品', sort_order=1),
                MenuCategory(name='配菜', description='辅助菜品', sort_order=2),
                MenuCategory(name='汤品', description='各类汤品', sort_order=3),
                MenuCategory(name='点心', description='各类点心', sort_order=4),
                MenuCategory(name='水果', description='各类水果', sort_order=5),
                MenuCategory(name='饮品', description='各类饮品', sort_order=6)
            ]
            db.session.add_all(categories)
            db.session.commit()
            print(f"创建了 {len(categories)} 个菜品分类")
        else:
            print("菜品分类数据已存在，跳过...")
        
        # 4. 填充食材分类数据
        print("\n4. 填充食材分类数据...")
        
        if IngredientCategory.query.count() == 0:
            categories = [
                IngredientCategory(name='蔬菜', description='各类蔬菜'),
                IngredientCategory(name='肉类', description='各类肉类'),
                IngredientCategory(name='海鲜', description='各类海鲜'),
                IngredientCategory(name='粮油', description='各类粮油'),
                IngredientCategory(name='调料', description='各类调料'),
                IngredientCategory(name='水果', description='各类水果'),
                IngredientCategory(name='饮品', description='各类饮品')
            ]
            db.session.add_all(categories)
            db.session.commit()
            print(f"创建了 {len(categories)} 个食材分类")
        else:
            print("食材分类数据已存在，跳过...")
        
        # 5. 填充食材数据
        print("\n5. 填充食材数据...")
        
        if Ingredient.query.count() == 0:
            ingredient_categories = IngredientCategory.query.all()
            ingredients = [
                Ingredient(name='西红柿', category_id=ingredient_categories[0].id, unit_of_measure='个', unit_cost=2.5, current_stock=100, is_active=True),
                Ingredient(name='鸡蛋', category_id=ingredient_categories[1].id, unit_of_measure='个', unit_cost=1.2, current_stock=200, is_active=True),
                Ingredient(name='大米', category_id=ingredient_categories[3].id, unit_of_measure='kg', unit_cost=6.5, current_stock=50, is_active=True),
                Ingredient(name='青菜', category_id=ingredient_categories[0].id, unit_of_measure='斤', unit_cost=3.8, current_stock=80, is_active=True),
                Ingredient(name='猪肉', category_id=ingredient_categories[1].id, unit_of_measure='斤', unit_cost=28.5, current_stock=30, is_active=True),
                Ingredient(name='鸡肉', category_id=ingredient_categories[1].id, unit_of_measure='斤', unit_cost=22.0, current_stock=25, is_active=True),
                Ingredient(name='鱼', category_id=ingredient_categories[2].id, unit_of_measure='条', unit_cost=35.0, current_stock=15, is_active=True),
                Ingredient(name='胡萝卜', category_id=ingredient_categories[0].id, unit_of_measure='根', unit_cost=1.5, current_stock=60, is_active=True),
                Ingredient(name='土豆', category_id=ingredient_categories[0].id, unit_of_measure='个', unit_cost=1.8, current_stock=70, is_active=True),
                Ingredient(name='洋葱', category_id=ingredient_categories[0].id, unit_of_measure='个', unit_cost=2.0, current_stock=40, is_active=True),
                Ingredient(name='大蒜', category_id=ingredient_categories[0].id, unit_of_measure='头', unit_cost=3.0, current_stock=50, is_active=True),
                Ingredient(name='生姜', category_id=ingredient_categories[0].id, unit_of_measure='块', unit_cost=4.0, current_stock=35, is_active=True),
                Ingredient(name='盐', category_id=ingredient_categories[4].id, unit_of_measure='袋', unit_cost=2.0, current_stock=20, is_active=True),
                Ingredient(name='糖', category_id=ingredient_categories[4].id, unit_of_measure='袋', unit_cost=5.0, current_stock=15, is_active=True),
                Ingredient(name='酱油', category_id=ingredient_categories[4].id, unit_of_measure='瓶', unit_cost=12.0, current_stock=10, is_active=True),
                Ingredient(name='醋', category_id=ingredient_categories[4].id, unit_of_measure='瓶', unit_cost=8.0, current_stock=12, is_active=True),
                Ingredient(name='苹果', category_id=ingredient_categories[5].id, unit_of_measure='个', unit_cost=3.0, current_stock=60, is_active=True),
                Ingredient(name='香蕉', category_id=ingredient_categories[5].id, unit_of_measure='根', unit_cost=2.0, current_stock=80, is_active=True),
                Ingredient(name='橙子', category_id=ingredient_categories[5].id, unit_of_measure='个', unit_cost=4.0, current_stock=50, is_active=True),
                Ingredient(name='牛奶', category_id=ingredient_categories[6].id, unit_of_measure='盒', unit_cost=6.0, current_stock=30, is_active=True)
            ]
            db.session.add_all(ingredients)
            db.session.commit()
            print(f"创建了 {len(ingredients)} 个食材")
        else:
            print("食材数据已存在，跳过...")
        
        # 6. 填充菜品数据
        print("\n6. 填充菜品数据...")
        
        if Dish.query.count() == 0:
            menu_categories = MenuCategory.query.all()
            dishes = [
                Dish(name='清蒸鱼', description='新鲜鱼肉清蒸，保持原味', category_id=menu_categories[0].id, price=88.0, is_available=True),
                Dish(name='红烧肉', description='传统红烧肉，肥而不腻', category_id=menu_categories[0].id, price=68.0, is_available=True),
                Dish(name='糖醋排骨', description='酸甜可口，老少皆宜', category_id=menu_categories[0].id, price=58.0, is_available=True),
                Dish(name='宫保鸡丁', description='经典川菜，香辣可口', category_id=menu_categories[0].id, price=48.0, is_available=True),
                Dish(name='鱼香肉丝', description='传统川菜，口味独特', category_id=menu_categories[0].id, price=42.0, is_available=True),
                Dish(name='清炒时蔬', description='新鲜蔬菜清炒', category_id=menu_categories[1].id, price=28.0, is_available=True),
                Dish(name='蒜蓉西兰花', description='蒜蓉搭配西兰花', category_id=menu_categories[1].id, price=32.0, is_available=True),
                Dish(name='西红柿炒蛋', description='经典家常菜', category_id=menu_categories[1].id, price=35.0, is_available=True),
                Dish(name='酸辣土豆丝', description='爽口开胃', category_id=menu_categories[1].id, price=26.0, is_available=True),
                Dish(name='鸡汤', description='新鲜鸡肉熬制', category_id=menu_categories[2].id, price=58.0, is_available=True),
                Dish(name='排骨汤', description='猪排骨熬制', category_id=menu_categories[2].id, price=48.0, is_available=True),
                Dish(name='西红柿鸡蛋汤', description='经典汤品', category_id=menu_categories[2].id, price=28.0, is_available=True),
                Dish(name='紫菜蛋花汤', description='清爽可口', category_id=menu_categories[2].id, price=26.0, is_available=True),
                Dish(name='小米粥', description='营养健康', category_id=menu_categories[3].id, price=15.0, is_available=True),
                Dish(name='馒头', description='传统面食', category_id=menu_categories[3].id, price=5.0, is_available=True),
                Dish(name='花卷', description='传统面食', category_id=menu_categories[3].id, price=6.0, is_available=True),
                Dish(name='包子', description='肉馅包子', category_id=menu_categories[3].id, price=8.0, is_available=True),
                Dish(name='苹果', description='新鲜苹果', category_id=menu_categories[4].id, price=12.0, is_available=True),
                Dish(name='香蕉', description='新鲜香蕉', category_id=menu_categories[4].id, price=10.0, is_available=True),
                Dish(name='橙子', description='新鲜橙子', category_id=menu_categories[4].id, price=15.0, is_available=True),
                Dish(name='牛奶', description='新鲜牛奶', category_id=menu_categories[5].id, price=18.0, is_available=True),
                Dish(name='果汁', description='新鲜果汁', category_id=menu_categories[5].id, price=25.0, is_available=True),
                Dish(name='茶', description='清香茶水', category_id=menu_categories[5].id, price=10.0, is_available=True)
            ]
            db.session.add_all(dishes)
            db.session.commit()
            print(f"创建了 {len(dishes)} 个菜品")
        else:
            print("菜品数据已存在，跳过...")
        
        # 7. 填充服务分类和服务项目数据
        print("\n7. 填充服务分类和服务项目数据...")
        
        if ServiceCategory.query.count() == 0:
            # 创建服务分类
            service_categories = [
                ServiceCategory(name='产后护理', description='产后妈妈护理', sort_order=1),
                ServiceCategory(name='新生儿护理', description='新生儿护理', sort_order=2),
                ServiceCategory(name='营养咨询', description='营养咨询服务', sort_order=3),
                ServiceCategory(name='家政服务', description='家政服务', sort_order=4)
            ]
            db.session.add_all(service_categories)
            db.session.commit()
            print(f"创建了 {len(service_categories)} 个服务分类")
            
            # 创建服务项目
            service_items = [
                ServiceItem(name='产后护理', description='专业产后护理服务', category_id=service_categories[0].id, price=500.0, duration_minutes=120, is_available=True),
                ServiceItem(name='新生儿护理', description='专业新生儿护理服务', category_id=service_categories[1].id, price=400.0, duration_minutes=90, is_available=True),
                ServiceItem(name='营养咨询', description='专业营养咨询服务', category_id=service_categories[2].id, price=300.0, duration_minutes=60, is_available=True),
                ServiceItem(name='家政服务', description='专业家政服务', category_id=service_categories[3].id, price=200.0, duration_minutes=180, is_available=True)
            ]
            db.session.add_all(service_items)
            db.session.commit()
            print(f"创建了 {len(service_items)} 个服务项目")
        else:
            print("服务数据已存在，跳过...")
        
        # 8. 填充客户数据
        print("\n8. 填充客户数据...")
        
        if Customer.query.count() == 0:
            customers = [
                Customer(name='张女士', phone='13812345678', email='zhang@example.com', status='active'),
                Customer(name='李女士', phone='13912345678', email='li@example.com', status='active'),
                Customer(name='王女士', phone='13712345678', email='wang@example.com', status='active'),
                Customer(name='刘女士', phone='13612345678', email='liu@example.com', status='active'),
                Customer(name='陈女士', phone='13512345678', email='chen@example.com', status='active')
            ]
            db.session.add_all(customers)
            db.session.commit()
            print(f"创建了 {len(customers)} 个客户")
        else:
            print("客户数据已存在，跳过...")
        
        # 9. 填充服务预定数据
        print("\n9. 填充服务预定数据...")
        
        if ServiceBooking.query.count() == 0:
            customers = Customer.query.all()
            service_items = ServiceItem.query.all()
            
            bookings = []
            for i in range(10):
                customer = random.choice(customers)
                service_item = random.choice(service_items)
                booking_date = datetime.now() + timedelta(days=random.randint(1, 30))
                
                booking = ServiceBooking(
                    booking_number=f'BOOK{i+1:04d}',
                    customer_id=customer.id,
                    service_item_id=service_item.id,
                    booking_date=booking_date.date(),
                    duration_minutes=service_item.duration_minutes,
                    status=random.choice(['pending', 'confirmed', 'completed', 'cancelled'])
                )
                bookings.append(booking)
            
            db.session.add_all(bookings)
            db.session.commit()
            print(f"创建了 {len(bookings)} 个服务预定")
        else:
            print("服务预定数据已存在，跳过...")
        
        # 10. 填充订单数据
        print("\n10. 填充订单数据...")
        
        if CustomerOrder.query.count() == 0:
            customers = Customer.query.all()
            dishes = Dish.query.all()
            
            orders = []
            for i in range(15):
                customer = random.choice(customers)
                order_date = datetime.now() - timedelta(days=random.randint(1, 60))
                total_amount = 0
                order_items = []
                
                # 为每个订单添加1-3个菜品
                for j in range(random.randint(1, 3)):
                    dish = random.choice(dishes)
                    quantity = random.randint(1, 2)
                    item_amount = dish.price * quantity
                    total_amount += item_amount
                    
                    order_item = OrderItem(
                        dish_id=dish.id,
                        quantity=quantity,
                        unit_price=dish.price,
                        total_price=item_amount
                    )
                    order_items.append(order_item)
                
                order = CustomerOrder(
                    order_number=f'ORDER{i+1:04d}',
                    customer_id=customer.id,
                    order_date=order_date,
                    total_amount=total_amount,
                    payment_status=random.choice(['pending', 'paid', 'completed', 'cancelled']),
                    order_status=random.choice(['pending', 'processing', 'delivered', 'cancelled']),
                    payment_method=random.choice(['微信支付', '支付宝', '现金'])
                )
                order.order_items = order_items
                orders.append(order)
            
            db.session.add_all(orders)
            db.session.commit()
            print(f"创建了 {len(orders)} 个订单")
        else:
            print("订单数据已存在，跳过...")
        
        # 11. 填充财务管理数据
        print("\n11. 填充财务管理数据...")
        
        # 注意：Finance模型未在models.py中定义，暂时跳过
        print("Finance模型未定义，跳过财务数据填充...")
        
        # 12. 填充员工数据
        print("\n12. 填充员工数据...")
        
        # 注意：Employee模型未在models.py中定义，暂时跳過
        print("Employee模型未定义，跳过员工数据填充...")
        
        print("\n数据填充完成！")
        print("系统现在可以使用真实数据了。")
        
    except Exception as e:
        print(f"数据填充错误: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
