# 餐食管理系统技术架构文档

## 1. 系统架构

### 1.1 整体架构

餐食管理系统采用分层架构设计，包括前端、后端和数据库三个主要部分。后端基于 Flask 框架构建，提供 RESTful API 接口，前端通过这些接口与后端进行交互。

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    前端应用     │     │    后端服务     │     │    数据库       │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ - React/Angular │     │ - Flask        │     │ - MySQL         │
│ - REST API调用  │────▶│ - RESTful API  │────▶│ - 数据存储      │
│ - 响应式设计    │◀────│ - 业务逻辑      │◀────│ - 数据检索      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 1.2 后端架构

后端采用模块化设计，包括以下层次：

1. **表示层（API层）**：处理HTTP请求和响应，路由管理，请求验证
2. **业务逻辑层**：实现核心业务逻辑，如菜单管理、订单处理等
3. **数据访问层**：与数据库交互，实现数据的CRUD操作
4. **工具层**：提供通用功能，如安全认证、日志管理等

### 1.3 核心组件

| 组件 | 职责 | 技术实现 |
|------|------|----------|
| Flask | Web框架，处理HTTP请求 | Flask 2.2.5 |
| SQLAlchemy | ORM框架，数据库交互 | SQLAlchemy 1.4.46 |
| JWT | 用户认证和授权 | Flask-JWT-Extended 4.4.4 |
| Flask-Caching | 缓存管理 | Flask-Caching 2.0.2 |
| Pandas | 数据处理，Excel文件解析 | Pandas 2.0.3 |
| Prometheus | 系统监控 | prometheus-client 0.20.0 |
| Redis | 缓存存储（可选） | redis 4.5.4 |

## 2. 数据库设计

### 2.1 数据库模型

系统采用关系型数据库设计，包含以下主要模型：

1. **用户模型（User）**：存储用户信息，如用户名、密码哈希、角色等
2. **角色模型（Role）**：定义用户角色，如管理员、营养师、厨师等
3. **权限模型（Permission）**：定义系统权限，如创建、读取、更新、删除等
4. **菜单分类模型（MenuCategory）**：存储菜单分类信息
5. **菜品模型（Dish）**：存储菜品信息，如名称、描述、食材等
6. **菜单模型（Menu）**：存储菜单信息，如名称、描述、周数等
7. **菜单菜品关联模型（MenuDish）**：存储菜单与菜品的关联关系
8. **每日菜单模型（DailyMenu）**：存储每日菜单信息
9. **客户模型（Customer）**：存储客户信息，如姓名、联系方式等
10. **客户菜单选择模型（CustomerMenuSelection）**：存储客户的菜单选择
11. **客户订单模型（CustomerOrder）**：存储客户订单信息
12. **订单项目模型（OrderItem）**：存储订单项目信息
13. **食材模型（Ingredient）**：存储食材信息，如名称、数量、单位等
14. **菜品食材关联模型（DishIngredient）**：存储菜品与食材的关联关系

### 2.2 表结构

#### 2.2.1 用户表（user）

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INTEGER | PRIMARY KEY | 用户ID |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |
| deleted_at | DATETIME | NULL | 删除时间 |
| version | INTEGER | NOT NULL | 版本号 |
| username | VARCHAR(100) | NOT NULL, UNIQUE | 用户名 |
| email | VARCHAR(100) | UNIQUE | 邮箱 |
| phone | VARCHAR(20) | | 电话 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希 |
| full_name | VARCHAR(100) | | 全名 |
| department | VARCHAR(50) | | 部门 |
| position | VARCHAR(50) | | 职位 |
| avatar_url | VARCHAR(500) | | 头像URL |
| last_login_at | DATETIME | | 最后登录时间 |
| is_active | BOOLEAN | NOT NULL | 是否活跃 |
| is_superuser | BOOLEAN | NOT NULL | 是否超级用户 |
| color_theme | VARCHAR(20) | | 颜色主题 |

#### 2.2.2 角色表（role）

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INTEGER | PRIMARY KEY | 角色ID |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |
| deleted_at | DATETIME | NULL | 删除时间 |
| version | INTEGER | NOT NULL | 版本号 |
| name | VARCHAR(50) | NOT NULL, UNIQUE | 角色名称 |
| description | TEXT | | 角色描述 |
| is_system_role | BOOLEAN | NOT NULL | 是否系统角色 |

#### 2.2.3 菜品表（dish）

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| id | INTEGER | PRIMARY KEY | 菜品ID |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |
| deleted_at | DATETIME | NULL | 删除时间 |
| version | INTEGER | NOT NULL | 版本号 |
| name | VARCHAR(100) | NOT NULL | 菜品名称 |
| description | TEXT | | 菜品描述 |
| ingredients | JSON | | 食材列表 |
| dietary_restrictions | JSON | | 饮食限制 |
| calories_per_serving | NUMERIC(6,2) | | 每份热量 |
| price | NUMERIC(10,2) | NOT NULL | 价格 |
| preparation_time | INTEGER | | 准备时间 |
| category_id | INTEGER | FOREIGN KEY | 分类ID |
| image_url | VARCHAR(500) | | 图片URL |
| is_available | BOOLEAN | NOT NULL | 是否可用 |

