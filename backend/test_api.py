import requests
import json

print("测试后端API端点...")
print("=" * 60)

# 测试基础连接
base_url = "http://localhost:5000"

# 1. 测试根路径
print("\n1. 测试根路径:")
try:
    response = requests.get(f"{base_url}/")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.text[:100]}")
except Exception as e:
    print(f"   错误: {str(e)}")

# 2. 测试服务预定API
print("\n2. 测试服务预定API:")
try:
    response = requests.get(f"{base_url}/api/service-bookings")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   数据数量: {len(data) if isinstance(data, list) else 'N/A'}")
        if isinstance(data, list) and len(data) > 0:
            print(f"   第一条数据: {json.dumps(data[0], ensure_ascii=False, indent=2)[:200]}")
    else:
        print(f"   响应: {response.text[:200]}")
except Exception as e:
    print(f"   错误: {str(e)}")

# 3. 测试客户API
print("\n3. 测试客户API:")
try:
    response = requests.get(f"{base_url}/api/customers")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   数据数量: {len(data) if isinstance(data, list) else 'N/A'}")
        if isinstance(data, list) and len(data) > 0:
            print(f"   第一条数据: {json.dumps(data[0], ensure_ascii=False, indent=2)[:200]}")
    else:
        print(f"   响应: {response.text[:200]}")
except Exception as e:
    print(f"   错误: {str(e)}")

# 4. 测试菜品API
print("\n4. 测试菜品API:")
try:
    response = requests.get(f"{base_url}/api/dishes")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   数据数量: {len(data) if isinstance(data, list) else 'N/A'}")
        if isinstance(data, list) and len(data) > 0:
            print(f"   第一条数据: {json.dumps(data[0], ensure_ascii=False, indent=2)[:200]}")
    else:
        print(f"   响应: {response.text[:200]}")
except Exception as e:
    print(f"   错误: {str(e)}")

# 5. 测试订单API
print("\n5. 测试订单API:")
try:
    response = requests.get(f"{base_url}/api/orders")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   数据数量: {len(data) if isinstance(data, list) else 'N/A'}")
        if isinstance(data, list) and len(data) > 0:
            print(f"   第一条数据: {json.dumps(data[0], ensure_ascii=False, indent=2)[:200]}")
    else:
        print(f"   响应: {response.text[:200]}")
except Exception as e:
    print(f"   错误: {str(e)}")

print("\n" + "=" * 60)
print("API测试完成！")