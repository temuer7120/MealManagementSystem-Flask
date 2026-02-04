# 餐饮管理系统

## 项目简介
餐饮管理系统是一个完整的餐饮运营管理解决方案，包含食材管理、菜品管理、菜单管理、客户管理、订单管理、排餐管理等功能。

## 技术栈

### 后端
- Flask：Python Web框架
- SQLAlchemy：ORM数据库工具
- JWT：用户认证
- CORS：跨域资源共享
- Pandas：Excel文件解析

### 前端
- HTML/CSS/JavaScript：基础前端技术

### 微信小程序
- 原生微信小程序开发

## 项目结构

```
MealManagementSystem/
├── backend/           # 后端代码
│   ├── docs/          # 文档
│   ├── instance/      # 数据库文件
│   ├── uploads/       # 上传文件
│   ├── utils/         # 工具函数
│   ├── app.py         # 应用入口
│   ├── config.py      # 配置文件
│   ├── extensions.py  # 扩展初始化
│   ├── models.py      # 数据库模型
│   ├── routes.py      # API路由
│   └── requirements.txt # 依赖包
├── frontend/          # 前端代码
│   ├── index.html     # 首页
│   └── ui_design.html # UI设计
└── wechat-miniprogram/ # 微信小程序代码
    ├── images/        # 图片资源
    ├── pages/         # 页面
    ├── app.js         # 小程序入口
    └── app.json       # 小程序配置
```

## 功能模块

1. **用户管理**：用户注册、登录、权限控制
2. **食材管理**：食材的增删改查、库存管理
3. **菜品管理**：菜品的增删改查、食材组成管理
4. **菜单管理**：基础菜单、每日菜单的管理
5. **客户管理**：客户信息的管理、饮食禁忌记录
6. **订单管理**：客户订单的创建、查询、状态更新
7. **排餐管理**：排餐表的创建、菜品分配、状态跟踪
8. **Excel上传**：支持上传Excel文件导入菜单和排餐数据

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python -c "from app import app; with app.app_context(): from extensions import db; db.create_all()"
```

### 3. 启动服务

```bash
python app.py
```

服务将在 `http://127.0.0.1:5000` 启动。

## API文档

### 认证接口
- `POST /api/auth/register`：用户注册
- `POST /api/auth/login`：用户登录
- `GET /api/auth/me`：获取当前用户信息

### 食材接口
- `GET /api/ingredients`：获取所有食材
- `POST /api/ingredients`：创建新食材
- `GET /api/ingredients/<id>`：获取食材详情
- `PUT /api/ingredients/<id>`：更新食材信息
- `DELETE /api/ingredients/<id>`：删除食材

### 菜品接口
- `GET /api/dishes`：获取所有菜品
- `GET /api/dishes/<id>`：获取菜品详情
- `PUT /api/dishes/<id>`：更新菜品信息
- `GET /api/dishes/<id>/ingredients`：获取菜品的食材组成
- `POST /api/dishes/<id>/ingredients`：为菜品添加食材

### 菜单接口
- `GET /api/menus`：获取所有菜单
- `GET /api/menus/<id>`：获取菜单详情
- `GET /api/daily_menus`：获取每日菜单
- `GET /api/daily_menus/<id>`：获取每日菜单详情

### 客户接口
- `GET /api/customers`：获取所有客户
- `GET /api/customers/<id>`：获取客户详情
- `PUT /api/customers/<id>`：更新客户信息

### 订单接口
- `GET /api/orders`：获取所有订单
- `POST /api/orders`：创建新订单
- `GET /api/orders/<id>`：获取订单详情

### 排餐接口
- `GET /api/meal_schedules`：获取所有排餐表
- `POST /api/meal_schedules`：创建新排餐表
- `GET /api/meal_schedules/<id>`：获取排餐表详情
- `POST /api/meal_schedules/<id>/items`：为排餐表添加排餐项

### 工具接口
- `POST /api/upload/excel`：上传Excel文件
- `POST /api/init_db`：初始化数据库
- `POST /api/init_sample_data`：初始化模拟数据

### 服务管理接口
- `GET /api/service_categories`：获取所有服务分类
- `POST /api/service_categories`：创建新服务分类
- `GET /api/service_items`：获取所有服务项目
- `POST /api/service_items`：创建新服务项目
- `GET /api/service_records`：获取所有服务记录
- `POST /api/service_records`：创建新服务记录

### 月子餐管理接口
- `GET /api/confinement_meal_plans`：获取所有月子餐计划
- `POST /api/confinement_meal_plans`：创建新月子餐计划

### 送餐管理接口
- `GET /api/delivery_records`：获取所有送餐记录
- `POST /api/delivery_records`：创建新送餐记录

### AI数据分析接口
- `GET /api/ai_analysis_results`：获取所有AI分析结果
- `POST /api/ai_analysis_results`：创建新AI分析结果

