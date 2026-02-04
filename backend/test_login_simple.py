import requests
import json

# 测试登录
url = 'http://127.0.0.1:5000/api/auth/login'
headers = {'Content-Type': 'application/json'}

# 测试admin用户登录
data = {
    'username': 'admin',
    'password': 'admin123'
}

print('测试登录端点...')
try:
    # 直接使用json参数，而不是data参数
    response = requests.post(url, json=data, timeout=5)
    print(f'Status Code: {response.status_code}')
    print(f'Response Text: {response.text}')
    if response.status_code == 200:
        print(f'Response JSON: {response.json()}')
except Exception as e:
    print(f'Error: {str(e)}')
print('-' * 80)