from app import app
from extensions import db
from models import Customer

def check_all_customers():
    with app.app_context():
        # 查询所有客户
        customers = Customer.query.all()
        
        if not customers:
            print('数据库中没有任何客户记录')
        else:
            print(f'数据库中共有 {len(customers)} 条客户记录：')
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

if __name__ == '__main__':
    check_all_customers()