### 查询和打印接口
- `GET /api/reports/customer_meals/<id>`：获取客户餐食记录报告
- `GET /api/reports/customer_services/<id>`：获取客户服务记录报告
- `GET /api/reports/staff_workload/<id>`：获取工作人员工作量报告

## 权限管理

系统采用基于角色的权限控制（RBAC），包含以下角色：

- `admin`：管理员，拥有所有权限
- `nutritionist`：营养师，负责菜品和菜单管理
- `chef`：厨师，负责食材和菜品管理
- `admin_staff`：行政人员，负责客户和订单管理
- `head_nurse`：护士长，负责客户管理
- `nurse`：护士，负责客户管理
- `caregiver`：护理员，负责客户管理
- `customer`：客户，只能查看信息
- `guest`：访客，只能查看信息

## 数据库设计

系统包含以下主要数据表：

- `menu_category`：菜单分类（早餐、午餐、晚餐）
- `dish`：菜品信息
- `menu`：菜单信息
- `menu_dish`：菜单与菜品的关联
- `daily_menu`：每日菜单
- `daily_menu_dish`：每日菜单与菜品的关联
- `customer`：客户信息
- `customer_menu`：客户与每日菜单的关联
- `ingredient`：食材信息
- `dish_ingredient`：菜品与食材的关联
- `customer_order`：客户订单
- `order_item`：订单详情
- `meal_schedule`：排餐表
- `meal_schedule_item`：排餐表详情
- `user`：用户信息

## 运行环境

- Python 3.7+
- MySQL/PostgreSQL（推荐生产环境）
- Flask 2.0+

## 部署说明

### 开发环境
1. 安装依赖：`pip install -r requirements.txt`
2. 配置环境变量：修改 `config.py` 中的配置项
3. 初始化数据库：运行 `python -c "from app import app; with app.app_context(): from extensions import db; db.create_all()"`
4. 启动服务：`python app.py`

### 生产环境
1. 安装依赖：`pip install -r requirements.txt`
2. 配置环境变量：设置 `FLASK_ENV=production`，修改 `config.py` 中的配置项
3. 初始化数据库：运行 `python -c "from app import app; with app.app_context(): from extensions import db; db.create_all()"`
4. 使用WSGI服务器启动：推荐使用Gunicorn或uWSGI

## 开发指南

### 添加新功能
1. 在 `models.py` 中添加数据库模型
2. 在 `routes.py` 中添加API路由
3. 在 `utils/security.py` 中配置权限
4. 运行测试确保功能正常

### 代码规范
- 使用PEP 8编码规范
- 为所有函数和方法添加文档字符串
- 使用类型提示增强代码可读性
- 遵循RESTful API设计原则

### 测试策略
- 单元测试：测试单个函数和方法
- 集成测试：测试API接口和数据库操作
- 端到端测试：测试完整的用户流程

## 系统改进计划

### 架构优化
1. **前端架构升级**：使用Vue.js或React重构前端，提升用户体验
2. **微服务架构**：将系统拆分为多个微服务，提高可扩展性
3. **容器化部署**：使用Docker容器化应用，简化部署和扩展

### 安全性改进
1. **JWT安全增强**：使用环境变量存储密钥，实现token刷新机制
2. **密码策略优化**：实现强密码策略，支持密码复杂度验证
3. **API安全加固**：添加请求速率限制，防止暴力攻击
4. **数据加密**：对敏感数据进行加密存储

### 数据库优化
1. **数据库迁移**：添加Alembic数据库迁移支持
2. **索引优化**：优化数据库索引，提高查询性能
3. **数据备份**：实现自动数据备份和恢复机制
4. **缓存策略**：添加Redis缓存，减少数据库查询

### 功能完善
1. **报表生成**：添加数据报表生成功能
2. **通知系统**：实现邮件和短信通知功能
3. **批量操作**：支持批量导入和导出数据
4. **移动端适配**：优化微信小程序功能

### 性能优化
1. **代码优化**：优化关键路径代码，减少响应时间
2. **数据库查询优化**：优化复杂查询，减少数据库负载
3. **静态资源优化**：压缩和缓存静态资源
4. **并发处理**：优化并发请求处理

### 开发流程改进
1. **CI/CD集成**：配置持续集成和持续部署流程
2. **代码审查**：建立代码审查机制，提高代码质量
3. **测试覆盖率**：提高测试覆盖率，确保系统稳定性
4. **文档完善**：完善API文档和开发文档

### 部署优化
1. **负载均衡**：配置负载均衡，提高系统可用性
2. **监控系统**：添加系统监控和告警机制
3. **日志管理**：实现集中式日志管理
4. **灾备方案**：制定系统灾备方案

## 测试账户

系统初始化后，可以使用以下测试账户登录：

- 管理员：admin/admin123
- 营养师：nutritionist/nutritionist123
- 厨师：chef/chef123
- 客户：customer/customer123

## 许可证

MIT License
```