## 3. API设计

### 3.1 API架构

系统采用 RESTful API 设计风格，所有API端点都以 `/api` 为前缀。API设计遵循以下原则：

- **资源导向**：API端点围绕资源设计，如 `/api/dishes`、`/api/menus` 等
- **HTTP方法**：使用标准HTTP方法，如 GET、POST、PUT、DELETE
- **状态码**：使用标准HTTP状态码表示请求结果
- **响应格式**：统一使用JSON格式响应

### 3.2 认证API

| 端点 | 方法 | 描述 | 请求体 | 响应 |
|------|------|------|--------|------|
| `/api/auth/register` | POST | 用户注册 | `{"username": "...", "password": "...", "role": "..."}` | `{"message": "...", "user_id": 1}` |
| `/api/auth/login` | POST | 用户登录 | `{"username": "...", "password": "..."}` | `{"access_token": "...", "user": {...}}` |
| `/api/auth/me` | GET | 获取当前用户信息 | N/A | `{"id": 1, "username": "...", "role": "..."}` |

### 3.3 菜单API

| 端点 | 方法 | 描述 | 请求体 | 响应 |
|------|------|------|--------|------|
| `/api/menus` | GET | 获取所有菜单 | N/A | `[{"id": 1, "name": "...", "description": "...", "week_number": 1}]` |
| `/api/menus` | POST | 创建新菜单 | `{"name": "...", "description": "...", "week_number": 1}` | `{"id": 1, "name": "...", "description": "...", "week_number": 1}` |
| `/api/menus/<id>` | GET | 获取单个菜单 | N/A | `{"id": 1, "name": "...", "description": "...", "week_number": 1}` |
| `/api/menus/<id>` | PUT | 更新菜单 | `{"name": "...", "description": "...", "week_number": 1}` | `{"id": 1, "name": "...", "description": "...", "week_number": 1}` |
| `/api/menus/<id>` | DELETE | 删除菜单 | N/A | `{"message": "Menu deleted successfully"}` |

### 3.4 菜品API

| 端点 | 方法 | 描述 | 请求体 | 响应 |
|------|------|------|--------|------|
| `/api/dishes` | GET | 获取所有菜品 | N/A | `[{"id": 1, "name": "...", "description": "...", "price": 10.99}]` |
| `/api/dishes` | POST | 创建新菜品 | `{"name": "...", "description": "...", "price": 10.99}` | `{"id": 1, "name": "...", "description": "...", "price": 10.99}` |
| `/api/dishes/<id>` | GET | 获取单个菜品 | N/A | `{"id": 1, "name": "...", "description": "...", "price": 10.99}` |
| `/api/dishes/<id>` | PUT | 更新菜品 | `{"name": "...", "description": "...", "price": 10.99}` | `{"id": 1, "name": "...", "description": "...", "price": 10.99}` |
| `/api/dishes/<id>` | DELETE | 删除菜品 | N/A | `{"message": "Dish deleted successfully"}` |

### 3.5 客户API

| 端点 | 方法 | 描述 | 请求体 | 响应 |
|------|------|------|--------|------|
| `/api/customers` | GET | 获取所有客户 | N/A | `[{"id": 1, "name": "...", "email": "...", "phone": "..."}]` |
| `/api/customers` | POST | 创建新客户 | `{"name": "...", "email": "...", "phone": "..."}` | `{"id": 1, "name": "...", "email": "...", "phone": "..."}` |
| `/api/customers/<id>` | GET | 获取单个客户 | N/A | `{"id": 1, "name": "...", "email": "...", "phone": "..."}` |
| `/api/customers/<id>` | PUT | 更新客户 | `{"name": "...", "email": "...", "phone": "..."}` | `{"id": 1, "name": "...", "email": "...", "phone": "..."}` |
| `/api/customers/<id>` | DELETE | 删除客户 | N/A | `{"message": "Customer deleted successfully"}` |

### 3.6 上传API

| 端点 | 方法 | 描述 | 请求体 | 响应 |
|------|------|------|--------|------|
| `/api/upload/excel` | POST | 上传Excel文件 | `multipart/form-data` | `{"message": "File uploaded and parsed successfully"}` |
| `/api/upload/image` | POST | 上传图片文件 | `multipart/form-data` | `{"message": "File uploaded successfully", "file_path": "..."}` |

## 4. 安全性

### 4.1 认证与授权

系统使用 JWT（JSON Web Token）进行用户认证和授权。认证流程如下：

