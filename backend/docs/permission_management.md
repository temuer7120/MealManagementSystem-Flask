# 权限管理方案

## 1. 设计理念

本系统采用基于角色的访问控制（Role-Based Access Control，RBAC）模型，结合资源级别的权限控制，实现了细粒度的权限管理。系统设计遵循以下原则：

- **最小权限原则**：用户只获得完成任务所需的最小权限
- **职责分离**：不同角色有不同的职责和权限范围
- **权限继承**：高级角色继承低级角色的权限
- **灵活性**：支持动态调整角色和权限
- **安全性**：确保所有敏感操作都有适当的权限控制

## 2. 角色定义

系统定义了以下角色，按照权限从高到低排序：

| 角色 | 描述 | 核心权限 |
|------|------|----------|
| admin | 系统管理员 | 所有权限，包括系统配置和数据管理 |
| nutritionist | 营养师 | 菜单、菜品、食材的管理，Excel文件上传 |
| chef | 厨师 | 菜品、食材的管理，Excel文件上传 |
| admin_staff | 行政人员 | 客户管理，Excel文件上传 |
| head_nurse | 护士长 | 客户信息查看和更新，排餐表管理 |
| nurse | 护士 | 客户信息查看和更新，排餐表管理 |
| caregiver | 护理员 | 客户信息查看和更新，排餐表管理 |
| customer | 客户 | 只能查看与自己相关的信息 |
| guest | 访客 | 只能查看公开信息 |

## 3. 资源权限定义

系统为以下资源定义了细粒度的权限控制：

### 3.1 菜单（menu）

| 角色 | create | read | update | delete |
|------|--------|------|--------|--------|
| admin | ✅ | ✅ | ✅ | ✅ |
| nutritionist | ✅ | ✅ | ✅ | ✅ |
| chef | ❌ | ✅ | ✅ | ❌ |
| admin_staff | ❌ | ✅ | ❌ | ❌ |
| head_nurse | ❌ | ✅ | ❌ | ❌ |
| nurse | ❌ | ✅ | ❌ | ❌ |
| caregiver | ❌ | ✅ | ❌ | ❌ |
| customer | ❌ | ✅ | ❌ | ❌ |
| guest | ❌ | ✅ | ❌ | ❌ |

### 3.2 菜品（dish）

| 角色 | create | read | update | delete |
|------|--------|------|--------|--------|
| admin | ✅ | ✅ | ✅ | ✅ |
| nutritionist | ✅ | ✅ | ✅ | ✅ |
| chef | ✅ | ✅ | ✅ | ✅ |
| admin_staff | ❌ | ✅ | ❌ | ❌ |
| head_nurse | ❌ | ✅ | ❌ | ❌ |
| nurse | ❌ | ✅ | ❌ | ❌ |
| caregiver | ❌ | ✅ | ❌ | ❌ |
| customer | ❌ | ✅ | ❌ | ❌ |
| guest | ❌ | ✅ | ❌ | ❌ |

### 3.3 客户（customer）

| 角色 | create | read | update | delete |
|------|--------|------|--------|--------|
| admin | ✅ | ✅ | ✅ | ✅ |
| nutritionist | ❌ | ✅ | ✅ | ❌ |
| chef | ❌ | ✅ | ❌ | ❌ |
| admin_staff | ✅ | ✅ | ✅ | ✅ |
| head_nurse | ❌ | ✅ | ✅ | ❌ |
| nurse | ❌ | ✅ | ✅ | ❌ |
| caregiver | ❌ | ✅ | ✅ | ❌ |
| customer | ❌ | ✅ | ❌ | ❌ |
| guest | ❌ | ✅ | ❌ | ❌ |

### 3.4 食材（ingredient）

| 角色 | create | read | update | delete |
|------|--------|------|--------|--------|
| admin | ✅ | ✅ | ✅ | ✅ |
| nutritionist | ✅ | ✅ | ✅ | ✅ |
| chef | ✅ | ✅ | ✅ | ✅ |
| admin_staff | ❌ | ✅ | ❌ | ❌ |
| head_nurse | ❌ | ✅ | ❌ | ❌ |
| nurse | ❌ | ✅ | ❌ | ❌ |
| caregiver | ❌ | ✅ | ❌ | ❌ |
| customer | ❌ | ✅ | ❌ | ❌ |
| guest | ❌ | ✅ | ❌ | ❌ |

### 3.5 上传（upload）

| 角色 | upload |
|------|--------|
| admin | ✅ |
| nutritionist | ✅ |
| chef | ✅ |
| admin_staff | ✅ |
| head_nurse | ❌ |
| nurse | ❌ |
| caregiver | ❌ |
| customer | ❌ |
| guest | ❌ |

### 3.6 订单（order）

| 角色 | create | read | update | delete |
|------|--------|------|--------|--------|
| admin | ✅ | ✅ | ✅ | ✅ |
| nutritionist | ❌ | ✅ | ❌ | ❌ |
| chef | ❌ | ✅ | ❌ | ❌ |
| admin_staff | ✅ | ✅ | ✅ | ✅ |
| head_nurse | ❌ | ✅ | ❌ | ❌ |
| nurse | ❌ | ✅ | ❌ | ❌ |
| caregiver | ❌ | ✅ | ❌ | ❌ |
| customer | ❌ | ✅ | ❌ | ❌ |
| guest | ❌ | ✅ | ❌ | ❌ |

### 3.7 排餐表（meal_schedule）

