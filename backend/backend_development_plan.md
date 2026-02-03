# 后端开发计划

## 1. 技术选型

### 1.1 核心框架
- **Web框架**：Flask
  - 选择理由：轻量级、灵活、扩展丰富、适合构建RESTful API
  - 版本：2.x

### 1.2 数据库
- **主数据库**：MySQL
  - 选择理由：稳定可靠、性能优秀、适合关系型数据存储、社区活跃
  - 版本：8.x
- **缓存数据库**：Redis
  - 选择理由：高性能、支持多种数据结构、适合缓存和会话存储
  - 版本：7.x

### 1.3 ORM
- **ORM**：SQLAlchemy
  - 选择理由：功能强大、支持多种数据库、Pythonic API、事务支持
  - 版本：2.x

### 1.4 认证
- **认证方式**：JWT (JSON Web Token)
  - 选择理由：无状态、便于水平扩展、适合RESTful API
  - 库：Flask-JWT-Extended

### 1.5 其他扩展
- **CORS**：Flask-CORS
  - 选择理由：处理跨域请求、配置灵活
- **表单验证**：Flask-WTF
  - 选择理由：表单验证、CSRF保护
- **文件上传**：Flask-Uploads
  - 选择理由：文件上传处理、安全可靠
- **API文档**：Flask-RESTPlus/Flask-RESTx
  - 选择理由：API文档自动生成、Swagger UI集成

### 1.6 工具库
- **HTTP客户端**：Requests
  - 选择理由：API简洁、功能强大、广泛使用
- **日期处理**：Arrow
  - 选择理由：比datetime更友好的API、时区支持
- **加密**：Passlib
  - 选择理由：密码哈希、多种哈希算法支持
- **Excel处理**：Pandas + Openpyxl
  - 选择理由：强大的Excel文件处理能力
- **日志**：Python标准库logging + Loguru
  - 选择理由：结构化日志、异常处理

### 1.7 开发工具
- **代码检查**：Flake8
- **类型提示**：MyPy
- **测试框架**：pytest
- **数据库迁移**：Alembic

## 2. 架构设计

### 2.1 整体架构
- **架构风格**：分层架构
  - 表现层（API层）：处理HTTP请求和响应
  - 业务逻辑层：实现核心业务逻辑
  - 数据访问层：处理数据库操作
  - 基础设施层：提供通用功能和服务

### 2.2 模块划分
- **api**：API路由和控制器
- **services**：业务逻辑服务
- **models**：数据库模型
- **schemas**：数据验证和序列化
- **utils**：工具函数和辅助类
- **config**：配置管理
- **extensions**：扩展初始化
- **middlewares**：中间件
- **tasks**：异步任务
- **mother_baby**：母婴服务相关功能

### 2.3 目录结构
```
backend/
├── api/
│   ├── __init__.py
│   ├── auth.py        # 认证相关API
│   ├── menu.py        # 菜单相关API
│   ├── dish.py        # 菜品相关API
│   ├── customer.py    # 客户相关API
│   ├── order.py       # 订单相关API
│   ├── system.py      # 系统相关API
│   ├── upload.py      # 文件上传API
│   └── mother_baby.py # 母婴服务相关API
├── services/
│   ├── __init__.py
│   ├── auth_service.py     # 认证服务
│   ├── menu_service.py     # 菜单服务
│   ├── dish_service.py     # 菜品服务
│   ├── customer_service.py # 客户服务
│   ├── order_service.py    # 订单服务
│   ├── system_service.py   # 系统服务
│   ├── upload_service.py   # 文件上传服务
│   └── mother_baby_service.py # 母婴服务
├── models/
│   ├── __init__.py
│   ├── base.py        # 基础模型
│   ├── user.py        # 用户模型
│   ├── menu.py        # 菜单模型
│   ├── dish.py        # 菜品模型
│   ├── customer.py    # 客户模型
│   ├── order.py       # 订单模型
│   ├── system.py      # 系统模型
│   └── mother_baby.py # 母婴服务相关模型
├── schemas/
│   ├── __init__.py
│   ├── auth.py        # 认证相关模式
│   ├── menu.py        # 菜单相关模式
│   ├── dish.py        # 菜品相关模式
│   ├── customer.py    # 客户相关模式
│   ├── order.py       # 订单相关模式
│   ├── system.py      # 系统相关模式
│   └── mother_baby.py # 母婴服务相关模式
├── utils/
│   ├── __init__.py
│   ├── security.py    # 安全相关工具
│   ├── validator.py   # 数据验证工具
│   ├── excel.py       # Excel处理工具
│   └── response.py    # 响应处理工具
├── config/
│   ├── __init__.py
│   ├── base.py        # 基础配置
│   ├── development.py # 开发环境配置
│   ├── testing.py     # 测试环境配置
│   └── production.py  # 生产环境配置
├── extensions/
│   ├── __init__.py
│   ├── db.py          # 数据库扩展
│   ├── jwt.py         # JWT扩展
│   ├── cors.py        # CORS扩展
│   └── cache.py       # 缓存扩展
├── middlewares/
│   ├── __init__.py
│   ├── auth.py        # 认证中间件
│   ├── error.py       # 错误处理中间件
│   └── logger.py      # 日志中间件
├── tasks/
│   ├── __init__.py
│   ├── celery.py      # Celery配置
│   └── tasks.py       # 异步任务定义
├── app.py             # 应用入口
├── wsgi.py            # WSGI入口
├── requirements.txt   # 依赖包
└── migrations/        # 数据库迁移文件
```

## 3. 数据库设计

### 3.1 核心模型

