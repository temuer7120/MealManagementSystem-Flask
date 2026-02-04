# 餐食管理系统部署指南

## 1. 系统要求

### 1.1 硬件要求
- **CPU**：至少2核
- **内存**：至少2GB
- **存储空间**：至少10GB

### 1.2 软件要求
- **操作系统**：Windows、macOS或Linux
- **Python**：3.9或更高版本
- **数据库**：MySQL
- **Redis**：6.0或更高版本（用于缓存，可选）

## 2. 环境配置

### 2.1 安装Python

请从 [Python官方网站](https://www.python.org/downloads/) 下载并安装Python 3.9或更高版本。

### 2.2 安装依赖

在项目根目录下运行以下命令安装依赖：

```bash
# 创建虚拟环境（可选）
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2.3 配置环境变量

在项目根目录下创建 `.env` 文件，根据 `.env.example` 模板配置环境变量：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://root:MySQL@localhost:3306/meal_management

# JWT配置
JWT_SECRET_KEY=your-secret-key-here

# 上传文件配置
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=xlsx,xls

# CORS配置
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 缓存配置
CACHE_TYPE=simple  # 可选：simple, redis
CACHE_REDIS_URL=redis://localhost:6379/0
```

## 3. 数据库初始化

### 3.1 创建数据库表

运行以下命令初始化数据库：

```bash
python init_db.py
```

### 3.2 创建测试用户

运行以下命令创建测试用户：

```bash
python create_test_users.py
```

创建的测试用户包括：
- `admin` / `admin123`（系统管理员）
- `nutritionist` / `nutr123`（营养师）
- `chef` / `chef123`（厨师）
- `user` / `user123`（普通用户）
- `guest` / `guest123`（访客）

## 4. 运行系统

### 4.1 开发模式运行

```bash
python app.py
```

系统将在 `http://localhost:5000` 启动。

### 4.2 生产模式运行

使用 Gunicorn 等 WSGI 服务器运行：

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 5. 容器化部署

### 5.1 Docker 部署

#### 5.1.1 构建镜像

在项目根目录下运行：

```bash
docker build -t meal-management-system .
```

#### 5.1.2 运行容器

```bash
docker run -d \
  --name meal-management-system \
  -p 5000:5000 \
  -v ./uploads:/app/uploads \
  -e JWT_SECRET_KEY=your-secret-key-here \
  -e CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000 \
  meal-management-system
```

### 5.2 Docker Compose 部署

使用 `docker-compose.yml` 文件部署：

```bash
docker-compose up -d
```

## 6. 监控与维护

### 6.1 系统监控

系统集成了 Prometheus 监控，可通过以下端点访问：
- **健康检查**：`http://localhost:5000/health`
- **监控指标**：`http://localhost:5000/metrics`

### 6.2 日志管理

系统日志位于以下位置：
- **应用日志**：控制台输出
- **Prometheus 指标**：通过 `/metrics` 端点访问

### 6.3 定期维护

1. **数据库备份**：定期备份 `meal_management.db` 文件
2. **依赖更新**：定期更新项目依赖
3. **安全检查**：定期检查系统安全性，更新 JWT 密钥

## 7. 常见问题与解决方案

### 7.1 数据库连接问题

**症状**：系统启动时无法连接数据库

**解决方案**：
- 确保数据库文件路径正确
- 确保数据库文件有正确的读写权限
- 对于 MySQL 数据库，确保数据库服务正在运行

### 7.2 权限问题

**症状**：用户无法访问某些功能

**解决方案**：
- 检查用户角色是否正确
- 检查权限配置是否正确
- 运行 `create_test_users.py` 重新创建测试用户

### 7.3 文件上传问题

**症状**：无法上传 Excel 文件

**解决方案**：
- 确保 `uploads` 目录存在且有读写权限
- 确保文件类型和大小符合要求
- 检查用户是否有上传权限

### 7.4 缓存问题

**症状**：系统响应缓慢

**解决方案**：
- 确保 Redis 服务正在运行（如果使用 Redis 缓存）
- 检查缓存配置是否正确
- 对于生产环境，建议使用 Redis 缓存

## 8. 总结

本部署指南提供了餐食管理系统的详细部署步骤，包括环境配置、数据库初始化、部署方式和常见问题解决方案。通过按照本指南操作，可以快速部署和运行餐食管理系统，为餐饮运营提供高效的管理工具。

系统支持多种部署方式，包括传统部署和容器化部署，可以根据实际需求选择适合的部署方式。同时，系统集成了监控和日志功能，便于系统维护和问题排查。