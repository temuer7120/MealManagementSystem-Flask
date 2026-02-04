import requests
import json
import pytest

# 测试登录
url = 'http://127.0.0.1:5000/api/auth/login'
headers = {'Content-Type': 'application/json'}

def test_admin_login():
    """测试admin用户登录"""
    data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('Admin登录测试:')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')
    print('-' * 80)
    
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_nutritionist_login():
    """测试营养师用户登录"""
    data = {
        'username': 'nutritionist',
        'password': 'nutr123'
    }
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('Nutritionist登录测试:')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')
    print('-' * 80)
    
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_chef_login():
    """测试厨师用户登录"""
    data = {
        'username': 'chef',
        'password': 'chef123'
    }
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('Chef登录测试:')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')
    print('-' * 80)
    
    assert response.status_code == 200
    assert 'access_token' in response.json()