#### 3.1.1 用户模型 (`user`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 用户ID |
| `username` | `VARCHAR(100)` | `UNIQUE, NOT NULL` | 用户名 |
| `email` | `VARCHAR(100)` | `UNIQUE` | 邮箱 |
| `phone` | `VARCHAR(20)` | | 手机号 |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` | 密码哈希 |
| `full_name` | `VARCHAR(100)` | | 全名 |
| `department` | `VARCHAR(50)` | | 部门 |
| `position` | `VARCHAR(50)` | | 职位 |
| `avatar_url` | `VARCHAR(500)` | | 头像URL |
| `color_theme` | `VARCHAR(20)` | | 主题颜色 |
| `last_login_at` | `DATETIME` | | 最后登录时间 |
| `is_active` | `BOOLEAN` | `DEFAULT TRUE` | 是否激活 |
| `is_superuser` | `BOOLEAN` | `DEFAULT FALSE` | 是否超级用户 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.15 月子餐计划模型 (`confinement_meal_plan`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 计划ID |
| `plan_number` | `VARCHAR(50)` | `UNIQUE, NOT NULL` | 计划编号 |
| `customer_id` | `INT` | `FOREIGN KEY (customer.id)` | 客户ID |
| `start_date` | `DATE` | `NOT NULL` | 开始日期 |
| `end_date` | `DATE` | | 结束日期 |
| `total_days` | `INT` | | 总天数 |
| `total_weeks` | `INT` | | 总周数 |
| `meal_plan_type` | `VARCHAR(20)` | | 计划类型 |
| `total_calories_per_day` | `DECIMAL(8,2)` | | 每日总卡路里 |
| `total_price` | `DECIMAL(12,2)` | `DEFAULT 0` | 总价格 |
| `discount_amount` | `DECIMAL(10,2)` | | 折扣金额 |
| `final_price` | `DECIMAL(12,2)` | `DEFAULT 0` | 最终价格 |
| `status` | `VARCHAR(20)` | `DEFAULT 'draft'` | 状态 |
| `notes` | `TEXT` | | 备注 |
| `created_by` | `INT` | `FOREIGN KEY (user.id)` | 创建人ID |
| `approved_by` | `INT` | `FOREIGN KEY (user.id)` | 审批人ID |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.16 月子餐周计划模型 (`confinement_week_plan`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 周计划ID |
| `meal_plan_id` | `INT` | `FOREIGN KEY (confinement_meal_plan.id)` | 计划ID |
| `week_number` | `INT` | `NOT NULL` | 周数 |
| `focus_area` | `VARCHAR(100)` | | 重点区域 |
| `nutrition_goals` | `JSON` | | 营养目标 |
| `avoid_foods` | `JSON` | | 禁忌食物 |
| `recommended_foods` | `JSON` | | 推荐食物 |
| `notes` | `TEXT` | | 备注 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.17 月子餐日计划模型 (`confinement_day_plan`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 日计划ID |
| `week_plan_id` | `INT` | `FOREIGN KEY (confinement_week_plan.id)` | 周计划ID |
| `day_number` | `INT` | `NOT NULL` | 日数 |
| `date` | `DATE` | | 日期 |
| `total_calories` | `DECIMAL(8,2)` | | 总卡路里 |
| `nutrition_summary` | `JSON` | | 营养总结 |
| `special_notes` | `TEXT` | | 特别备注 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.18 月子餐单项模型 (`confinement_meal_item`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 餐单项ID |
| `day_plan_id` | `INT` | `FOREIGN KEY (confinement_day_plan.id)` | 日计划ID |
| `meal_type` | `VARCHAR(50)` | `NOT NULL` | 餐食类型 |
| `dish_id` | `INT` | `FOREIGN KEY (dish.id)` | 菜品ID |
| `serving_time` | `TIME` | | 供应时间 |
| `quantity` | `INT` | `DEFAULT 1` | 数量 |
| `calories` | `DECIMAL(8,2)` | | 卡路里 |
| `nutrition_details` | `JSON` | | 营养详情 |
| `special_instructions` | `TEXT` | | 特别说明 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.19 健康记录模型 (`health_record`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 记录ID |
| `customer_id` | `INT` | `FOREIGN KEY (customer.id)` | 客户ID |
| `record_type` | `VARCHAR(50)` | `NOT NULL` | 记录类型 |
| `record_date` | `DATE` | `NOT NULL` | 记录日期 |
| `health_data` | `JSON` | | 健康数据 |
| `notes` | `TEXT` | | 备注 |
| `created_by` | `INT` | `FOREIGN KEY (user.id)` | 创建人ID |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.2 角色模型 (`role`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 角色ID |
| `name` | `VARCHAR(50)` | `UNIQUE, NOT NULL` | 角色名称 |
| `description` | `TEXT` | | 角色描述 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.3 用户角色关联模型 (`user_role`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 关联ID |
| `user_id` | `INT` | `FOREIGN KEY (user.id)` | 用户ID |
| `role_id` | `INT` | `FOREIGN KEY (role.id)` | 角色ID |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

#### 3.1.4 月子餐计划模型 (`confinement_meal_plan`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 计划ID |
| `plan_number` | `VARCHAR(50)` | `UNIQUE, NOT NULL` | 计划编号 |
| `customer_id` | `INT` | `FOREIGN KEY (customer.id)` | 客户ID |
| `start_date` | `DATE` | `NOT NULL` | 开始日期 |
| `end_date` | `DATE` | | 结束日期 |
| `total_days` | `INT` | | 总天数 |
| `total_weeks` | `INT` | | 总周数 |
| `meal_plan_type` | `VARCHAR(20)` | | 计划类型 |
| `total_calories_per_day` | `DECIMAL(8,2)` | | 每日总卡路里 |
| `total_price` | `DECIMAL(12,2)` | `DEFAULT 0` | 总价格 |
| `discount_amount` | `DECIMAL(10,2)` | | 折扣金额 |
| `final_price` | `DECIMAL(12,2)` | `DEFAULT 0` | 最终价格 |
| `status` | `VARCHAR(20)` | `DEFAULT 'draft'` | 状态 |
| `notes` | `TEXT` | | 备注 |
| `created_by` | `INT` | `FOREIGN KEY (user.id)` | 创建人ID |
| `approved_by` | `INT` | `FOREIGN KEY (user.id)` | 审批人ID |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.5 月子餐周计划模型 (`confinement_week_plan`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 周计划ID |
| `meal_plan_id` | `INT` | `FOREIGN KEY (confinement_meal_plan.id)` | 计划ID |
| `week_number` | `INT` | `NOT NULL` | 周数 |
| `focus_area` | `VARCHAR(100)` | | 重点区域 |
| `nutrition_goals` | `JSON` | | 营养目标 |
| `avoid_foods` | `JSON` | | 禁忌食物 |
| `recommended_foods` | `JSON` | | 推荐食物 |
| `notes` | `TEXT` | | 备注 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.6 月子餐日计划模型 (`confinement_day_plan`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 日计划ID |
| `week_plan_id` | `INT` | `FOREIGN KEY (confinement_week_plan.id)` | 周计划ID |
| `day_number` | `INT` | `NOT NULL` | 日数 |
| `date` | `DATE` | | 日期 |
| `total_calories` | `DECIMAL(8,2)` | | 总卡路里 |
| `nutrition_summary` | `JSON` | | 营养总结 |
| `special_notes` | `TEXT` | | 特别备注 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.7 月子餐单项模型 (`confinement_meal_item`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 餐单项ID |
| `day_plan_id` | `INT` | `FOREIGN KEY (confinement_day_plan.id)` | 日计划ID |
| `meal_type` | `VARCHAR(50)` | `NOT NULL` | 餐食类型 |
| `dish_id` | `INT` | `FOREIGN KEY (dish.id)` | 菜品ID |
| `serving_time` | `TIME` | | 供应时间 |
| `quantity` | `INT` | `DEFAULT 1` | 数量 |
| `calories` | `DECIMAL(8,2)` | | 卡路里 |
| `nutrition_details` | `JSON` | | 营养详情 |
| `special_instructions` | `TEXT` | | 特别说明 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.8 健康记录模型 (`health_record`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 记录ID |
| `customer_id` | `INT` | `FOREIGN KEY (customer.id)` | 客户ID |
| `record_type` | `VARCHAR(50)` | `NOT NULL` | 记录类型 |
| `record_date` | `DATE` | `NOT NULL` | 记录日期 |
| `health_data` | `JSON` | | 健康数据 |
| `notes` | `TEXT` | | 备注 |
| `created_by` | `INT` | `FOREIGN KEY (user.id)` | 创建人ID |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.9 预约模型 (`appointment`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 预约ID |
| `customer_id` | `INT` | `FOREIGN KEY (customer.id)` | 客户ID |
| `service_type` | `VARCHAR(50)` | `NOT NULL` | 服务类型 |
| `appointment_date` | `DATE` | `NOT NULL` | 预约日期 |
| `appointment_time` | `TIME` | `NOT NULL` | 预约时间 |
| `status` | `VARCHAR(20)` | `DEFAULT 'pending'` | 状态 |
| `notes` | `TEXT` | | 备注 |
| `created_by` | `INT` | `FOREIGN KEY (user.id)` | 创建人ID |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.10 菜单分类模型 (`menu_category`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 分类ID |
| `name` | `VARCHAR(50)` | `NOT NULL` | 分类名称（早餐、午餐、晚餐） |
| `description` | `TEXT` | | 分类描述 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.5 菜品模型 (`dish`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 菜品ID |
| `name` | `VARCHAR(100)` | `NOT NULL` | 菜品名称 |
| `description` | `TEXT` | | 菜品描述 |
| `price` | `DECIMAL(10,2)` | | 价格 |
| `category_id` | `INT` | `FOREIGN KEY (menu_category.id)` | 分类ID |
| `image_url` | `VARCHAR(500)` | | 菜品图片URL |
| `nutrition_info` | `JSON` | | 营养成分信息 |
| `is_available` | `BOOLEAN` | `DEFAULT TRUE` | 是否可用 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.6 菜单模型 (`menu`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 菜单ID |
| `name` | `VARCHAR(100)` | `NOT NULL` | 菜单名称 |
| `description` | `TEXT` | | 菜单描述 |
| `menu_type` | `VARCHAR(20)` | `NOT NULL` | 菜单类型（基础菜单、定制菜单） |
| `is_active` | `BOOLEAN` | `DEFAULT TRUE` | 是否激活 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.7 菜单菜品关联模型 (`menu_dish`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 关联ID |
| `menu_id` | `INT` | `FOREIGN KEY (menu.id)` | 菜单ID |
| `dish_id` | `INT` | `FOREIGN KEY (dish.id)` | 菜品ID |
| `quantity` | `INT` | `DEFAULT 1` | 数量 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

#### 3.1.8 每日菜单模型 (`daily_menu`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 每日菜单ID |
| `menu_date` | `DATE` | `NOT NULL` | 菜单日期 |
| `category_id` | `INT` | `FOREIGN KEY (menu_category.id)` | 分类ID |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.9 每日菜单菜品关联模型 (`daily_menu_dish`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 关联ID |
| `daily_menu_id` | `INT` | `FOREIGN KEY (daily_menu.id)` | 每日菜单ID |
| `dish_id` | `INT` | `FOREIGN KEY (dish.id)` | 菜品ID |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

#### 3.1.10 客户模型 (`customer`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 客户ID |
| `name` | `VARCHAR(100)` | `NOT NULL` | 客户姓名 |
| `phone` | `VARCHAR(20)` | `NOT NULL` | 手机号 |
| `email` | `VARCHAR(100)` | | 邮箱 |
| `address` | `TEXT` | | 地址 |
| `dietary_restrictions` | `JSON` | | 饮食禁忌 |
| `preferences` | `JSON` | | 饮食偏好 |
| `is_active` | `BOOLEAN` | `DEFAULT TRUE` | 是否激活 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.11 订单模型 (`customer_order`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 订单ID |
| `customer_id` | `INT` | `FOREIGN KEY (customer.id)` | 客户ID |
| `order_date` | `DATE` | `NOT NULL` | 订单日期 |
| `delivery_date` | `DATE` | `NOT NULL` | 配送日期 |
| `total_amount` | `DECIMAL(10,2)` | `NOT NULL` | 总金额 |
| `status` | `VARCHAR(20)` | `NOT NULL` | 订单状态（待处理、已确认、已完成、已取消） |
| `payment_status` | `VARCHAR(20)` | `NOT NULL` | 支付状态（未支付、已支付、部分支付） |
| `notes` | `TEXT` | | 备注 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.12 订单详情模型 (`order_item`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 订单详情ID |
| `order_id` | `INT` | `FOREIGN KEY (customer_order.id)` | 订单ID |
| `dish_id` | `INT` | `FOREIGN KEY (dish.id)` | 菜品ID |
| `quantity` | `INT` | `NOT NULL` | 数量 |
| `unit_price` | `DECIMAL(10,2)` | `NOT NULL` | 单价 |
| `subtotal` | `DECIMAL(10,2)` | `NOT NULL` | 小计 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

#### 3.1.13 食材模型 (`ingredient`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 食材ID |
| `name` | `VARCHAR(100)` | `NOT NULL` | 食材名称 |
| `description` | `TEXT` | | 食材描述 |
| `unit` | `VARCHAR(20)` | `NOT NULL` | 单位 |
| `stock_quantity` | `DECIMAL(10,2)` | `DEFAULT 0` | 库存数量 |
| `is_available` | `BOOLEAN` | `DEFAULT TRUE` | 是否可用 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 3.1.14 菜品食材关联模型 (`dish_ingredient`)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 关联ID |
| `dish_id` | `INT` | `FOREIGN KEY (dish.id)` | 菜品ID |
| `ingredient_id` | `INT` | `FOREIGN KEY (ingredient.id)` | 食材ID |
| `quantity` | `DECIMAL(10,2)` | `NOT NULL` | 用量 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

### 3.2 索引设计
- **用户表**：`username`、`email`、`phone` 字段添加唯一索引
- **菜品表**：`name` 字段添加索引，`category_id` 字段添加外键索引
- **菜单表**：`name` 字段添加索引
- **订单表**：`customer_id`、`order_date`、`delivery_date`、`status` 字段添加索引
- **客户表**：`name`、`phone` 字段添加索引
- **月子餐计划表**：`plan_number`、`customer_id`、`start_date`、`status` 字段添加索引
- **月子餐周计划表**：`meal_plan_id`、`week_number` 字段添加索引
- **月子餐日计划表**：`week_plan_id`、`day_number`、`date` 字段添加索引
- **健康记录表**：`customer_id`、`record_type`、`record_date` 字段添加索引
- **预约表**：`customer_id`、`service_type`、`appointment_date`、`status` 字段添加索引

### 3.3 数据库迁移
- 使用 Alembic 进行数据库迁移
- 维护迁移脚本，确保数据库结构变更的可追溯性
- 实现开发、测试、生产环境的数据库结构同步

## 4. API接口设计

### 4.1 认证接口

#### 4.1.1 登录
- **URL**：`/api/auth/login`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **响应**：
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "管理员",
      "roles": ["admin"],
      "color_theme": "#3498db"
    }
  }
  ```