1. 用户通过 `/api/auth/login` 端点登录，提供用户名和密码
2. 服务器验证用户名和密码，生成 JWT 令牌
3. 客户端在后续请求中携带 JWT 令牌
4. 服务器验证 JWT 令牌，确保用户已认证且有权限访问资源

### 4.2 权限控制

系统实现了基于角色的权限控制（RBAC），包括：

1. **角色定义**：系统预定义了多种角色，如管理员、营养师、厨师等
2. **权限映射**：为每个角色定义了可执行的操作和可访问的资源
3. **权限装饰器**：使用装饰器检查用户是否有权限执行特定操作

### 4.3 输入验证

系统对所有输入进行严格验证，包括：

1. **API请求参数验证**：验证所有API请求参数的格式和值
2. **文件上传验证**：验证文件类型、大小和内容
3. **SQL注入防护**：使用参数化查询和ORM框架防止SQL注入
4. **XSS防护**：对用户输入进行HTML转义，防止跨站脚本攻击

### 4.4 数据保护

系统采取以下措施保护数据安全：

1. **密码加密**：使用 Werkzeug 的安全哈希函数存储密码
2. **敏感数据脱敏**：在日志和错误信息中避免暴露敏感数据
3. **HTTPS传输**：建议在生产环境中使用HTTPS传输所有数据

## 5. 性能优化

### 5.1 缓存策略

系统实现了多级缓存策略，包括：

1. **内存缓存**：使用 Flask-Caching 实现内存缓存
2. **Redis缓存**：支持使用 Redis 作为分布式缓存
3. **缓存键设计**：基于资源类型和ID设计缓存键，如 `menu:1`、`dish:2` 等
4. **缓存失效**：当资源更新时，自动失效相关缓存

### 5.2 数据库优化

系统采取以下措施优化数据库性能：

1. **索引优化**：为常用查询字段添加索引
2. **查询优化**：使用 ORM 框架的查询优化功能，如延迟加载、批量查询等
3. **事务管理**：使用数据库事务确保数据一致性
4. **连接池**：使用连接池管理数据库连接，减少连接开销

### 5.3 代码优化

系统采取以下措施优化代码性能：

1. **异步处理**：对耗时操作使用异步处理
2. **批处理**：对批量操作使用批处理，减少数据库交互次数
3. **惰性加载**：对大型对象使用惰性加载，减少内存使用
4. **代码分析**：定期分析代码性能，优化关键路径

## 6. 监控与可观测性

### 6.1 系统监控

系统集成了 Prometheus 监控，收集以下指标：

1. **请求指标**：请求数量、响应时间、状态码分布
2. **系统指标**：CPU使用率、内存使用率、磁盘使用率
3. **业务指标**：订单数量、菜品种类、客户数量等

### 6.2 健康检查

系统提供了健康检查端点 `/health`，用于监控系统状态：

1. **数据库连接**：检查数据库连接状态
2. **缓存状态**：检查缓存系统状态
3. **系统状态**：检查系统资源使用情况

### 6.3 日志管理

系统实现了结构化日志管理，包括：

1. **请求日志**：记录所有API请求的详细信息
2. **错误日志**：记录系统错误和异常
3. **业务日志**：记录关键业务操作

## 7. 部署与运维

### 7.1 部署方式

系统支持多种部署方式：

1. **传统部署**：直接在服务器上安装和运行
2. **容器化部署**：使用 Docker 容器化部署
3. **容器编排**：使用 Docker Compose 或 Kubernetes 编排

### 7.2 环境配置

系统使用环境变量进行配置，主要配置项包括：

1. **数据库配置**：`DATABASE_URL`
2. **JWT配置**：`JWT_SECRET_KEY`
3. **上传配置**：`UPLOAD_FOLDER`、`ALLOWED_EXTENSIONS`
4. **CORS配置**：`CORS_ORIGINS`
5. **缓存配置**：`CACHE_TYPE`、`CACHE_REDIS_URL`

### 7.3 运维工具

系统提供了以下运维工具：

1. **数据库初始化**：`init_db.py` - 创建数据库表
2. **测试用户创建**：`create_test_users.py` - 创建测试用户
3. **用户检查**：`check_users.py` - 检查用户列表
4. **数据库检查**：`check_db.py` - 检查数据库状态

## 8. 总结

餐食管理系统采用现代化的技术架构，包括 Flask 后端框架、SQLAlchemy ORM、JWT 认证、Redis 缓存等。系统设计遵循分层架构原则，实现了模块化、可扩展的代码结构。

系统的核心功能包括菜单管理、菜品管理、客户管理、订单管理、文件上传等，通过 RESTful API 接口提供给前端使用。系统实现了基于角色的权限控制，确保数据安全和操作合规。

系统集成了监控和可观测性功能，便于运维和问题排查。同时，系统支持多种部署方式，适应不同的运行环境需求。

通过持续优化和改进，餐食管理系统将不断提升性能、安全性和用户体验，为餐饮运营提供更加高效、可靠的管理工具。