import requests
import json

# 测试登录
url = 'http://localhost:5000/api/auth/login'
headers = {'Content-Type': 'application/json'}

# 测试admin用户登录
data = {
    'username': 'admin',
    'password': 'admin123'
}

response = requests.post(url, data=json.dumps(data), headers=headers)
print('Admin登录测试:')
print(f'Status Code: {response.status_code}')
print(f'Response: {response.json()}')
print('-' * 80)

# 测试其他用户登录
test_users = [
    {'username': 'nutritionist', 'password': 'nutr123'},
    {'username': 'chef', 'password': 'chef123'},
    {'username': 'customer', 'password': 'cust123'}
]

for user in test_users:
    response = requests.post(url, data=json.dumps(user), headers=headers)
    print(f'{user["username"]}登录测试:')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')
    print('-' * 80)