#### 4.1.2 注册
- **URL**：`/api/auth/register`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "username": "newuser",
    "password": "password123",
    "email": "newuser@example.com",
    "full_name": "新用户"
  }
  ```
- **响应**：
  ```json
  {
    "id": 2,
    "username": "newuser",
    "email": "newuser@example.com",
    "full_name": "新用户"
  }
  ```

#### 4.1.3 刷新Token
- **URL**：`/api/auth/refresh`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <refresh_token>`
- **响应**：
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

#### 4.1.4 获取当前用户信息
- **URL**：`/api/auth/me`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "管理员",
    "roles": ["admin"],
    "color_theme": "#3498db"
  }
  ```

### 4.2 菜单接口

#### 4.2.1 获取菜单列表
- **URL**：`/api/menus`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **查询参数**：`page`、`per_page`、`menu_type`、`is_active`
- **响应**：
  ```json
  {
    "total": 10,
    "pages": 2,
    "current_page": 1,
    "data": [
      {
        "id": 1,
        "name": "基础菜单",
        "description": "标准基础菜单",
        "menu_type": "basic",
        "is_active": true,
        "dishes": [
          {
            "id": 1,
            "name": "宫保鸡丁",
            "price": 25.00
          }
        ]
      }
    ]
  }
  ```

#### 4.2.2 创建菜单
- **URL**：`/api/menus`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "name": "新菜单",
    "description": "新创建的菜单",
    "menu_type": "basic",
    "dish_ids": [1, 2, 3]
  }
  ```
