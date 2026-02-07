from app import app, db
from models import CustomerOrder, Customer

with app.app_context():
    # 检查客户数据
    print('客户数量:', Customer.query.count())
    print('客户详情:')
    for customer in Customer.query.all():
        print(f'ID: {customer.id}, 姓名: {customer.name}, 电话: {customer.phone}')
    
    # 检查订单数据
    print('\n订单数量:', CustomerOrder.query.count())
    print('订单详情:')
    for order in CustomerOrder.query.all():
        customer_name = order.customer.name if order.customer else '未知客户'
        print(f'ID: {order.id}, 客户: {customer_name}, 日期: {order.order_date}, 状态: {order.status}, 金额: {order.total_amount}')
