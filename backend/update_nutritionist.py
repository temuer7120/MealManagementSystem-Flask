from app import app
from extensions import db
from models import User

def update_nutritionist_user():
    with app.app_context():
        # 删除旧的nutr用户（如果存在）
        old_nutr = User.query.filter_by(username='nutr').first()
        if old_nutr:
            db.session.delete(old_nutr)
            print('删除旧的营养师用户: nutr')
        
        # 检查新用户是否已存在
        new_nutritionist = User.query.filter_by(username='nutr').first()
        if not new_nutritionist:
            nutritionist = User(username='nutr')
            nutritionist.set_password('nutr123')
            nutritionist.role = 'nutritionist'
            db.session.add(nutritionist)
            print('创建新的营养师用户: nutr / nutr123')
        else:
            print('营养师用户 nutr 已存在')
        
        # 检查客户用户是否已存在
        customer_user = User.query.filter_by(username='cust').first()
        if not customer_user:
            customer = User(username='cust')
            customer.set_password('cust123')
            customer.role = 'customer'
            db.session.add(customer)
            print('创建客户用户: cust / cust123')
        else:
            print('客户用户 cust 已存在')
        
        # 提交更改
        db.session.commit()
        print('\n用户更新完成！')
        
        # 显示当前用户列表
        print('\n当前用户列表：')
        users = User.query.all()
        for user in users:
            print(f'  - {user.username} ({user.role})')

if __name__ == '__main__':
    update_nutritionist_user()