- **响应**：
  ```json
  {
    "id": 2,
    "name": "新菜单",
    "description": "新创建的菜单",
    "menu_type": "basic",
    "is_active": true
  }
  ```

#### 4.2.3 获取每日菜单
- **URL**：`/api/daily-menus`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **查询参数**：`date`、`category_id`
- **响应**：
  ```json
  {
    "total": 3,
    "data": [
      {
        "id": 1,
        "menu_date": "2026-02-01",
        "category_id": 1,
        "category_name": "早餐",
        "dishes": [
          {
            "id": 1,
            "name": "豆浆",
            "price": 5.00
          }
        ]
      }
    ]
  }
  ```

### 4.3 菜品接口

#### 4.3.1 获取菜品列表
- **URL**：`/api/dishes`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **查询参数**：`page`、`per_page`、`category_id`、`is_available`
- **响应**：
  ```json
  {
    "total": 50,
    "pages": 5,
    "current_page": 1,
    "data": [
      {
        "id": 1,
        "name": "宫保鸡丁",
        "description": "经典川菜",
        "price": 25.00,
        "category_id": 2,
        "category_name": "午餐",
        "image_url": "http://example.com/images/dish1.jpg",
        "nutrition_info": {
          "calories": 350,
          "protein": 25,
          "carbohydrates": 30,
          "fat": 15
        },
        "is_available": true
      }
    ]
  }
  ```

