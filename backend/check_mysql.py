import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
db_url = os.getenv('DATABASE_URL')
print(f"Current DATABASE_URL: {db_url}")

# 解析连接参数
if db_url.startswith('mysql+pymysql://'):
    # 解析连接字符串
    conn_str = db_url.replace('mysql+pymysql://', '')
    user_pass, host_db = conn_str.split('@')
    user, password = user_pass.split(':')
    host_port, db_name = host_db.split('/')
    host, port = host_port.split(':')
    
    print(f"\nConnection Parameters:")
    print(f"User: {user}")
    print(f"Password: {'*' * len(password)}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Database: {db_name}")
    
    # 尝试连接
    try:
        print("\nTrying to connect to MySQL...")
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=int(port),
            database=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✓ Connected successfully!")
        
        # 检查数据库是否存在
        with conn.cursor() as cursor:
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()
            db_exists = any(db['Database'] == db_name for db in databases)
            print(f"Database '{db_name}' exists: {db_exists}")
            
            if not db_exists:
                print(f"Creating database '{db_name}'...")
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                print("✓ Database created successfully!")
        
        conn.close()
        print("✓ Connection closed.")
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        
        # 尝试不指定数据库连接
        try:
            print("\nTrying to connect without specifying database...")
            conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=int(port),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("✓ Connected successfully!")
            
            # 创建数据库
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                print(f"✓ Database '{db_name}' created successfully!")
            
            conn.close()
            print("✓ Connection closed.")
            
        except Exception as e2:
            print(f"✗ Connection without database failed: {e2}")
else:
    print("Not a MySQL connection string.")
