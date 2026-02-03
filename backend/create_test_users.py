from app import app
from extensions import db
from models import User

def create_test_users():
    with app.app_context():
        # 检查用户是否已存在
        existing_users = User.query.all()
        existing_usernames = [user.username for user in existing_users]
        
        # 创建管理员用户
        if 'admin' not in existing_usernames:
            admin = User(username='admin')
            admin.set_password('admin123')
            admin.role = 'admin'
            db.session.add(admin)
            print('创建管理员用户: admin / admin123')
        else:
            print('管理员用户已存在')
        
        # 创建营养师用户
        if 'nutr' not in existing_usernames:
            nutritionist = User(username='nutr')
            nutritionist.set_password('nutr123')
            nutritionist.role = 'nutritionist'
            db.session.add(nutritionist)
            print('创建营养师用户: nutr / nutr')
        else:
            print('营养师用户已存在')
        
        # 创建普通用户
        if 'user' not in existing_usernames:
            normal_user = User(username='user')
            normal_user.set_password('user123')
            normal_user.role = 'user'
            db.session.add(normal_user)
            print('创建普通用户: user / user123')
        else:
            print('普通用户已存在')
        
        # 创建访客用户
        if 'guest' not in existing_usernames:
            guest = User(username='guest')
            guest.set_password('guest123')
            guest.role = 'guest'
            db.session.add(guest)
            print('创建访客用户: guest / guest123')
        else:
            print('访客用户已存在')
        
        # 创建厨师用户
        if 'chef' not in existing_usernames:
            chef = User(username='chef')
            chef.set_password('chef123')
            chef.role = 'chef'
            db.session.add(chef)
            print('创建厨师用户: chef / chef123')
        else:
            print('厨师用户已存在')
        
        # 提交更改
        db.session.commit()
        print('\n所有测试用户创建完成！')
        print('\n用户列表：')
        users = User.query.all()
        for user in users:
            print(f'  - {user.username} ({user.role})')

if __name__ == '__main__':
    create_test_users()
