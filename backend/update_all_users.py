from app import app
from extensions import db
from models import User

def update_all_users():
    with app.app_context():
        # 更新或创建行政用户
        admin_staff = User.query.filter_by(username='admin_staff').first()
        if admin_staff:
            admin_staff.set_password('admin')
            admin_staff.role = 'admin_staff'
            print('更新行政用户密码: admin_staff / admin')
        else:
            admin_staff = User(username='admin_staff')
            admin_staff.set_password('admin')
            admin_staff.role = 'admin_staff'
            db.session.add(admin_staff)
            print('创建行政用户: admin_staff / admin')
        
        # 更新或创建护士长用户
        head_nurse = User.query.filter_by(username='head_nurse').first()
        if head_nurse:
            head_nurse.set_password('nurse')
            head_nurse.role = 'head_nurse'
            print('更新护士长用户密码: head_nurse / nurse')
        else:
            head_nurse = User(username='head_nurse')
            head_nurse.set_password('nurse')
            head_nurse.role = 'head_nurse'
            db.session.add(head_nurse)
            print('创建护士长用户: head_nurse / nurse')
        
        # 更新或创建护士用户
        nurse = User.query.filter_by(username='nurse').first()
        if nurse:
            nurse.set_password('nurse')
            nurse.role = 'nurse'
            print('更新护士用户密码: nurse / nurse')
        else:
            nurse = User(username='nurse')
            nurse.set_password('nurse')
            nurse.role = 'nurse'
            db.session.add(nurse)
            print('创建护士用户: nurse / nurse')
        
        # 更新或创建陪护用户
        caregiver = User.query.filter_by(username='caregiver').first()
        if caregiver:
            caregiver.set_password('care')
            caregiver.role = 'caregiver'
            print('更新陪护用户密码: caregiver / care')
        else:
            caregiver = User(username='caregiver')
            caregiver.set_password('care')
            caregiver.role = 'caregiver'
            db.session.add(caregiver)
            print('创建陪护用户: caregiver / care')
        
        # 提交更改
        db.session.commit()
        print('\n用户更新完成！')
        
        # 显示当前用户列表
        print('\n当前用户列表：')
        users = User.query.all()
        for user in users:
            print(f'  - {user.username} ({user.role})')

if __name__ == '__main__':
    update_all_users()