#### 4.3.2 创建菜品
- **URL**：`/api/dishes`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "name": "鱼香肉丝",
    "description": "经典川菜",
    "price": 22.00,
    "category_id": 2,
    "nutrition_info": {
      "calories": 320,
      "protein": 20,
      "carbohydrates": 35,
      "fat": 12
    },
    "ingredients": [
      {
        "ingredient_id": 1,
        "quantity": 200
      }
    ]
  }
  ```
- **响应**：
  ```json
  {
    "id": 2,
    "name": "鱼香肉丝",
    "description": "经典川菜",
    "price": 22.00,
    "category_id": 2,
    "is_available": true
  }
  ```

#### 4.3.3 获取菜品详情
- **URL**：`/api/dishes/{id}`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "id": 1,
    "name": "宫保鸡丁",
    "description": "经典川菜",
    "price": 25.00,
    "category_id": 2,
    "category_name": "午餐",
    "image_url": "http://example.com/images/dish1.jpg",
    "nutrition_info": {
      "calories": 350,
      "protein": 25,
      "carbohydrates": 30,
      "fat": 15
    },
    "is_available": true,
    "ingredients": [
      {
        "id": 1,
        "name": "鸡肉",
        "quantity": 200,
        "unit": "g"
      }
    ],
    "created_at": "2026-02-01T10:00:00Z",
    "updated_at": "2026-02-01T10:00:00Z"
  }
  ```

### 4.4 客户接口

#### 4.4.1 获取客户列表
- **URL**：`/api/customers`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **查询参数**：`page`、`per_page`、`is_active`、`search`
- **响应**：
  ```json
  {
    "total": 100,
    "pages": 10,
    "current_page": 1,
    "data": [
      {
        "id": 1,
        "name": "张三",
        "phone": "13800138000",
        "email": "zhangsan@example.com",
        "address": "北京市朝阳区",
        "dietary_restrictions": ["辣椒", "海鲜"],
        "preferences": ["清淡", "素食"],
        "is_active": true
      }
    ]
  }
  ```

#### 4.4.2 创建客户
- **URL**：`/api/customers`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "name": "李四",
    "phone": "13900139000",
    "email": "lisi@example.com",
    "address": "上海市浦东新区",
    "dietary_restrictions": ["花生"],
    "preferences": ["川菜", "肉类"]
  }
  ```
- **响应**：
  ```json
  {
    "id": 2,
    "name": "李四",
    "phone": "13900139000",
    "email": "lisi@example.com",
    "address": "上海市浦东新区",
    "dietary_restrictions": ["花生"],
    "preferences": ["川菜", "肉类"],
    "is_active": true
  }
  ```

### 4.5 订单接口

#### 4.5.1 获取订单列表
- **URL**：`/api/orders`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **查询参数**：`page`、`per_page`、`status`、`customer_id`、`start_date`、`end_date`
- **响应**：
  ```json
  {
    "total": 50,
    "pages": 5,
    "current_page": 1,
    "data": [
      {
        "id": 1,
        "customer_id": 1,
        "customer_name": "张三",
        "order_date": "2026-02-01",
        "delivery_date": "2026-02-02",
        "total_amount": 125.00,
        "status": "completed",
        "payment_status": "paid",
        "items": [
          {
            "dish_id": 1,
            "dish_name": "宫保鸡丁",
            "quantity": 2,
            "unit_price": 25.00,
            "subtotal": 50.00
          }
        ]
      }
    ]
  }
  ```

#### 4.5.2 创建订单
- **URL**：`/api/orders`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "customer_id": 1,
    "delivery_date": "2026-02-03",
    "items": [
      {
        "dish_id": 1,
        "quantity": 2
      },
      {
        "dish_id": 2,
        "quantity": 1
      }
    ],
    "notes": "不要辣椒"
  }
  ```
- **响应**：
  ```json
  {
    "id": 2,
    "customer_id": 1,
    "customer_name": "张三",
    "order_date": "2026-02-01",
    "delivery_date": "2026-02-03",
    "total_amount": 72.00,
    "status": "pending",
    "payment_status": "unpaid",
    "notes": "不要辣椒"
  }
  ```

### 4.6 系统接口

#### 4.6.1 获取用户列表
- **URL**：`/api/users`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **查询参数**：`page`、`per_page`、`is_active`、`role`
- **响应**：
  ```json
  {
    "total": 20,
    "pages": 2,
    "current_page": 1,
    "data": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "管理员",
        "roles": ["admin"],
        "is_active": true,
        "is_superuser": true
      }
    ]
  }
  ```

