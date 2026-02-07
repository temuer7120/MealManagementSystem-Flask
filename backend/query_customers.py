from app import app
from extensions import db
from models import Customer, CustomerOrder, ServiceBooking, CustomerMenuSelection

def query_customers():
    with app.app_context():
        # 查询张女士、李女士、王女士
        customer_names = ['张女士', '李女士', '王女士']
        customers = Customer.query.filter(Customer.name.in_(customer_names)).all()
        
        if not customers:
            print('未找到张女士、李女士、王女士的客户记录')
            return
        
        print(f'找到 {len(customers)} 条客户记录：')
        for customer in customers:
            print(f'\n客户信息：')
            print(f'  ID: {customer.id}')
            print(f'  姓名: {customer.name}')
            print(f'  邮箱: {customer.email}')
            print(f'  电话: {customer.phone}')
            print(f'  身份证号: {customer.id_card_number}')
            print(f'  入住日期: {customer.check_in_date}')
            print(f'  退房日期: {customer.check_out_date}')
            print(f'  状态: {customer.status}')
            
            # 查询相关订单
            orders = CustomerOrder.query.filter_by(customer_id=customer.id).all()
            if orders:
                print(f'  关联订单 ({len(orders)} 条):')
                for order in orders:
                    print(f'    - 订单号: {order.order_number}, 日期: {order.order_date}, 状态: {order.order_status}')
            
            # 查询相关服务预订
            bookings = ServiceBooking.query.filter_by(customer_id=customer.id).all()
            if bookings:
                print(f'  关联服务预订 ({len(bookings)} 条):')
                for booking in bookings:
                    print(f'    - 预订号: {booking.booking_number}, 日期: {booking.booking_date}, 状态: {booking.status}')
            
            # 查询相关菜单选择
            menu_selections = CustomerMenuSelection.query.filter_by(customer_id=customer.id).all()
            if menu_selections:
                print(f'  关联菜单选择 ({len(menu_selections)} 条):')
                for selection in menu_selections:
                    print(f'    - 日期: {selection.selection_date}, 餐次: {selection.meal_type}, 状态: {selection.status}')

if __name__ == '__main__':
    query_customers()
