import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 从配置文件获取数据库连接字符串
from config import SQLALCHEMY_DATABASE_URI

def test_db_connection():
    """测试数据库连接"""
    print("开始测试数据库连接...")
    print(f"数据库连接字符串: {SQLALCHEMY_DATABASE_URI}")
    
    try:
        # 创建数据库引擎
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        
        # 测试连接
        with engine.connect() as connection:
            print("✅ 数据库连接成功！")
            
            # 测试执行SQL语句
            result = connection.execute("SELECT 1")
            print(f"✅ SQL执行成功，结果: {result.fetchone()}")
            
            # 检查数据库是否存在
            db_name = SQLALCHEMY_DATABASE_URI.split('/')[-1].split('?')[0]
            print(f"当前数据库: {db_name}")
            
            return True
            
    except OperationalError as e:
        print(f"❌ 数据库连接失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def test_db_tables():
    """测试数据库表结构"""
    print("\n开始测试数据库表结构...")
    
    try:
        from extensions import db
        from app import create_app
        
        app = create_app()
        
        with app.app_context():
            # 获取所有表名
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"✅ 数据库表数量: {len(tables)}")
            print("表名列表:")
            for table in sorted(tables):
                print(f"  - {table}")
            
            # 检查核心表是否存在
            core_tables = ['user', 'role', 'menu_category', 'dish', 'customer', 'ingredient']
            missing_tables = []
            
            for table in core_tables:
                if table in tables:
                    print(f"✅ 核心表 '{table}' 存在")
                else:
                    print(f"❌ 核心表 '{table}' 不存在")
                    missing_tables.append(table)
            
            if not missing_tables:
                print("✅ 所有核心表都存在")
                return True
            else:
                print(f"❌ 缺少以下核心表: {missing_tables}")
                return False
                
    except Exception as e:
        print(f"❌ 测试表结构时出错: {e}")
        return False

if __name__ == "__main__":
    print("=== 数据库连接测试 ===")
    
    # 测试连接
    conn_success = test_db_connection()
    
    if conn_success:
        # 测试表结构
        tables_success = test_db_tables()
        
        if tables_success:
            print("\n🎉 数据库测试全部通过！")
        else:
            print("\n⚠️  数据库连接成功，但表结构存在问题")
    else:
        print("\n❌ 数据库连接失败")