#### 4.6.2 获取角色列表
- **URL**：`/api/roles`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "data": [
      {
        "id": 1,
        "name": "admin",
        "description": "管理员角色",
        "permissions": ["create", "read", "update", "delete"]
      }
    ]
  }
  ```

### 4.7 文件上传接口

#### 4.7.1 上传Excel文件
- **URL**：`/api/upload/excel`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：`multipart/form-data`，包含文件字段 `file`
- **响应**：
  ```json
  {
    "success": true,
    "message": "文件上传成功",
    "data": {
      "filename": "menu.xlsx",
      "file_path": "/uploads/menu.xlsx",
      "processed_data": {
        "total_rows": 10,
        "success_rows": 8,
        "failed_rows": 2
      }
    }
  }
  ```

### 4.8 母婴服务接口

#### 4.8.1 月子餐计划接口

##### 4.8.1.1 获取月子餐计划列表
- **URL**：`/api/confinement_meal_plans`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **查询参数**：`page`、`per_page`、`customer_id`、`status`、`start_date`、`end_date`
- **响应**：
  ```json
  {
    "total": 10,
    "pages": 2,
    "current_page": 1,
    "data": [
      {
        "id": 1,
        "plan_number": "CMP20260201001",
        "customer_id": 1,
        "customer_name": "张三",
        "start_date": "2026-02-01",
        "end_date": "2026-03-01",
        "total_days": 28,
        "total_weeks": 4,
        "meal_plan_type": "standard",
        "total_calories_per_day": 2500.00,
        "total_price": 12000.00,
        "final_price": 10800.00,
        "status": "active",
        "created_by": 1,
        "created_at": "2026-01-15T10:00:00Z"
      }
    ]
  }
  ```

##### 4.8.1.2 创建月子餐计划
- **URL**：`/api/confinement_meal_plans`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "customer_id": 1,
    "start_date": "2026-02-01",
    "end_date": "2026-03-01",
    "meal_plan_type": "standard",
    "total_calories_per_day": 2500.00,
    "notes": "标准月子餐计划"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "plan_number": "CMP20260201001",
    "customer_id": 1,
    "start_date": "2026-02-01",
    "end_date": "2026-03-01",
    "total_days": 28,
    "total_weeks": 4,
    "meal_plan_type": "standard",
    "total_calories_per_day": 2500.00,
    "total_price": 12000.00,
    "final_price": 10800.00,
    "status": "draft",
    "notes": "标准月子餐计划",
    "created_by": 1,
    "created_at": "2026-01-15T10:00:00Z"
  }
  ```

##### 4.8.1.3 获取月子餐计划详情
- **URL**：`/api/confinement_meal_plans/{id}`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "id": 1,
    "plan_number": "CMP20260201001",
    "customer_id": 1,
    "customer_name": "张三",
    "start_date": "2026-02-01",
    "end_date": "2026-03-01",
    "total_days": 28,
    "total_weeks": 4,
    "meal_plan_type": "standard",
    "total_calories_per_day": 2500.00,
    "total_price": 12000.00,
    "final_price": 10800.00,
    "status": "active",
    "notes": "标准月子餐计划",
    "created_by": 1,
    "created_at": "2026-01-15T10:00:00Z",
    "week_plans": [
      {
        "id": 1,
        "week_number": 1,
        "focus_area": "恶露排出",
        "nutrition_goals": {
          "protein": "high",
          "iron": "medium"
        },
        "day_plans": [
          {
            "id": 1,
            "day_number": 1,
            "date": "2026-02-01",
            "total_calories": 2400.00,
            "meal_items": [
              {
                "id": 1,
                "meal_type": "早餐",
                "dish_id": 1,
                "dish_name": "小米粥",
                "serving_time": "08:00",
                "calories": 300.00
              }
            ]
          }
        ]
      }
    ]
  }
  ```

#### 4.8.2 健康记录接口

##### 4.8.2.1 获取健康记录列表
- **URL**：`/api/health_records`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **查询参数**：`page`、`per_page`、`customer_id`、`record_type`、`record_date`
- **响应**：
  ```json
  {
    "total": 20,
    "pages": 2,
    "current_page": 1,
    "data": [
      {
        "id": 1,
        "customer_id": 1,
        "customer_name": "张三",
        "record_type": "血压",
        "record_date": "2026-02-01",
        "health_data": {
          "systolic": 120,
          "diastolic": 80
        },
        "notes": "正常",
        "created_by": 1,
        "created_at": "2026-02-01T10:00:00Z"
      }
    ]
  }
  ```

##### 4.8.2.2 创建健康记录
- **URL**：`/api/health_records`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "customer_id": 1,
    "record_type": "血压",
    "record_date": "2026-02-01",
    "health_data": {
      "systolic": 120,
      "diastolic": 80
    },
    "notes": "正常"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "customer_id": 1,
    "record_type": "血压",
    "record_date": "2026-02-01",
    "health_data": {
      "systolic": 120,
      "diastolic": 80
    },
    "notes": "正常",
    "created_by": 1,
    "created_at": "2026-02-01T10:00:00Z"
  }
  ```

#### 4.8.3 预约接口

##### 4.8.3.1 获取预约列表
- **URL**：`/api/appointments`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **查询参数**：`page`、`per_page`、`customer_id`、`service_type`、`appointment_date`、`status`
- **响应**：
  ```json
  {
    "total": 15,
    "pages": 2,
    "current_page": 1,
    "data": [
      {
        "id": 1,
        "customer_id": 1,
        "customer_name": "张三",
        "service_type": "产后检查",
        "appointment_date": "2026-02-15",
        "appointment_time": "10:00",
        "status": "confirmed",
        "notes": "常规产后检查",
        "created_by": 1,
        "created_at": "2026-02-01T10:00:00Z"
      }
    ]
  }
  ```

