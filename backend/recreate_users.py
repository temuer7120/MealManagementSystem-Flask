from app import app
from extensions import db
from models import User

def recreate_users():
    with app.app_context():
        # 删除所有现有用户
        users_to_delete = ['admin_staff', 'head_nurse', 'nurse', 'caregiver']
        for username in users_to_delete:
            user = User.query.filter_by(username=username).first()
            if user:
                db.session.delete(user)
                print(f'删除用户: {username}')
        
        # 创建行政用户
        admin_staff = User(username='admin_staff')
        admin_staff.set_password('admin')
        admin_staff.role = 'admin_staff'
        db.session.add(admin_staff)
        print('创建行政用户: admin_staff / admin')
        
        # 创建护士长用户
        head_nurse = User(username='head_nurse')
        head_nurse.set_password('nurse')
        head_nurse.role = 'head_nurse'
        db.session.add(head_nurse)
        print('创建护士长用户: head_nurse / nurse')
        
        # 创建护士用户
        nurse = User(username='nurse')
        nurse.set_password('nurse')
        nurse.role = 'nurse'
        db.session.add(nurse)
        print('创建护士用户: nurse / nurse')
        
        # 创建陪护用户
        caregiver = User(username='caregiver')
        caregiver.set_password('care')
        caregiver.role = 'caregiver'
        db.session.add(caregiver)
        print('创建陪护用户: caregiver / care')
        
        # 提交更改
        db.session.commit()
        print('\n用户重新创建完成！')
        
        # 显示当前用户列表
        print('\n当前用户列表：')
        users = User.query.all()
        for user in users:
            print(f'  - {user.username} ({user.role})')

if __name__ == '__main__':
    recreate_users()