| 角色 | create | read | update | delete |
|------|--------|------|--------|--------|
| admin | ✅ | ✅ | ✅ | ✅ |
| nutritionist | ✅ | ✅ | ✅ | ✅ |
| chef | ❌ | ✅ | ✅ | ❌ |
| admin_staff | ❌ | ✅ | ❌ | ❌ |
| head_nurse | ❌ | ✅ | ✅ | ❌ |
| nurse | ❌ | ✅ | ✅ | ❌ |
| caregiver | ❌ | ✅ | ✅ | ❌ |
| customer | ❌ | ✅ | ❌ | ❌ |
| guest | ❌ | ✅ | ❌ | ❌ |

## 4. 权限控制实现

### 4.1 核心组件

权限控制通过以下组件实现：

1. **权限映射配置**：在 `utils/security.py` 中定义了 `ROLE_PERMISSIONS` 和 `RESOURCE_PERMISSIONS` 字典，存储角色和资源的权限映射

2. **权限装饰器**：
   - `requires_permission(action)`：检查用户是否有执行特定操作的权限
   - `requires_resource_permission(resource, action)`：检查用户是否有操作特定资源的权限

3. **JWT认证**：使用 JSON Web Token 进行用户认证，确保只有登录用户才能访问受保护的资源

### 4.2 实现代码

#### 权限映射配置

```python
# 角色权限映射
ROLE_PERMISSIONS = {
    'admin': ['create', 'read', 'update', 'delete', 'upload', 'init'],
    'nutritionist': ['create', 'read', 'update', 'delete', 'upload'],
    'chef': ['create', 'read', 'update', 'delete', 'upload'],
    'admin_staff': ['create', 'read', 'update', 'delete', 'upload'],
    'head_nurse': ['read', 'update'],
    'nurse': ['read', 'update'],
    'caregiver': ['read', 'update'],
    'customer': ['read'],
    'guest': ['read']
}

# 资源权限映射
RESOURCE_PERMISSIONS = {
    'menu': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['create', 'read', 'update', 'delete'],
        'chef': ['read', 'update'],
        # 其他角色...
    },
    # 其他资源...
}
```

#### 权限装饰器

```python
def requires_resource_permission(resource, action):
    """资源权限装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
            
            # 检查用户角色是否有权限操作该资源
            user_role = user.role
            if user_role not in RESOURCE_PERMISSIONS.get(resource, {}):
                return jsonify({'error': 'Role not authorized for this resource'}), 403
            
            if action not in RESOURCE_PERMISSIONS[resource][user_role]:
                return jsonify({'error': 'Permission denied for this action'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

#### API端点权限控制

```python
@api.route('/upload/excel', methods=['POST'])
@requires_resource_permission('upload', 'upload')
def upload_excel():
    """上传Excel文件并解析排餐表"""
    # 实现代码...

@api.route('/ingredients', methods=['POST'])
@requires_resource_permission('ingredient', 'create')
def create_ingredient():
    """创建新食材"""
    # 实现代码...
```

## 5. 安全最佳实践

### 5.1 认证与授权

- **使用HTTPS**：确保所有API请求都通过HTTPS传输
- **强密码策略**：要求用户使用强密码，并定期更换
- **JWT安全**：设置合理的JWT过期时间，使用安全的签名算法
- **防暴力破解**：实现登录失败次数限制和账户锁定机制
- **会话管理**：确保用户会话安全，支持会话超时和强制下线

### 5.2 输入验证

- **所有输入必须验证**：包括API请求参数、文件上传、表单数据等
- **使用参数绑定**：避免SQL注入攻击
- **文件上传安全**：限制文件类型、大小，扫描恶意文件
- **XSS防护**：对用户输入进行HTML转义，防止跨站脚本攻击
- **CSRF防护**：实现跨站请求伪造防护

### 5.3 数据保护

- **加密存储**：敏感数据（如密码）必须加密存储
- **数据脱敏**：在日志和错误信息中避免暴露敏感数据
- **访问日志**：记录所有敏感操作的访问日志
- **审计跟踪**：实现数据变更的审计跟踪
- **备份策略**：定期备份数据库，确保数据可恢复

## 6. 维护与扩展

### 6.1 权限管理维护

- **定期审查**：定期审查角色和权限设置，确保符合业务需求
- **权限调整**：根据业务变化及时调整角色和权限
- **权限审计**：定期审计权限使用情况，发现异常权限使用

### 6.2 权限系统扩展

- **动态角色管理**：支持在系统中动态创建和管理角色
- **用户组管理**：支持用户分组，简化权限管理
- **权限模板**：提供常见权限组合的模板
- **权限继承**：实现更复杂的权限继承关系
- **外部认证集成**：支持与LDAP、OAuth等外部认证系统集成

### 6.3 监控与告警

- **权限异常监控**：监控异常的权限使用情况
- **安全事件告警**：对可疑的权限操作进行告警
- **性能监控**：监控权限检查对系统性能的影响

## 7. 总结

本权限管理方案实现了一个安全、灵活、可扩展的权限控制系统，满足了餐饮管理系统的各种权限需求。通过RBAC模型和资源级权限控制，确保了系统的安全性和可维护性。

系统的权限管理设计不仅满足了当前的业务需求，也为未来的业务扩展和功能升级预留了空间。通过定期的权限审查和维护，可以确保权限系统始终与业务需求保持一致，为系统的安全运行提供有力保障。