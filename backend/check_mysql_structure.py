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
        print("\nConnecting to MySQL database...")
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
        
        # 列出所有表
        with conn.cursor() as cursor:
            print("\n=== Listing all tables in database ===")
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            table_names = [table[f'Tables_in_{db_name}'] for table in tables]
            
            print(f"Total tables: {len(table_names)}")
            print("Tables:")
            for i, table_name in enumerate(table_names, 1):
                print(f"  {i}. {table_name}")
            
            # 检查核心表结构
            print("\n=== Checking core table structures ===")
            core_tables = [
                'user', 'role', 'permission', 'user_role', 'role_permission',
                'customer', 'customer_order', 'order_item',
                'dish', 'menu_category', 'menu', 'menu_dish', 'daily_menu', 'daily_menu_dish',
                'ingredient', 'ingredient_category', 'supplier', 'purchase_order', 'purchase_order_item',
                'service_category', 'service_item', 'service_package', 'service_booking',
                'confinement_meal_plan', 'confinement_week_plan', 'confinement_day_plan', 'confinement_meal_item',
                'delivery_schedule', 'delivery_assignment', 'delivery_route', 'delivery_status_update',
                'ai_analysis_job', 'ai_analysis_result', 'report_template', 'generated_report', 'alert_rule', 'alert'
            ]
            
            print("\n=== Checking table existence ===")
            existing_tables = []
            missing_tables = []
            
            for table in core_tables:
                if table in table_names:
                    existing_tables.append(table)
                    print(f"✓ {table} - exists")
                else:
                    missing_tables.append(table)
                    print(f"✗ {table} - missing")
            
            print(f"\nSummary:")
            print(f"Existing tables: {len(existing_tables)}")
            print(f"Missing tables: {len(missing_tables)}")
            
            # 检查表结构
            print("\n=== Checking table structures ===")
            for table in existing_tables[:5]:  # 检查前5个表的详细结构
                print(f"\n--- {table} table structure ---")
                cursor.execute(f"DESCRIBE {table};")
                columns = cursor.fetchall()
                print(f"Columns: {len(columns)}")
                for col in columns:
                    print(f"  {col['Field']} - {col['Type']} - {col['Null']} - {col['Default']} - {col['Key']}")
        
        conn.close()
        print("\n✓ Connection closed.")
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
else:
    print("Not a MySQL connection string.")
