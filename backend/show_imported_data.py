from app import app
from extensions import db
from models import *

print("展示已录入的真实数据...")
print("=" * 80)

with app.app_context():
    try:
        # 1. 展示菜品数据
        print("\n1. 菜品数据:")
        print("-" * 60)
        
        dishes = Dish.query.all()
        print(f"总共有 {len(dishes)} 个菜品")
        print("\n最近导入的菜品:")
        
        # 按创建时间排序，显示最近的10个菜品
        recent_dishes = Dish.query.order_by(Dish.created_at.desc()).limit(10).all()
        for i, dish in enumerate(recent_dishes, 1):
            category = MenuCategory.query.get(dish.category_id)
            category_name = category.name if category else "未知"
            print(f"{i}. {dish.name} (分类: {category_name}, 价格: ¥{dish.price}, 状态: {'可用' if dish.is_available else '不可用'})")
        
        # 2. 展示客户数据
        print("\n2. 客户数据:")
        print("-" * 60)
        
        customers = Customer.query.all()
        print(f"总共有 {len(customers)} 个客户")
        print("\n所有客户:")
        
        for i, customer in enumerate(customers, 1):
            print(f"{i}. {customer.name} (电话: {customer.phone}, 邮箱: {customer.email}, 状态: {customer.status})")
        
        # 3. 展示服务预定数据
        print("\n3. 服务预定数据:")
        print("-" * 60)
        
        bookings = ServiceBooking.query.all()
        print(f"总共有 {len(bookings)} 个服务预定")
        print("\n最近的服务预定:")
        
        # 按创建时间排序，显示最近的10个服务预定
        recent_bookings = ServiceBooking.query.order_by(ServiceBooking.created_at.desc()).limit(10).all()
        for i, booking in enumerate(recent_bookings, 1):
            customer = Customer.query.get(booking.customer_id)
            customer_name = customer.name if customer else "未知"
            
            service_item = ServiceItem.query.get(booking.service_item_id)
            service_name = service_item.name if service_item else "未知"
            
            print(f"{i}. 编号: {booking.booking_number}")
            print(f"   客户: {customer_name}")
            print(f"   服务: {service_name}")
            print(f"   日期: {booking.booking_date}")
            print(f"   时长: {booking.duration_minutes} 分钟")
            print(f"   状态: {booking.status}")
            print()
        
        # 4. 展示订单数据
        print("\n4. 订单数据:")
        print("-" * 60)
        
        orders = CustomerOrder.query.all()
        print(f"总共有 {len(orders)} 个订单")
        if orders:
            print("\n最近的订单:")
            
            # 按创建时间排序，显示最近的5个订单
            recent_orders = CustomerOrder.query.order_by(CustomerOrder.created_at.desc()).limit(5).all()
            for i, order in enumerate(recent_orders, 1):
                customer = Customer.query.get(order.customer_id)
                customer_name = customer.name if customer else "未知"
                
                print(f"{i}. 编号: {order.order_number}")
                print(f"   客户: {customer_name}")
                print(f"   日期: {order.order_date}")
                print(f"   金额: ¥{order.total_amount}")
                print(f"   支付状态: {order.payment_status}")
                print(f"   订单状态: {order.order_status}")
                print()
        
        print("=" * 80)
        print("数据展示完成！")
        
    except Exception as e:
        print(f"查询数据错误: {str(e)}")
        import traceback
        traceback.print_exc()