##### 4.8.3.2 创建预约
- **URL**：`/api/appointments`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "customer_id": 1,
    "service_type": "产后检查",
    "appointment_date": "2026-02-15",
    "appointment_time": "10:00",
    "notes": "常规产后检查"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "customer_id": 1,
    "service_type": "产后检查",
    "appointment_date": "2026-02-15",
    "appointment_time": "10:00",
    "status": "pending",
    "notes": "常规产后检查",
    "created_by": 1,
    "created_at": "2026-02-01T10:00:00Z"
  }
  ```

#### 4.8.4 月子餐外卖接口

##### 4.8.4.1 创建月子餐外卖订单
- **URL**：`/api/confinement_meal/takeaway`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "customer_id": 1,
    "delivery_date": "2026-02-01",
    "items": [
      {
        "dish_id": 1,
        "quantity": 1
      },
      {
        "dish_id": 2,
        "quantity": 1
      }
    ],
    "delivery_address": "北京市朝阳区",
    "contact_phone": "13800138000",
    "notes": "不要辣椒"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "order_number": "CTO20260201001",
    "customer_id": 1,
    "customer_name": "张三",
    "delivery_date": "2026-02-01",
    "total_amount": 150.00,
    "status": "pending",
    "delivery_address": "北京市朝阳区",
    "contact_phone": "13800138000",
    "notes": "不要辣椒",
    "created_by": 1,
    "created_at": "2026-01-31T10:00:00Z"
  }
  ```

## 5. 业务逻辑实现

### 5.1 认证与授权
- **JWT认证**：实现基于JWT的认证机制，支持token刷新
- **角色权限**：实现基于角色的权限控制（RBAC）
- **权限验证**：实现细粒度的权限验证，控制API访问
- **密码安全**：使用Passlib进行密码哈希，支持密码强度验证

### 5.2 菜单管理
- **菜单创建**：支持创建不同类型的菜单，关联菜品
- **菜单编辑**：支持修改菜单信息和关联菜品
- **菜单状态管理**：支持启用/禁用菜单
- **每日菜单生成**：支持基于基础菜单生成每日菜单
- **Excel导入**：支持通过Excel文件批量导入菜单数据

### 5.3 菜品管理
- **菜品创建**：支持创建菜品，设置基本信息、价格、分类等
- **食材管理**：支持管理菜品的食材组成
- **营养分析**：支持计算和存储菜品的营养成分
- **菜品状态管理**：支持启用/禁用菜品
- **图片上传**：支持上传菜品图片

### 5.4 客户管理
- **客户信息管理**：支持客户信息的增删改查
- **饮食偏好管理**：支持记录客户的饮食禁忌和偏好
- **客户状态管理**：支持启用/禁用客户
- **批量导入**：支持通过Excel文件批量导入客户数据

### 5.5 订单管理
- **订单创建**：支持创建订单，选择客户、菜品和数量
- **订单状态更新**：支持更新订单状态和支付状态
- **订单查询**：支持多条件查询订单
- **订单统计**：支持订单数据的统计和分析
- **订单导出**：支持导出订单数据为Excel文件

### 5.6 系统管理
- **用户管理**：支持用户的增删改查，分配角色
- **角色管理**：支持角色的增删改查，分配权限
- **权限管理**：支持权限的定义和管理
- **系统配置**：支持系统参数的配置和管理
- **数据备份**：支持数据库的备份和恢复

### 5.7 母婴服务
- **月子餐计划管理**：支持创建、编辑、删除月子餐计划，包含周计划和日计划管理
- **健康记录管理**：支持记录和管理母婴健康数据，包括血压、体重、体温等
- **预约管理**：支持服务项目预约，包括产后检查、新生儿护理等
- **月子餐外卖**：支持创建和管理月子餐外卖订单
- **营养分析**：支持分析月子餐的营养成分，生成营养报告

### 5.8 数据处理
- **Excel处理**：使用Pandas处理Excel文件，支持导入导出
- **数据验证**：实现数据的有效性验证，确保数据质量
- **数据转换**：实现不同数据格式之间的转换
- **异常处理**：实现统一的异常处理机制

### 5.8 缓存策略
- **用户会话**：使用Redis缓存用户会话和权限信息
- **菜单数据**：缓存常用的菜单和菜品数据
- **统计数据**：缓存仪表盘和报表的统计数据
- **缓存过期**：合理设置缓存过期时间，确保数据一致性

## 6. 性能优化

### 6.1 数据库优化
- **查询优化**：优化SQL查询，减少数据库负载
- **索引优化**：合理创建索引，提高查询速度
- **连接池**：使用数据库连接池，减少连接开销
- **批量操作**：使用批量插入和更新，减少数据库操作次数

### 6.2 API优化
- **响应缓存**：缓存API响应，减少重复计算
- **分页处理**：实现合理的分页机制，避免返回大量数据
- **异步处理**：对耗时操作使用异步处理，提高API响应速度
- **压缩传输**：启用HTTP压缩，减少数据传输量

### 6.3 代码优化
- **模块化设计**：采用模块化设计，提高代码复用性
- **惰性加载**：使用惰性加载，减少初始化时间
- **内存管理**：优化内存使用，避免内存泄漏
- **并发处理**：优化并发请求处理，提高系统吞吐量

### 6.4 部署优化
- **负载均衡**：使用负载均衡，分散系统负载
- **水平扩展**：支持水平扩展，提高系统容量
- **容器化**：使用Docker容器化部署，提高部署一致性
- **自动化部署**：实现自动化部署流程，减少人工干预

