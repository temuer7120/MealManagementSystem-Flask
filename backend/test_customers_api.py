import requests

base_url = 'http://localhost:5000/api'

try:
    response = requests.get(f'{base_url}/customers')
    print(f'状态码: {response.status_code}')
    
    if response.status_code == 200:
        customers = response.json()
        print(f'客户总数: {len(customers)}')
        print('\n客户列表:')
        print('-' * 80)
        for customer in customers:
            print(f"ID: {customer['id']:3d} | 姓名: {customer['name']:20s} | 入住日期: {customer.get('check_in_date', 'N/A'):12s} | 状态: {customer.get('status', 'N/A')}")
        print('-' * 80)
        
        if len(customers) > 0:
            print(f'\n现在入住的客户:')
            active_customers = [c for c in customers if c.get('status') == 'active']
            for customer in active_customers:
                print(f"  - {customer['name']} (ID: {customer['id']})")
    else:
        print(f'请求失败: {response.text}')
        
except Exception as e:
    print(f'发生错误: {e}')