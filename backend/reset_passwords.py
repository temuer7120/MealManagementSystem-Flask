from app import app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    print("=" * 60)
    print("重置所有用户密码为: 123456")
    print("=" * 60)
    
    users = User.query.all()
    count = 0
    
    for user in users:
        if user.is_active:
            user.set_password("123456")
            count += 1
            print(f"✓ 已重置用户: {user.username}")
    
    try:
        db.session.commit()
        print(f"\n成功重置 {count} 个用户的密码")
        print("\n现在可以使用以下账号登录（密码都是: 123456）:")
        print("\n管理员账号:")
        print("  - admin / 123456")
        print("  - manager1 / 123456 (李经理)")
        print("  - manager2 / 123456 (王经理)")
        
        print("\n营养师账号:")
        print("  - nutritionist / 123456")
        print("  - nutritionist1 / 123456 (张营养师)")
        print("  - nutritionist2 / 123456 (刘营养师)")
        
        print("\n厨师账号:")
        print("  - chef / 123456")
        print("  - chef1 / 123456 (陈厨师长)")
        print("  - chef2 / 123456 (林厨师)")
        print("  - chef3 / 123456 (黄厨师)")
        
        print("\n护士账号:")
        print("  - nurse1 ~ nurse10 / 123456")
        print("  - nurse_zhang1 / 123456 (张护士1)")
        print("  - nurse_zhang2 / 123456 (张护士2)")
        
        print("\n其他账号:")
        print("  - user / 123456")
        print("  - guest / 123456")
        
    except Exception as e:
        db.session.rollback()
        print(f"错误: {e}")
    
    print("=" * 60)