## 7. 安全性

### 7.1 认证安全
- **JWT安全**：使用强密钥，设置合理的过期时间
- **密码安全**：使用强哈希算法，定期要求密码更新
- **多因素认证**：支持多因素认证，提高账户安全性

### 7.2 授权安全
- **最小权限**：实现最小权限原则，只授予必要的权限
- **权限审计**：记录权限变更和使用情况，便于审计
- **权限隔离**：不同角色之间的权限隔离，防止越权访问

### 7.3 数据安全
- **数据加密**：对敏感数据进行加密存储
- **传输安全**：使用HTTPS，确保数据传输安全
- **数据备份**：定期备份数据，确保数据安全
- **数据脱敏**：在非生产环境中对敏感数据进行脱敏

### 7.4 API安全
- **请求验证**：验证所有API请求的合法性
- **速率限制**：对API请求进行速率限制，防止暴力攻击
- **CORS配置**：合理配置CORS，防止跨域攻击
- **CSRF保护**：实现CSRF保护，防止跨站请求伪造

### 7.5 系统安全
- **依赖安全**：定期更新依赖包，修复安全漏洞
- **日志安全**：确保日志中不包含敏感信息
- **错误处理**：不暴露详细的错误信息给客户端
- **安全扫描**：定期进行安全扫描，发现和修复安全问题

## 8. 开发流程

### 8.1 开发环境
- **环境配置**：使用Docker Compose配置开发环境
- **依赖管理**：使用Pipenv或requirements.txt管理依赖
- **代码规范**：使用Flake8和Black保持代码规范
- **类型提示**：使用MyPy进行类型检查

### 8.2 测试
- **单元测试**：使用pytest进行单元测试
- **集成测试**：测试API接口和数据库操作
- **端到端测试**：测试完整的业务流程
- **测试覆盖率**：确保测试覆盖率达到80%以上

### 8.3 数据库迁移
- **Alembic配置**：使用Alembic进行数据库迁移
- **迁移脚本**：维护清晰的迁移脚本，记录数据库变更
- **环境同步**：确保开发、测试、生产环境的数据库结构一致

### 8.4 部署
- **CI/CD**：配置CI/CD流水线，自动构建和部署
- **环境分离**：明确分离开发、测试、生产环境
- **部署脚本**：编写自动化部署脚本，减少人工干预
- **回滚机制**：实现部署回滚机制，确保系统稳定性

### 8.5 监控与日志
- **日志管理**：使用结构化日志，便于分析和监控
- **性能监控**：监控系统性能指标，及时发现问题
- **错误监控**：监控系统错误，及时告警
- **业务监控**：监控关键业务指标，确保业务正常运行

## 9. 实施计划

### 9.1 第一阶段：基础架构搭建
- 搭建Flask项目框架
- 配置数据库连接和ORM
- 实现认证授权机制
- 创建基础目录结构

### 9.2 第二阶段：核心功能开发
- 实现用户管理和权限控制
- 开发菜单管理模块
- 开发菜品管理模块
- 开发客户管理模块

### 9.3 第三阶段：功能完善
- 开发订单管理模块
- 实现Excel导入导出功能
- 开发系统管理模块
- 实现数据统计和分析

### 9.4 第四阶段：测试和优化
- 编写单元测试和集成测试
- 进行性能测试和优化
- 进行安全测试和加固
- 优化用户体验

### 9.5 第五阶段：部署和上线
- 配置生产环境
- 实现CI/CD流水线
- 进行系统上线
- 建立监控和维护机制

## 10. 预期成果

- **完整的后端系统**：实现所有核心功能的后端系统
- **RESTful API**：设计规范、功能完善的RESTful API
- **数据库设计**：结构合理、性能优化的数据库设计
- **安全性**：安全可靠的认证授权和数据保护机制
- **性能**：高性能、可扩展的后端系统
- **可维护性**：代码规范、结构清晰、易于维护

## 11. 技术文档

### 11.1 API文档
- 使用Flask-RESTx生成Swagger UI文档
- 详细描述每个API的URL、方法、参数、响应等
- 提供API使用示例

### 11.2 数据库文档
- 详细描述数据库表结构、字段含义、索引设计等
- 提供数据库关系图
- 描述数据库迁移流程

### 11.3 开发文档
- 项目架构说明
- 技术选型理由
- 开发环境配置指南
- 代码规范和最佳实践

### 11.4 部署文档
- 生产环境配置指南
- 部署流程说明
- 监控和维护指南
- 故障排查手册

## 12. 风险评估

### 12.1 技术风险
- **依赖风险**：第三方库的兼容性和安全性风险
- **性能风险**：系统在高负载下的性能风险
- **安全风险**：系统可能面临的安全威胁

### 12.2 项目风险
- **需求变更**：需求变更可能导致开发计划调整
- **资源不足**：开发资源不足可能影响项目进度
- **技术难点**：某些功能的实现可能遇到技术难点

### 12.3 应对策略
- **依赖管理**：定期更新依赖，监控安全漏洞
- **性能测试**：提前进行性能测试，发现和解决性能问题
- **安全审计**：定期进行安全审计，发现和修复安全问题
- **需求管理**：建立规范的需求管理流程，控制需求变更
- **资源规划**：合理规划开发资源，确保项目进度
- **技术储备**：提前研究和解决可能的技术难点

## 13. 结论

本后端开发计划基于Flask框架，旨在构建一个功能完整、性能优秀、安全可靠的餐食管理系统后端。通过合理的技术选型、架构设计、数据库设计和API接口设计，确保系统的可扩展性、可维护性和安全性。通过分阶段的实施计划，确保项目的顺利进行和成功交付。