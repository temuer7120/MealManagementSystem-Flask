from flask import Blueprint, request, jsonify
from extensions import db, jwt, cache
from models import MenuCategory, Dish, Menu, MenuDish, DailyMenu, DailyMenuDish, Customer, CustomerMenuSelection, User, Ingredient, DishIngredient, CustomerOrder, OrderItem, ServiceCategory, ServiceItem, ServiceBooking, ServiceFeedback, ConfinementMealPlan, ConfinementWeekPlan, ConfinementDayPlan, ConfinementMealItem, WeChatUser, CustomerWeChatLink, DeliverySchedule, DeliveryAssignment, DeliveryRoute, DeliveryStatusUpdate, AIAnalysisJob, AIAnalysisResult, ReportTemplate, GeneratedReport, AlertRule, Alert, Supplier, PurchaseOrder, PurchaseOrderItem, InventoryTransaction, InventoryAlert, IngredientCategory, CustomerDietaryPreference, Role, Permission, UserRole, RolePermission, ServicePackage, ServicePackageItem
import pandas as pd
import os
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.security import requires_permission, requires_resource_permission, validate_data, handle_error

api = Blueprint('api', __name__)

@api.route('/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    role_name = data.get('role', 'user')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    
    # 创建新用户
    user = User(username=username)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # 为用户分配角色
        if role_name:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                # 创建默认角色
                role = Role(name=role_name, description=f'{role_name} role')
                db.session.add(role)
                db.session.commit()
            
            # 创建用户角色关联
            user_role = UserRole(user_id=user.id, role_id=role.id)
            db.session.add(user_role)
            db.session.commit()
        
        return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 角色管理API
@api.route('/roles', methods=['GET'])
@requires_permission('role:read')
def get_roles():
    """获取所有角色"""
    roles = Role.query.all()
    return jsonify([{
        'id': role.id,
        'name': role.name,
        'description': role.description
    } for role in roles])

@api.route('/roles', methods=['POST'])
@requires_permission('role:create')
def create_role():
    """创建新角色"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查角色是否已存在
    existing_role = Role.query.filter_by(name=data['name']).first()
    if existing_role:
        return jsonify({'error': 'Role already exists'}), 400
    
    # 创建角色
    role = Role(
        name=data['name'],
        description=data.get('description')
    )
    
    try:
        db.session.add(role)
        db.session.commit()
        return jsonify({
            'id': role.id,
            'name': role.name,
            'description': role.description
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/roles/<int:role_id>', methods=['GET'])
@requires_permission('role:read')
def get_role_detail(role_id):
    """获取角色详情"""
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    
    # 获取角色的权限
    permissions = [{
        'id': rp.permission.id,
        'name': rp.permission.name,
        'code': rp.permission.code
    } for rp in role.role_permissions]
    
    return jsonify({
        'id': role.id,
        'name': role.name,
        'description': role.description,
        'permissions': permissions
    })

@api.route('/roles/<int:role_id>', methods=['PUT'])
@requires_permission('role:update')
def update_role(role_id):
    """更新角色信息"""
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查角色名称是否已被其他角色使用
    existing_role = Role.query.filter_by(name=data['name']).filter(Role.id != role_id).first()
    if existing_role:
        return jsonify({'error': 'Role name already exists'}), 400
    
    # 更新角色信息
    if 'name' in data:
        role.name = data['name']
    if 'description' in data:
        role.description = data['description']
    
    try:
        db.session.commit()
        return jsonify({
            'id': role.id,
            'name': role.name,
            'description': role.description
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/roles/<int:role_id>', methods=['DELETE'])
@requires_permission('role:delete')
def delete_role(role_id):
    """删除角色"""
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    
    # 检查是否有用户关联到该角色
    user_roles = UserRole.query.filter_by(role_id=role_id).first()
    if user_roles:
        return jsonify({'error': 'Cannot delete role with associated users'}), 400
    
    try:
        # 删除角色的权限关联
        RolePermission.query.filter_by(role_id=role_id).delete()
        # 删除角色
        db.session.delete(role)
        db.session.commit()
        return jsonify({'message': 'Role deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 权限管理API
@api.route('/permissions', methods=['GET'])
@requires_permission('permission:read')
def get_permissions():
    """获取所有权限"""
    permissions = Permission.query.all()
    return jsonify([{
        'id': permission.id,
        'name': permission.name,
        'code': permission.code,
        'module': permission.module,
        'description': permission.description
    } for permission in permissions])

@api.route('/permissions', methods=['POST'])
@requires_permission('permission:create')
def create_permission():
    """创建新权限"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name', 'code']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查权限是否已存在
    existing_permission = Permission.query.filter_by(code=data['code']).first()
    if existing_permission:
        return jsonify({'error': 'Permission already exists'}), 400
    
    # 创建权限
    permission = Permission(
        name=data['name'],
        code=data['code'],
        module=data.get('module'),
        description=data.get('description')
    )
    
    try:
        db.session.add(permission)
        db.session.commit()
        return jsonify({
            'id': permission.id,
            'name': permission.name,
            'code': permission.code,
            'module': permission.module,
            'description': permission.description
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/permissions/<int:permission_id>', methods=['GET'])
@requires_permission('permission:read')
def get_permission_detail(permission_id):
    """获取权限详情"""
    permission = Permission.query.get(permission_id)
    if not permission:
        return jsonify({'error': 'Permission not found'}), 404
    
    return jsonify({
        'id': permission.id,
        'name': permission.name,
        'code': permission.code,
        'module': permission.module,
        'description': permission.description
    })

@api.route('/permissions/<int:permission_id>', methods=['PUT'])
@requires_permission('permission:update')
def update_permission(permission_id):
    """更新权限信息"""
    permission = Permission.query.get(permission_id)
    if not permission:
        return jsonify({'error': 'Permission not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name', 'code']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查权限代码是否已被其他权限使用
    existing_permission = Permission.query.filter_by(code=data['code']).filter(Permission.id != permission_id).first()
    if existing_permission:
        return jsonify({'error': 'Permission code already exists'}), 400
    
    # 更新权限信息
    if 'name' in data:
        permission.name = data['name']
    if 'code' in data:
        permission.code = data['code']
    if 'module' in data:
        permission.module = data['module']
    if 'description' in data:
        permission.description = data['description']
    
    try:
        db.session.commit()
        return jsonify({
            'id': permission.id,
            'name': permission.name,
            'code': permission.code,
            'module': permission.module,
            'description': permission.description
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/permissions/<int:permission_id>', methods=['DELETE'])
@requires_permission('permission:delete')
def delete_permission(permission_id):
    """删除权限"""
    permission = Permission.query.get(permission_id)
    if not permission:
        return jsonify({'error': 'Permission not found'}), 404
    
    try:
        # 删除权限的角色关联
        RolePermission.query.filter_by(permission_id=permission_id).delete()
        # 删除权限
        db.session.delete(permission)
        db.session.commit()
        return jsonify({'message': 'Permission deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 用户角色管理API
@api.route('/users/<int:user_id>/roles', methods=['GET'])
@requires_permission('user:read')
def get_user_roles(user_id):
    """获取用户的角色"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # 获取用户的角色
    roles = [{
        'id': ur.role.id,
        'name': ur.role.name,
        'description': ur.role.description
    } for ur in user.user_roles]
    
    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'roles': roles
    })

@api.route('/users/<int:user_id>/roles', methods=['POST'])
@requires_permission('user:update')
def add_user_role(user_id):
    """为用户添加角色"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['role_id']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查角色是否存在
    role = Role.query.get(data['role_id'])
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    
    # 检查用户是否已拥有该角色
    existing_user_role = UserRole.query.filter_by(
        user_id=user_id,
        role_id=data['role_id']
    ).first()
    if existing_user_role:
        return jsonify({'error': 'User already has this role'}), 400
    
    # 为用户添加角色
    user_role = UserRole(
        user_id=user_id,
        role_id=data['role_id']
    )
    
    try:
        db.session.add(user_role)
        db.session.commit()
        return jsonify({
            'user_id': user.id,
            'username': user.username,
            'role_id': role.id,
            'role_name': role.name
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/users/<int:user_id>/roles/<int:role_id>', methods=['DELETE'])
@requires_permission('user:update')
def remove_user_role(user_id, role_id):
    """从用户移除角色"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # 检查角色是否存在
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    
    # 检查用户是否拥有该角色
    user_role = UserRole.query.filter_by(
        user_id=user_id,
        role_id=role_id
    ).first()
    if not user_role:
        return jsonify({'error': 'User does not have this role'}), 400
    
    try:
        db.session.delete(user_role)
        db.session.commit()
        return jsonify({'message': 'Role removed from user successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 角色权限管理API
@api.route('/roles/<int:role_id>/permissions', methods=['GET'])
@requires_permission('role:read')
def get_role_permissions(role_id):
    """获取角色的权限"""
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    
    # 获取角色的权限
    permissions = [{
        'id': rp.permission.id,
        'name': rp.permission.name,
        'code': rp.permission.code,
        'module': rp.permission.module
    } for rp in role.role_permissions]
    
    return jsonify({
        'role_id': role.id,
        'role_name': role.name,
        'permissions': permissions
    })

@api.route('/roles/<int:role_id>/permissions', methods=['POST'])
@requires_permission('role:update')
def add_role_permission(role_id):
    """为角色添加权限"""
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['permission_id']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查权限是否存在
    permission = Permission.query.get(data['permission_id'])
    if not permission:
        return jsonify({'error': 'Permission not found'}), 404
    
    # 检查角色是否已拥有该权限
    existing_role_permission = RolePermission.query.filter_by(
        role_id=role_id,
        permission_id=data['permission_id']
    ).first()
    if existing_role_permission:
        return jsonify({'error': 'Role already has this permission'}), 400
    
    # 为角色添加权限
    role_permission = RolePermission(
        role_id=role_id,
        permission_id=data['permission_id']
    )
    
    try:
        db.session.add(role_permission)
        db.session.commit()
        return jsonify({
            'role_id': role.id,
            'role_name': role.name,
            'permission_id': permission.id,
            'permission_name': permission.name,
            'permission_code': permission.code
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/roles/<int:role_id>/permissions/<int:permission_id>', methods=['DELETE'])
@requires_permission('role:update')
def remove_role_permission(role_id, permission_id):
    """从角色移除权限"""
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    
    # 检查权限是否存在
    permission = Permission.query.get(permission_id)
    if not permission:
        return jsonify({'error': 'Permission not found'}), 404
    
    # 检查角色是否拥有该权限
    role_permission = RolePermission.query.filter_by(
        role_id=role_id,
        permission_id=permission_id
    ).first()
    if not role_permission:
        return jsonify({'error': 'Role does not have this permission'}), 400
    
    try:
        db.session.delete(role_permission)
        db.session.commit()
        return jsonify({'message': 'Permission removed from role successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # 创建访问令牌
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
    }), 200

@api.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role
    }), 200

@api.route('/upload/excel', methods=['POST'])
@requires_resource_permission('upload', 'upload')
def upload_excel():
    """上传Excel文件并解析排餐表"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'Invalid file format'}), 400
    
    # 文件大小限制（10MB）
    file.seek(0, 2)  # 移动到文件末尾
    file_size = file.tell()  # 获取文件大小
    file.seek(0)  # 重置文件指针
    
    if file_size > 10 * 1024 * 1024:
        return jsonify({'error': 'File size exceeds 10MB limit'}), 400
    
    try:
        # 保存文件
        import config
        upload_folder = config.UPLOAD_FOLDER
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # 安全的文件名处理
        import uuid
        file_extension = os.path.splitext(file.filename)[1]
        safe_filename = f'excel_{uuid.uuid4().hex[:8]}_{datetime.now().strftime("%Y%m%d%H%M%S")}{file_extension}'
        filepath = os.path.join(upload_folder, safe_filename)
        file.save(filepath)
        
        # 文件内容验证（简单的Excel文件验证）
        try:
            import pandas as pd
            # 尝试读取文件，验证是否为有效的Excel文件
            pd.read_excel(filepath)
        except Exception as e:
            os.remove(filepath)  # 删除无效文件
            return jsonify({'error': 'Invalid Excel file content'}), 400
        
        # 解析文件（只解析每日厨房餐单，基础餐单改为导出）
        if '每日厨房餐单' in file.filename:
            parse_daily_kitchen_menu(filepath)
        
        return jsonify({'message': 'File uploaded and parsed successfully'}), 200
    except Exception as e:
        return handle_error(e)

@api.route('/upload/image', methods=['POST'])
def upload_image():
    """上传图片文件"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # 检查文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': 'Only image files are allowed'}), 400
        
        # 保存文件
        import os
        upload_folder = os.path.join(os.getcwd(), 'uploads', 'images')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        safe_filename = f"image_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        filepath = os.path.join(upload_folder, safe_filename)
        file.save(filepath)
        
        # 生成文件URL
        file_url = f"/uploads/images/{safe_filename}"
        
        return jsonify({'image_url': file_url}), 200
    except Exception as e:
        return handle_error(e)

@api.route('/ingredients/identify', methods=['POST'])
@requires_resource_permission('ingredient', 'create')
def identify_ingredient():
    """通过图片识别食材"""
    try:
        data = request.get_json()
        if not data or 'image_url' not in data:
            return jsonify({'error': 'No image URL provided'}), 400
        
        image_url = data['image_url']
        
        # 模拟AI识别结果（实际项目中应调用真实的AI识别服务）
        # 这里根据图片URL中的关键词进行简单的模拟识别
        import os
        filename = os.path.basename(image_url)
        
        # 模拟识别结果
        mock_results = {
            'tomato': {
                'name': '西红柿',
                'category': '蔬菜',
                'nutrition_info': {'蛋白质': '0.9g', '碳水化合物': '3.9g', '脂肪': '0.2g', '维生素C': '23mg'},
                'calories': 18,
                'features': '富含维生素C，酸甜可口',
                'taboo': '脾胃虚寒者不宜多食',
                'description': '常见的蔬菜，可生食或烹饪',
                'shelf_life_days': 7
            },
            'potato': {
                'name': '土豆',
                'category': '蔬菜',
                'nutrition_info': {'蛋白质': '2g', '碳水化合物': '17g', '脂肪': '0.1g', '膳食纤维': '2.2g'},
                'calories': 77,
                'features': '富含淀粉，用途广泛',
                'taboo': '发芽土豆有毒，不宜食用',
                'description': '常见的根茎类蔬菜，可制作多种菜肴',
                'shelf_life_days': 30
            },
            'chicken': {
                'name': '鸡肉',
                'category': '肉类',
                'nutrition_info': {'蛋白质': '20g', '碳水化合物': '0g', '脂肪': '5g', '维生素B6': '0.5mg'},
                'calories': 130,
                'features': '高蛋白低脂肪，营养丰富',
                'taboo': '感冒发热者不宜食用',
                'description': '常见的肉类食材，肉质鲜嫩',
                'shelf_life_days': 3
            },
            'fish': {
                'name': '鱼',
                'category': '海鲜',
                'nutrition_info': {'蛋白质': '22g', '碳水化合物': '0g', '脂肪': '3g', 'omega-3': '1g'},
                'calories': 120,
                'features': '富含omega-3脂肪酸，有益健康',
                'taboo': '痛风患者不宜食用',
                'description': '常见的海鲜食材，肉质鲜美',
                'shelf_life_days': 2
            }
        }
        
        # 默认识别结果
        result = {
            'name': '未知食材',
            'category': '其他',
            'nutrition_info': {},
            'calories': 0,
            'features': '',
            'taboo': '',
            'description': '',
            'shelf_life_days': 7
        }
        
        # 根据文件名关键词匹配识别结果
        for key, value in mock_results.items():
            if key in filename.lower():
                result = value
                break
        
        return jsonify(result), 200
    except Exception as e:
        return handle_error(e)

@api.route('/export/basic_menu', methods=['GET'])
@requires_resource_permission('menu', 'read')
def export_basic_menu():
    """导出基础餐单为Excel文件"""
    try:
        # 创建Excel文件
        from io import BytesIO
        import pandas as pd
        from flask import send_file
        
        # 创建工作簿
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        # 获取所有菜单分类
        categories = MenuCategory.query.all()
        
        # 获取所有菜单和菜品关联
        menu_dishes = MenuDish.query.all()
        
        # 创建基础餐单数据
        # 行：菜单分类 + 菜品
        # 列：周一到周日
        days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        
        # 构建数据结构
        data = []
        header = ['餐别'] + days
        data.append(['基础餐单'] + [''] * 7)  # 第一行：菜单名称
        data.append([''] + days)  # 第二行：星期
        
        # 为每个分类添加菜品
        for category in categories:
            # 添加分类行
            category_row = [category.name] + [''] * 7
            data.append(category_row)
            
            # 获取该分类下的所有菜品
            category_menu_dishes = [md for md in menu_dishes if md.category_id == category.id]
            
            # 按菜品分组
            dish_dict = {}
            for md in category_menu_dishes:
                dish_id = md.dish_id
                if dish_id not in dish_dict:
                    dish_dict[dish_id] = {'dish': md.dish, 'days': []}
                dish_dict[dish_id]['days'].append(md.day_of_week)
            
            # 添加每个菜品
            for dish_id, info in dish_dict.items():
                dish = info['dish']
                dish_row = [''] + [''] * 7
                # 填充菜品到对应日期
                for day_idx in info['days']:
                    if 1 <= day_idx <= 7:
                        dish_row[day_idx] = dish.name
                data.append(dish_row)
        
        # 创建DataFrame
        df = pd.DataFrame(data, columns=header)
        
        # 写入Excel
        df.to_excel(writer, sheet_name='基础餐单', index=False)
        
        # 保存工作簿
        writer.close()
        output.seek(0)
        
        # 发送文件
        return send_file(output, download_name='基础餐单.xlsx', as_attachment=True)
    except Exception as e:
        return handle_error(e)

# 提示阈值管理API
@api.route('/alert_thresholds', methods=['GET'])
@cache.cached(timeout=600, key_prefix='alert_thresholds')
def get_alert_thresholds():
    """获取所有提示阈值"""
    thresholds = AlertRule.query.all()
    return jsonify([{
        'id': threshold.id,
        'rule_name': threshold.rule_name,
        'rule_type': threshold.rule_type,
        'condition': threshold.condition,
        'severity': threshold.severity,
        'notification_channels': threshold.notification_channels,
        'is_active': threshold.is_active,
        'updated_at': threshold.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    } for threshold in thresholds])

@api.route('/alert_thresholds', methods=['POST'])
@requires_resource_permission('alert_threshold', 'create')
def create_alert_threshold():
    """创建新提示阈值"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['rule_name', 'rule_type', 'condition']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查阈值是否已存在
    existing_threshold = AlertRule.query.filter_by(rule_name=data['rule_name']).first()
    if existing_threshold:
        return jsonify({'error': 'Alert rule already exists with this name'}), 400
    
    # 创建阈值
    threshold = AlertRule(
        rule_name=data['rule_name'],
        rule_type=data['rule_type'],
        condition=data['condition'],
        severity=data.get('severity', 'warning'),
        notification_channels=data.get('notification_channels'),
        is_active=data.get('is_active', True)
    )
    
    try:
        db.session.add(threshold)
        db.session.commit()
        return jsonify({
            'id': threshold.id,
            'rule_name': threshold.rule_name,
            'rule_type': threshold.rule_type,
            'condition': threshold.condition,
            'severity': threshold.severity,
            'notification_channels': threshold.notification_channels,
            'is_active': threshold.is_active,
            'updated_at': threshold.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/alert_thresholds/<int:threshold_id>', methods=['PUT'])
@requires_resource_permission('alert_threshold', 'update')
def update_alert_threshold(threshold_id):
    """更新提示阈值"""
    threshold = AlertRule.query.get(threshold_id)
    if not threshold:
        return jsonify({'error': 'Alert threshold not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 更新阈值
    if 'rule_name' in data:
        # 检查新的规则名称是否已被其他规则使用
        existing_threshold = AlertRule.query.filter_by(rule_name=data['rule_name']).filter(AlertRule.id != threshold_id).first()
        if existing_threshold:
            return jsonify({'error': 'Alert rule already exists with this name'}), 400
        threshold.rule_name = data['rule_name']
    if 'rule_type' in data:
        threshold.rule_type = data['rule_type']
    if 'condition' in data:
        threshold.condition = data['condition']
    if 'severity' in data:
        threshold.severity = data['severity']
    if 'notification_channels' in data:
        threshold.notification_channels = data['notification_channels']
    if 'is_active' in data:
        threshold.is_active = data['is_active']
    
    try:
        db.session.commit()
        return jsonify({
            'id': threshold.id,
            'rule_name': threshold.rule_name,
            'rule_type': threshold.rule_type,
            'condition': threshold.condition,
            'severity': threshold.severity,
            'notification_channels': threshold.notification_channels,
            'is_active': threshold.is_active,
            'updated_at': threshold.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/alert_thresholds/<int:threshold_id>', methods=['DELETE'])
@requires_resource_permission('alert_threshold', 'delete')
def delete_alert_threshold(threshold_id):
    """删除提示阈值"""
    threshold = AlertRule.query.get(threshold_id)
    if not threshold:
        return jsonify({'error': 'Alert rule not found'}), 404
    
    try:
        db.session.delete(threshold)
        db.session.commit()
        return jsonify({'message': 'Alert rule deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 提示管理API
@api.route('/alerts', methods=['GET'])
@cache.cached(timeout=300, key_prefix='alerts')
def get_alerts():
    """获取所有提示"""
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    return jsonify([{
        'id': alert.id,
        'alert_code': alert.alert_code,
        'rule_id': alert.rule_id,
        'entity_type': alert.entity_type,
        'entity_id': alert.entity_id,
        'entity_name': alert.entity_name,
        'message': alert.message,
        'severity': alert.severity,
        'data': alert.data,
        'status': alert.status,
        'created_at': alert.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'resolved_at': alert.resolved_at.strftime('%Y-%m-%d %H:%M:%S') if alert.resolved_at else None,
        'resolved_by': alert.resolved_by,
        'resolution_notes': alert.resolution_notes,
        'acknowledged_at': alert.acknowledged_at.strftime('%Y-%m-%d %H:%M:%S') if alert.acknowledged_at else None,
        'acknowledged_by': alert.acknowledged_by
    } for alert in alerts])

@api.route('/alerts/<int:alert_id>', methods=['GET'])
def get_alert_detail(alert_id):
    """获取提示详情"""
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    return jsonify({
        'id': alert.id,
        'alert_code': alert.alert_code,
        'rule_id': alert.rule_id,
        'entity_type': alert.entity_type,
        'entity_id': alert.entity_id,
        'entity_name': alert.entity_name,
        'message': alert.message,
        'severity': alert.severity,
        'data': alert.data,
        'status': alert.status,
        'created_at': alert.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'resolved_at': alert.resolved_at.strftime('%Y-%m-%d %H:%M:%S') if alert.resolved_at else None,
        'resolved_by': alert.resolved_by,
        'resolution_notes': alert.resolution_notes,
        'acknowledged_at': alert.acknowledged_at.strftime('%Y-%m-%d %H:%M:%S') if alert.acknowledged_at else None,
        'acknowledged_by': alert.acknowledged_by
    })

@api.route('/alerts/<int:alert_id>', methods=['PUT'])
@requires_resource_permission('alert', 'update')
def update_alert(alert_id):
    """更新提示状态"""
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 更新状态
    if 'status' in data:
        alert.status = data['status']
        if data['status'] == 'resolved':
            alert.resolved_at = datetime.now()
            alert.resolved_by = data.get('resolved_by')
            alert.resolution_notes = data.get('resolution_notes')
        elif data['status'] == 'acknowledged':
            alert.acknowledged_at = datetime.now()
            alert.acknowledged_by = data.get('acknowledged_by')
    if 'severity' in data:
        alert.severity = data['severity']
    if 'data' in data:
        alert.data = data['data']
    
    try:
        db.session.commit()
        return jsonify({
            'id': alert.id,
            'alert_code': alert.alert_code,
            'rule_id': alert.rule_id,
            'entity_type': alert.entity_type,
            'entity_id': alert.entity_id,
            'entity_name': alert.entity_name,
            'message': alert.message,
            'severity': alert.severity,
            'data': alert.data,
            'status': alert.status,
            'created_at': alert.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'resolved_at': alert.resolved_at.strftime('%Y-%m-%d %H:%M:%S') if alert.resolved_at else None,
            'resolved_by': alert.resolved_by,
            'resolution_notes': alert.resolution_notes,
            'acknowledged_at': alert.acknowledged_at.strftime('%Y-%m-%d %H:%M:%S') if alert.acknowledged_at else None,
            'acknowledged_by': alert.acknowledged_by
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/alerts/<int:alert_id>', methods=['DELETE'])
@requires_resource_permission('alert', 'delete')
def delete_alert(alert_id):
    """删除提示"""
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    try:
        db.session.delete(alert)
        db.session.commit()
        return jsonify({'message': 'Alert deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 触发提示检查API
@api.route('/alerts/check', methods=['POST'])
@requires_permission('init')
def check_alerts():
    """检查并触发所有提示"""
    try:
        # 检查食材不足
        check_ingredient_shortage()
        # 检查客户退房
        check_customer_checkout()
        # 检查订单超时
        check_order_timeout()
        # 检查服务过期
        check_service_expired()
        # 检查排餐表待处理
        check_meal_schedule_pending()
        # 检查月子餐计划到期
        check_confinement_meal_expiring()
        # 检查配送延迟
        check_delivery_delay()
        
        return jsonify({'message': 'Alert check completed successfully'}), 200
    except Exception as e:
        return handle_error(e)

# 提示检查函数
def check_ingredient_shortage():
    """检查食材不足"""
    # 获取食材不足阈值
    threshold = AlertRule.query.filter_by(rule_type='ingredient').first()
    if not threshold:
        # 默认阈值
        threshold_value = 1000  # 默认1000克
    else:
        threshold_value = threshold.condition.get('threshold', 1000)
    
    # 检查所有食材
    ingredients = Ingredient.query.all()
    for ingredient in ingredients:
        if ingredient.current_stock < threshold_value:
            # 检查是否已存在未解决的提示
            existing_alert = Alert.query.filter_by(
                entity_type='ingredient',
                entity_id=ingredient.id,
                status='active'
            ).first()
            if not existing_alert:
                # 创建新提示
                import uuid
                alert_code = f'ING_{uuid.uuid4().hex[:8].upper()}'
                alert = Alert(
                    alert_code=alert_code,
                    rule_id=threshold.id if threshold else None,
                    entity_type='ingredient',
                    entity_id=ingredient.id,
                    entity_name=ingredient.name,
                    message=f'食材 {ingredient.name} 库存不足，当前库存: {ingredient.current_stock} {ingredient.unit_of_measure}',
                    severity='high',
                    data={
                        'current_stock': float(ingredient.current_stock),
                        'threshold': threshold_value,
                        'unit': ingredient.unit_of_measure
                    }
                )
                db.session.add(alert)
    db.session.commit()

def check_customer_checkout():
    """检查客户退房"""
    today = datetime.now().date()
    # 检查所有客户
    customers = Customer.query.all()
    for customer in customers:
        if customer.check_out_date and customer.check_out_date <= today:
            # 检查是否已存在未解决的提示
            existing_alert = Alert.query.filter_by(
                entity_type='customer',
                entity_id=customer.id,
                status='active'
            ).first()
            if not existing_alert:
                # 创建新提示
                import uuid
                alert_code = f'CUST_{uuid.uuid4().hex[:8].upper()}'
                alert = Alert(
                    alert_code=alert_code,
                    entity_type='customer',
                    entity_id=customer.id,
                    entity_name=customer.name,
                    message=f'客户 {customer.name} 今日退房',
                    severity='medium',
                    data={
                        'check_out_date': customer.check_out_date.isoformat(),
                        'name': customer.name
                    }
                )
                db.session.add(alert)
    db.session.commit()

def check_order_timeout():
    """检查订单超时"""
    # 获取订单超时阈值（小时）
    threshold = AlertRule.query.filter_by(rule_type='order').first()
    if not threshold:
        # 默认阈值
        threshold_hours = 24  # 默认24小时
    else:
        threshold_hours = threshold.condition.get('threshold', 24)
    
    # 检查所有待处理订单
    orders = CustomerOrder.query.filter_by(status='pending').all()
    for order in orders:
        # 计算订单时间差
        time_diff = datetime.now() - order.order_date
        if time_diff.total_seconds() / 3600 > threshold_hours:
            # 检查是否已存在未解决的提示
            existing_alert = Alert.query.filter_by(
                entity_type='order',
                entity_id=order.id,
                status='active'
            ).first()
            if not existing_alert:
                # 创建新提示
                import uuid
                alert_code = f'ORD_{uuid.uuid4().hex[:8].upper()}'
                alert = Alert(
                    alert_code=alert_code,
                    rule_id=threshold.id if threshold else None,
                    entity_type='order',
                    entity_id=order.id,
                    entity_name=f'订单 {order.order_number}',
                    message=f'订单 {order.order_number} 已超时 {threshold_hours} 小时未处理',
                    severity='medium',
                    data={
                        'order_number': order.order_number,
                        'order_date': order.order_date.isoformat(),
                        'threshold_hours': threshold_hours,
                        'time_elapsed_hours': time_diff.total_seconds() / 3600
                    }
                )
                db.session.add(alert)
    db.session.commit()

def check_service_expired():
    """检查服务过期"""
    # 获取服务过期阈值（天）
    threshold = AlertRule.query.filter_by(rule_type='service').first()
    if not threshold:
        # 默认阈值
        threshold_days = 7  # 默认7天
    else:
        threshold_days = threshold.condition.get('threshold', 7)
    
    # 检查所有服务记录
    services = ServiceBooking.query.all()
    for service in services:
        if service.start_time:
            # 计算服务时间差
            time_diff = datetime.now() - service.start_time
            if time_diff.days > threshold_days and service.status != 'completed':
                # 检查是否已存在未解决的提示
                existing_alert = Alert.query.filter_by(
                    entity_type='service',
                    entity_id=service.id,
                    status='active'
                ).first()
                if not existing_alert:
                    # 创建新提示
                    import uuid
                    alert_code = f'SRV_{uuid.uuid4().hex[:8].upper()}'
                    alert = Alert(
                        alert_code=alert_code,
                        rule_id=threshold.id if threshold else None,
                        entity_type='service',
                        entity_id=service.id,
                        entity_name=service.service_item.name if service.service_item else 'Unknown Service',
                        message=f'服务 {service.service_item.name if service.service_item else "Unknown Service"} 已超过 {threshold_days} 天未完成',
                        severity='low',
                        data={
                            'service_id': service.id,
                            'service_name': service.service_item.name if service.service_item else 'Unknown Service',
                            'start_time': service.start_time.isoformat(),
                            'threshold_days': threshold_days,
                            'time_elapsed_days': time_diff.days
                        }
                    )
                    db.session.add(alert)
    db.session.commit()

def check_meal_schedule_pending():
    """检查排餐表待处理"""
    today = datetime.now().date()
    # 检查所有待处理排餐表
    schedules = DeliverySchedule.query.filter_by(status='pending').all()
    for schedule in schedules:
        if schedule.date <= today:
            # 检查是否已存在未解决的提示
            existing_alert = Alert.query.filter_by(
                entity_type='delivery_schedule',
                entity_id=schedule.id,
                status='active'
            ).first()
            if not existing_alert:
                # 创建新提示
                import uuid
                alert_code = f'SCH_{uuid.uuid4().hex[:8].upper()}'
                alert = Alert(
                    alert_code=alert_code,
                    entity_type='delivery_schedule',
                    entity_id=schedule.id,
                    entity_name=f'排餐表 {schedule.date}',
                    message=f'排餐表 {schedule.date} 未发布',
                    severity='medium',
                    data={
                        'schedule_id': schedule.id,
                        'schedule_date': schedule.date.isoformat(),
                        'status': schedule.status
                    }
                )
                db.session.add(alert)
    db.session.commit()

def check_confinement_meal_expiring():
    """检查月子餐计划到期"""
    today = datetime.now().date()
    # 检查所有月子餐计划
    meal_plans = ConfinementMealPlan.query.all()
    for meal_plan in meal_plans:
        if meal_plan.end_date and meal_plan.end_date <= today + timedelta(days=3):
            # 检查是否已存在未解决的提示
            existing_alert = Alert.query.filter_by(
                entity_type='confinement_meal_plan',
                entity_id=meal_plan.id,
                status='active'
            ).first()
            if not existing_alert:
                # 创建新提示
                import uuid
                alert_code = f'CMP_{uuid.uuid4().hex[:8].upper()}'
                alert = Alert(
                    alert_code=alert_code,
                    entity_type='confinement_meal_plan',
                    entity_id=meal_plan.id,
                    entity_name=f'月子餐计划 {meal_plan.customer.name}',
                    message=f'月子餐计划 {meal_plan.customer.name} 将在 {meal_plan.end_date} 到期',
                    severity='medium',
                    data={
                        'meal_plan_id': meal_plan.id,
                        'meal_plan_number': meal_plan.plan_number,
                        'customer_name': meal_plan.customer.name,
                        'end_date': meal_plan.end_date.isoformat(),
                        'days_until_expiry': (meal_plan.end_date - today).days
                    }
                )
                db.session.add(alert)
    db.session.commit()

def check_delivery_delay():
    """检查配送延迟"""
    # 获取配送延迟阈值（分钟）
    threshold = AlertRule.query.filter_by(rule_type='delivery').first()
    if not threshold:
        # 默认阈值
        threshold_minutes = 30  # 默认30分钟
    else:
        threshold_minutes = threshold.condition.get('threshold', 30)
    
    # 检查所有配送记录
    deliveries = DeliveryAssignment.query.filter_by(status='in_progress').all()
    for delivery in deliveries:
        if delivery.actual_start_time:
            # 计算配送时间差
            time_diff = datetime.now() - delivery.actual_start_time
            if time_diff.total_seconds() / 60 > threshold_minutes:
                # 检查是否已存在未解决的提示
                existing_alert = Alert.query.filter_by(
                    entity_type='delivery_assignment',
                    entity_id=delivery.id,
                    status='active'
                ).first()
                if not existing_alert:
                    # 创建新提示
                    import uuid
                    alert_code = f'DEL_{uuid.uuid4().hex[:8].upper()}'
                    alert = Alert(
                        alert_code=alert_code,
                        rule_id=threshold.id if threshold else None,
                        entity_type='delivery_assignment',
                        entity_id=delivery.id,
                        entity_name=f'配送 {delivery.id}',
                        message=f'配送 {delivery.id} 已延迟超过 {threshold_minutes} 分钟',
                        severity='high',
                        data={
                            'delivery_id': delivery.id,
                            'start_time': delivery.actual_start_time.isoformat(),
                            'threshold_minutes': threshold_minutes,
                            'time_elapsed_minutes': time_diff.total_seconds() / 60
                        }
                    )
                    db.session.add(alert)
    db.session.commit()

# 图片上传识别API
@api.route('/image_recognition/id_card', methods=['POST'])
@requires_resource_permission('customer', 'update')
def recognize_id_card():
    """身份证图片识别"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        return jsonify({'error': 'Invalid file format'}), 400
    
    # 文件大小限制（5MB）
    file.seek(0, 2)  # 移动到文件末尾
    file_size = file.tell()  # 获取文件大小
    file.seek(0)  # 重置文件指针
    
    if file_size > 5 * 1024 * 1024:
        return jsonify({'error': 'File size exceeds 5MB limit'}), 400
    
    try:
        # 保存文件
        import config
        upload_folder = config.UPLOAD_FOLDER
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # 安全的文件名处理
        import uuid
        file_extension = os.path.splitext(file.filename)[1]
        safe_filename = f'id_card_{uuid.uuid4().hex[:8]}_{datetime.now().strftime("%Y%m%d%H%M%S")}{file_extension}'
        filepath = os.path.join(upload_folder, safe_filename)
        file.save(filepath)
        
        # 简单的图片文件验证
        try:
            from PIL import Image
            # 尝试打开文件，验证是否为有效的图片文件
            img = Image.open(filepath)
            img.verify()  # 验证图片文件的完整性
        except Exception as e:
            os.remove(filepath)  # 删除无效文件
            return jsonify({'error': 'Invalid image file content'}), 400
        
        # 模拟身份证识别结果
        # 实际项目中，这里应该调用OCR API进行身份证识别
        id_card_info = {
            'name': '张三',
            'id_number': '110101199001011234',
            'gender': '男',
            'birth_date': '1990-01-01',
            'address': '北京市朝阳区'
        }
        
        return jsonify({
            'message': 'ID card recognized successfully',
            'image_url': filepath,
            'id_card_info': id_card_info
        }), 200
    except Exception as e:
        return handle_error(e)

@api.route('/image_recognition/report', methods=['POST'])
@requires_resource_permission('admin_staff', 'create')
def recognize_report():
    """报表图片识别（发票、供货单、消费记录、出货单）"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        return jsonify({'error': 'Invalid file format'}), 400
    
    report_type = request.form.get('report_type', 'invoice')  # invoice, purchase_order, expense_record, delivery_order
    
    try:
        # 保存文件
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        filepath = os.path.join('uploads', 'report_' + report_type + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_' + file.filename)
        file.save(filepath)
        
        # 模拟报表识别结果
        # 实际项目中，这里应该调用OCR API进行报表识别
        if report_type == 'invoice':
            report_info = {
                'invoice_number': '202602020001',
                'date': '2026-02-02',
                'total_amount': 1234.56,
                'seller': '某某公司',
                'buyer': '月子中心'
            }
        elif report_type == 'purchase_order':
            report_info = {
                'order_number': 'PO202602020001',
                'date': '2026-02-02',
                'supplier': '某某供应商',
                'items': [
                    {'name': '食材1', 'quantity': 10, 'unit_price': 100, 'total': 1000},
                    {'name': '食材2', 'quantity': 5, 'unit_price': 50, 'total': 250}
                ],
                'total_amount': 1250
            }
        elif report_type == 'expense_record':
            report_info = {
                'record_number': 'ER202602020001',
                'date': '2026-02-02',
                'category': '食材采购',
                'amount': 1234.56,
                'payer': '管理员',
                'description': '采购食材'
            }
        elif report_type == 'delivery_order':
            report_info = {
                'order_number': 'DO202602020001',
                'date': '2026-02-02',
                'sender': '月子中心',
                'receiver': '客户1',
                'items': [
                    {'name': '月子餐', 'quantity': 3, 'unit': '份'},
                    {'name': '营养品', 'quantity': 1, 'unit': '盒'}
                ],
                'status': '已送达'
            }
        else:
            report_info = {
                'message': 'Unknown report type'
            }
        
        return jsonify({
            'message': report_type + ' recognized successfully',
            'image_url': filepath,
            'report_info': report_info
        }), 200
    except Exception as e:
        return handle_error(e)



def parse_daily_kitchen_menu(filepath):
    """解析每日厨房餐单Excel文件"""
    try:
        df = pd.read_excel(filepath)
        
        # 获取日期
        if len(df.columns) < 2:
            date = datetime.now().date()
        else:
            date_str = df.columns[1]
            try:
                date = pd.to_datetime(date_str).date()
            except:
                date = datetime.now().date()
        
        # 检查该日期的菜单是否已经存在
        daily_menu = DailyMenu.query.filter_by(date=date).first()
        if not daily_menu:
            # 创建每日菜单
            daily_menu = DailyMenu(date=date, description='厨房每日餐单')
            db.session.add(daily_menu)
            db.session.flush()
        else:
            # 如果已存在，删除该日期的所有菜品关联
            DailyMenuDish.query.filter_by(daily_menu_id=daily_menu.id).delete()
            CustomerMenuSelection.query.filter_by(daily_menu_id=daily_menu.id).delete()
            db.session.flush()
        
        # 解析客户信息和菜品
        if len(df.columns) > 1:
            for col_idx in range(1, len(df.columns)):
                try:
                    customer_name = df.iloc[0, col_idx]
                    if pd.isna(customer_name):
                        continue
                    
                    # 检查客户是否存在
                    customer = Customer.query.filter_by(name=customer_name.strip()).first()
                    if not customer:
                        customer = Customer(name=customer_name.strip())
                        db.session.add(customer)
                        db.session.flush()
                    
                    # 解析禁忌
                    if len(df) > 1:
                        restrictions = df.iloc[1, col_idx]
                        if not pd.isna(restrictions):
                            customer.dietary_restrictions = restrictions
                    
                    # 解析菜品
                    dish_row = 2
                    while dish_row < len(df):
                        try:
                            if pd.isna(df.iloc[dish_row, col_idx]):
                                break
                            dish_name = df.iloc[dish_row, col_idx]
                            if not pd.isna(dish_name):
                                # 检查菜品是否存在
                                dish = Dish.query.filter_by(name=dish_name.strip()).first()
                                if not dish:
                                    dish = Dish(name=dish_name.strip())
                                    db.session.add(dish)
                                    db.session.flush()
                                
                                # 添加到每日菜单
                                daily_menu_dish = DailyMenuDish(
                                    daily_menu_id=daily_menu.id,
                                    dish_id=dish.id,
                                    meal_type='lunch',  # 默认午餐
                                    category_id=1  # 默认分类
                                )
                                db.session.add(daily_menu_dish)
                            dish_row += 1
                        except Exception as e:
                            print(f"Error parsing dish at row {dish_row}, column {col_idx}: {str(e)}")
                            dish_row += 1
                            continue
                    
                    # 关联客户和每日菜单
                    customer_menu = CustomerMenuSelection(
                        customer_id=customer.id,
                        daily_menu_id=daily_menu.id,
                        selection_date=daily_menu.date,
                        meal_type='lunch'
                    )
                    db.session.add(customer_menu)
                except Exception as e:
                    print(f"Error parsing customer at column {col_idx}: {str(e)}")
                    continue
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error parsing daily kitchen menu: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

@api.route('/menus', methods=['GET'])
@cache.cached(timeout=600, key_prefix='menus')
def get_menus():
    """获取所有菜单"""
    menus = Menu.query.all()
    return jsonify([{
        'id': menu.id,
        'name': menu.name,
        'description': menu.description,
        'week_number': menu.week_number
    } for menu in menus])

@api.route('/menus', methods=['POST'])
@requires_resource_permission('menu', 'create')
def create_menu():
    """创建新菜单"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查菜单是否已存在
    existing_menu = Menu.query.filter_by(name=data['name']).first()
    if existing_menu:
        return jsonify({'error': 'Menu already exists'}), 400
    
    # 创建菜单
    menu = Menu(
        name=data['name'],
        description=data.get('description'),
        week_number=data.get('week_number'),
        year=data.get('year'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        status=data.get('status', 'draft')
    )
    
    try:
        db.session.add(menu)
        db.session.commit()
        return jsonify({
            'id': menu.id,
            'name': menu.name,
            'description': menu.description,
            'week_number': menu.week_number,
            'year': menu.year,
            'start_date': menu.start_date.strftime('%Y-%m-%d') if menu.start_date else None,
            'end_date': menu.end_date.strftime('%Y-%m-%d') if menu.end_date else None,
            'status': menu.status
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/menus/<int:menu_id>', methods=['PUT'])
@requires_resource_permission('menu', 'update')
def update_menu(menu_id):
    """更新菜单信息"""
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({'error': 'Menu not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 检查菜单名称是否已被其他菜单使用
    if 'name' in data:
        existing_menu = Menu.query.filter_by(name=data['name']).filter(Menu.id != menu_id).first()
        if existing_menu:
            return jsonify({'error': 'Menu name already exists'}), 400
        menu.name = data['name']
    
    # 更新其他字段
    if 'description' in data:
        menu.description = data['description']
    if 'week_number' in data:
        menu.week_number = data['week_number']
    if 'year' in data:
        menu.year = data['year']
    if 'start_date' in data:
        try:
            menu.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid start_date format'}), 400
    if 'end_date' in data:
        try:
            menu.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid end_date format'}), 400
    if 'status' in data:
        menu.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({
            'id': menu.id,
            'name': menu.name,
            'description': menu.description,
            'week_number': menu.week_number,
            'year': menu.year,
            'start_date': menu.start_date.strftime('%Y-%m-%d') if menu.start_date else None,
            'end_date': menu.end_date.strftime('%Y-%m-%d') if menu.end_date else None,
            'status': menu.status
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/menus/<int:menu_id>', methods=['DELETE'])
@requires_resource_permission('menu', 'delete')
def delete_menu(menu_id):
    """删除菜单"""
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({'error': 'Menu not found'}), 404
    
    try:
        # 删除菜单与菜品的关联
        MenuDish.query.filter_by(menu_id=menu_id).delete()
        # 删除菜单
        db.session.delete(menu)
        db.session.commit()
        return jsonify({'message': 'Menu deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/daily_menus', methods=['GET'])
def get_daily_menus():
    """获取每日菜单"""
    date = request.args.get('date')
    if date:
        cache_key = f'daily_menus_{date}'
        @cache.cached(timeout=300, key_prefix=cache_key)
        def get_daily_menu_by_date():
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            daily_menus = DailyMenu.query.filter_by(date=date_obj).all()
            return jsonify([{
                'id': menu.id,
                'date': menu.date.strftime('%Y-%m-%d'),
                'description': menu.description
            } for menu in daily_menus])
        return get_daily_menu_by_date()
    else:
        @cache.cached(timeout=300, key_prefix='daily_menus_all')
        def get_all_daily_menus():
            daily_menus = DailyMenu.query.all()
            return jsonify([{
                'id': menu.id,
                'date': menu.date.strftime('%Y-%m-%d'),
                'description': menu.description
            } for menu in daily_menus])
        return get_all_daily_menus()

@api.route('/customers', methods=['GET'])
def get_customers():
    """获取所有客户"""
    customers = Customer.query.all()
    return jsonify([{
        'id': customer.id,
        'name': customer.name,
        'dietary_restrictions': customer.dietary_restrictions,
        'check_in_date': customer.check_in_date.strftime('%Y-%m-%d') if customer.check_in_date else None,
        'check_out_date': customer.check_out_date.strftime('%Y-%m-%d') if customer.check_out_date else None
    } for customer in customers])

@api.route('/customers', methods=['POST'])
@requires_resource_permission('customer', 'create')
def create_customer():
    """创建新客户"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查客户是否已存在
    existing_customer = Customer.query.filter_by(name=data['name']).first()
    if existing_customer:
        return jsonify({'error': 'Customer already exists'}), 400
    
    # 创建客户
    customer = Customer(
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        date_of_birth=data.get('date_of_birth'),
        gender=data.get('gender'),
        height_cm=data.get('height_cm'),
        weight_kg=data.get('weight_kg'),
        check_in_date=data.get('check_in_date'),
        check_out_date=data.get('check_out_date'),
        id_card_number=data.get('id_card_number'),
        id_card_image_url=data.get('id_card_image_url'),
        physical_exam_report_url=data.get('physical_exam_report_url'),
        health_conditions=data.get('health_conditions'),
        dietary_restrictions=data.get('dietary_restrictions'),
        allergies=data.get('allergies'),
        preferred_foods=data.get('preferred_foods'),
        meal_plan_type=data.get('meal_plan_type'),
        status=data.get('status', 'active')
    )
    
    try:
        db.session.add(customer)
        db.session.commit()
        return jsonify({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'check_in_date': customer.check_in_date.strftime('%Y-%m-%d') if customer.check_in_date else None,
            'check_out_date': customer.check_out_date.strftime('%Y-%m-%d') if customer.check_out_date else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/dishes', methods=['GET'])
def get_dishes():
    """获取所有菜品"""
    dishes = Dish.query.all()
    return jsonify([{
        'id': dish.id,
        'name': dish.name,
        'ingredients': dish.ingredients,
        'dietary_restrictions': dish.dietary_restrictions,
        'category': dish.category.name if dish.category else None
    } for dish in dishes])

@api.route('/init_db', methods=['POST'])
def init_db():
    """初始化数据库"""
    try:
        db.create_all()
        return jsonify({'message': 'Database initialized successfully'}), 200
    except Exception as e:
        return handle_error(e)

@api.route('/menus/<int:menu_id>', methods=['GET'])
def get_menu_detail(menu_id):
    """获取菜单详情"""
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({'error': 'Menu not found'}), 404
    
    # 获取菜单中的菜品
    menu_dishes = MenuDish.query.filter_by(menu_id=menu_id).all()
    dishes_by_day = {}
    
    for md in menu_dishes:
        day = md.day_of_week
        if day not in dishes_by_day:
            dishes_by_day[day] = {}
        
        category = md.category.name if md.category else '未知'
        if category not in dishes_by_day[day]:
            dishes_by_day[day][category] = []
        
        dish = {
            'id': md.dish.id,
            'name': md.dish.name,
            'ingredients': md.dish.ingredients,
            'dietary_restrictions': md.dish.dietary_restrictions
        }
        dishes_by_day[day][category].append(dish)
    
    return jsonify({
        'id': menu.id,
        'name': menu.name,
        'description': menu.description,
        'week_number': menu.week_number,
        'dishes_by_day': dishes_by_day
    })

@api.route('/daily_menus/<int:menu_id>', methods=['GET'])
def get_daily_menu_detail(menu_id):
    """获取每日餐单详情"""
    daily_menu = DailyMenu.query.get(menu_id)
    if not daily_menu:
        return jsonify({'error': 'Daily menu not found'}), 404
    
    # 获取每日餐单中的菜品
    daily_menu_dishes = DailyMenuDish.query.filter_by(daily_menu_id=menu_id).all()
    dishes_by_category = {}
    
    for dmd in daily_menu_dishes:
        category = dmd.category.name if dmd.category else '未知'
        if category not in dishes_by_category:
            dishes_by_category[category] = []
        
        dish = {
            'id': dmd.dish.id,
            'name': dmd.dish.name,
            'ingredients': dmd.dish.ingredients,
            'dietary_restrictions': dmd.dish.dietary_restrictions
        }
        dishes_by_category[category].append(dish)
    
    # 获取关联的客户
    customer_menus = CustomerMenuSelection.query.filter_by(daily_menu_id=menu_id).all()
    customers = []
    
    for cm in customer_menus:
        customer = {
            'id': cm.customer.id,
            'name': cm.customer.name,
            'dietary_restrictions': cm.customer.dietary_restrictions
        }
        customers.append(customer)
    
    return jsonify({
        'id': daily_menu.id,
        'date': daily_menu.date.strftime('%Y-%m-%d'),
        'description': daily_menu.description,
        'dishes_by_category': dishes_by_category,
        'customers': customers
    })

@api.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer_detail(customer_id):
    """获取客户详情"""
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'dietary_restrictions': customer.dietary_restrictions,
        'check_in_date': customer.check_in_date.strftime('%Y-%m-%d') if customer.check_in_date else None,
        'check_out_date': customer.check_out_date.strftime('%Y-%m-%d') if customer.check_out_date else None
    })

@api.route('/customers/<int:customer_id>', methods=['PUT'])
@requires_resource_permission('customer', 'update')
def update_customer(customer_id):
    """更新客户信息"""
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 更新客户信息
    if 'name' in data:
        customer.name = data['name']
    if 'email' in data:
        customer.email = data['email']
    if 'phone' in data:
        customer.phone = data['phone']
    if 'date_of_birth' in data:
        customer.date_of_birth = data['date_of_birth']
    if 'gender' in data:
        customer.gender = data['gender']
    if 'height_cm' in data:
        customer.height_cm = data['height_cm']
    if 'weight_kg' in data:
        customer.weight_kg = data['weight_kg']
    if 'check_in_date' in data:
        try:
            customer.check_in_date = datetime.strptime(data['check_in_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid check_in_date format'}), 400
    if 'check_out_date' in data:
        try:
            customer.check_out_date = datetime.strptime(data['check_out_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid check_out_date format'}), 400
    if 'id_card_number' in data:
        customer.id_card_number = data['id_card_number']
    if 'id_card_image_url' in data:
        customer.id_card_image_url = data['id_card_image_url']
    if 'physical_exam_report_url' in data:
        customer.physical_exam_report_url = data['physical_exam_report_url']
    if 'health_conditions' in data:
        customer.health_conditions = data['health_conditions']
    if 'dietary_restrictions' in data:
        customer.dietary_restrictions = data['dietary_restrictions']
    if 'allergies' in data:
        customer.allergies = data['allergies']
    if 'preferred_foods' in data:
        customer.preferred_foods = data['preferred_foods']
    if 'meal_plan_type' in data:
        customer.meal_plan_type = data['meal_plan_type']
    if 'status' in data:
        customer.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'check_in_date': customer.check_in_date.strftime('%Y-%m-%d') if customer.check_in_date else None,
            'check_out_date': customer.check_out_date.strftime('%Y-%m-%d') if customer.check_out_date else None,
            'status': customer.status
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/customers/<int:customer_id>', methods=['DELETE'])
@requires_resource_permission('customer', 'delete')
def delete_customer(customer_id):
    """删除客户"""
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    try:
        # 删除客户相关的关联数据
        CustomerMenuSelection.query.filter_by(customer_id=customer_id).delete()
        CustomerOrder.query.filter_by(customer_id=customer_id).delete()
        DeliveryAssignment.query.filter_by(customer_id=customer_id).delete()
        CustomerDietaryPreference.query.filter_by(customer_id=customer_id).delete()
        
        # 删除客户
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish_detail(dish_id):
    """获取菜品详情"""
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    
    return jsonify({
        'id': dish.id,
        'name': dish.name,
        'ingredients': dish.ingredients,
        'dietary_restrictions': dish.dietary_restrictions,
        'category': dish.category.name if dish.category else None,
        'category_id': dish.category_id
    })

@api.route('/dishes/<int:dish_id>', methods=['PUT'])
@requires_resource_permission('dish', 'update')
def update_dish(dish_id):
    """更新菜品信息"""
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 更新菜品信息
    if 'name' in data:
        dish.name = data['name']
    if 'ingredients' in data:
        dish.ingredients = data['ingredients']
    if 'dietary_restrictions' in data:
        dish.dietary_restrictions = data['dietary_restrictions']
    if 'category_id' in data:
        # 验证分类是否存在
        from models import MenuCategory
        category = MenuCategory.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        dish.category_id = data['category_id']
    
    try:
        db.session.commit()
        return jsonify({
            'id': dish.id,
            'name': dish.name,
            'ingredients': dish.ingredients,
            'dietary_restrictions': dish.dietary_restrictions,
            'category': dish.category.name if dish.category else None,
            'category_id': dish.category_id
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/init_sample_data', methods=['POST'])
@requires_permission('init')
def init_sample_data():
    """初始化模拟数据"""
    try:
        # 创建菜单分类
        categories = ['早餐', '午餐', '晚餐']
        for cat_name in categories:
            category = MenuCategory.query.filter_by(name=cat_name).first()
            if not category:
                category = MenuCategory(name=cat_name)
                db.session.add(category)
        db.session.commit()
        
        # 创建菜品
        dishes = [
            {'name': '小米粥', 'category': '早餐'},
            {'name': '包子', 'category': '早餐'},
            {'name': '鸡蛋', 'category': '早餐'},
            {'name': '红烧肉', 'category': '午餐'},
            {'name': '鱼香肉丝', 'category': '午餐'},
            {'name': '米饭', 'category': '午餐'},
            {'name': '西红柿鸡蛋汤', 'category': '午餐'},
            {'name': '糖醋排骨', 'category': '晚餐'},
            {'name': '清炒时蔬', 'category': '晚餐'},
            {'name': '馒头', 'category': '晚餐'}
        ]
        
        for dish_data in dishes:
            dish = Dish.query.filter_by(name=dish_data['name']).first()
            if not dish:
                category = MenuCategory.query.filter_by(name=dish_data['category']).first()
                dish = Dish(name=dish_data['name'], category_id=category.id)
                db.session.add(dish)
        db.session.commit()
        
        # 创建菜单
        menu = Menu.query.filter_by(name='本周菜单').first()
        if not menu:
            menu = Menu(name='本周菜单', description='本周基础餐单')
            db.session.add(menu)
            db.session.flush()
            
            # 为每天添加菜品
            days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            for day_idx, day in enumerate(days):
                # 为每个分类添加菜品
                for category in MenuCategory.query.all():
                    # 随机选择该分类的两个菜品
                    category_dishes = Dish.query.filter_by(category_id=category.id).all()
                    if category_dishes:
                        for i in range(min(2, len(category_dishes))):
                            menu_dish = MenuDish(
                                menu_id=menu.id,
                                dish_id=category_dishes[i].id,
                                day_of_week=day_idx + 1,
                                category_id=category.id
                            )
                            db.session.add(menu_dish)
        db.session.commit()
        
        # 创建客户
        customers = [
            {'name': '张三', 'dietary_restrictions': '不吃辣'},
            {'name': '李四', 'dietary_restrictions': '海鲜过敏'},
            {'name': '王五', 'dietary_restrictions': '无'},
            {'name': '赵六', 'dietary_restrictions': '素食'}
        ]
        
        for customer_data in customers:
            customer = Customer.query.filter_by(name=customer_data['name']).first()
            if not customer:
                customer = Customer(
                    name=customer_data['name'],
                    dietary_restrictions=customer_data['dietary_restrictions'],
                    check_in_date=datetime.now().date(),
                    check_out_date=datetime.now().date() + timedelta(days=7)
                )
                db.session.add(customer)
        db.session.commit()
        
        # 创建每日菜单
        today = datetime.now().date()
        daily_menu = DailyMenu.query.filter_by(date=today).first()
        if not daily_menu:
            daily_menu = DailyMenu(date=today, description='今日厨房餐单')
            db.session.add(daily_menu)
            db.session.flush()
            
            # 添加菜品
            all_dishes = Dish.query.all()
            for i in range(min(6, len(all_dishes))):
                daily_menu_dish = DailyMenuDish(
                    daily_menu_id=daily_menu.id,
                    dish_id=all_dishes[i].id,
                    category_id=all_dishes[i].category_id
                )
                db.session.add(daily_menu_dish)
            
            # 关联客户
            all_customers = Customer.query.all()
            for customer in all_customers:
                customer_menu = CustomerMenuSelection(
                    customer_id=customer.id,
                    daily_menu_id=daily_menu.id,
                    selection_date=daily_menu.date,
                    meal_type='lunch'
                )
                db.session.add(customer_menu)
        db.session.commit()
        
        return jsonify({'message': 'Sample data initialized successfully'}), 200
    except Exception as e:
        return handle_error(e)

# 食材分类API
@api.route('/ingredient_categories', methods=['GET'])
def get_ingredient_categories():
    """获取所有食材分类"""
    categories = IngredientCategory.query.all()
    return jsonify([{
        'id': category.id,
        'name': category.name,
        'description': category.description
    } for category in categories])

@api.route('/ingredient_categories', methods=['POST'])
@requires_resource_permission('ingredient', 'create')
def create_ingredient_category():
    """创建新食材分类"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查分类是否已存在
    existing_category = IngredientCategory.query.filter_by(name=data['name']).first()
    if existing_category:
        return jsonify({'error': 'Ingredient category already exists'}), 400
    
    # 创建食材分类
    category = IngredientCategory(
        name=data['name'],
        description=data.get('description')
    )
    
    try:
        db.session.add(category)
        db.session.commit()
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 供应商管理API


@api.route('/suppliers', methods=['POST'])
@requires_resource_permission('supplier', 'create')
def create_supplier():
    """创建新供应商"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查供应商是否已存在
    existing_supplier = Supplier.query.filter_by(name=data['name']).first()
    if existing_supplier:
        return jsonify({'error': 'Supplier already exists'}), 400
    
    # 创建供应商
    supplier = Supplier(
        name=data['name'],
        contact_person=data.get('contact_person'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address'),
        description=data.get('description')
    )
    
    try:
        db.session.add(supplier)
        db.session.commit()
        return jsonify({
            'id': supplier.id,
            'name': supplier.name,
            'contact_person': supplier.contact_person,
            'phone': supplier.phone,
            'email': supplier.email,
            'address': supplier.address
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 食材相关API
@api.route('/ingredients', methods=['GET'])
def get_ingredients():
    """获取所有食材"""
    ingredients = Ingredient.query.all()
    return jsonify([{
        'id': ingredient.id,
        'name': ingredient.name,
        'description': ingredient.description,
        'current_stock': float(ingredient.current_stock),
        'unit_of_measure': ingredient.unit_of_measure,
        'category_id': ingredient.category_id,
        'category_name': ingredient.category.name if ingredient.category else None
    } for ingredient in ingredients])

@api.route('/ingredients', methods=['POST'])
def create_ingredient():
    """创建新食材"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查食材是否已存在
    existing_ingredient = Ingredient.query.filter_by(name=data['name']).first()
    if existing_ingredient:
        return jsonify({'error': 'Ingredient already exists'}), 400
    
    # 创建食材
    ingredient = Ingredient(
        name=data['name'],
        description=data.get('description'),
        current_stock=data.get('current_stock', 0),
        unit_of_measure=data.get('unit_of_measure', 'g'),
        category_id=data.get('category_id'),
        reorder_point=data.get('reorder_point', 0),
        supplier_id=data.get('supplier_id'),
        unit_cost=data.get('unit_cost'),
        calories_per_unit=data.get('calories_per_unit'),
        nutrition_info=data.get('nutrition_info'),
        shelf_life_days=data.get('shelf_life_days'),
        image_url=data.get('image_url')
    )
    
    try:
        db.session.add(ingredient)
        db.session.commit()
        return jsonify({
            'id': ingredient.id,
            'name': ingredient.name,
            'description': ingredient.description,
            'current_stock': float(ingredient.current_stock),
            'unit_of_measure': ingredient.unit_of_measure,
            'category_id': ingredient.category_id,
            'supplier_id': ingredient.supplier_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient_detail(ingredient_id):
    """获取食材详情"""
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    return jsonify({
        'id': ingredient.id,
        'name': ingredient.name,
        'description': ingredient.description,
        'current_stock': float(ingredient.current_stock),
        'unit_of_measure': ingredient.unit_of_measure,
        'category_id': ingredient.category_id,
        'category_name': ingredient.category.name if ingredient.category else None,
        'supplier_id': ingredient.supplier_id,
        'supplier_name': ingredient.supplier.name if ingredient.supplier else None,
        'reorder_point': ingredient.reorder_point
    })

@api.route('/ingredients/<int:ingredient_id>', methods=['PUT'])
@requires_resource_permission('ingredient', 'update')
def update_ingredient(ingredient_id):
    """更新食材信息"""
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    if 'name' in data:
        # 检查食材名称是否已被其他食材使用
        existing_ingredient = Ingredient.query.filter_by(name=data['name']).filter(Ingredient.id != ingredient_id).first()
        if existing_ingredient:
            return jsonify({'error': 'Ingredient name already exists'}), 400
        ingredient.name = data['name']
    
    # 更新其他字段
    if 'description' in data:
        ingredient.description = data['description']
    if 'current_stock' in data:
        ingredient.current_stock = data['current_stock']
    if 'unit_of_measure' in data:
        ingredient.unit_of_measure = data['unit_of_measure']
    if 'category_id' in data:
        ingredient.category_id = data['category_id']
    if 'supplier_id' in data:
        ingredient.supplier_id = data['supplier_id']
    if 'reorder_point' in data:
        ingredient.reorder_point = data['reorder_point']
    if 'unit_cost' in data:
        ingredient.unit_cost = data['unit_cost']
    if 'calories_per_unit' in data:
        ingredient.calories_per_unit = data['calories_per_unit']
    if 'nutrition_info' in data:
        ingredient.nutrition_info = data['nutrition_info']
    if 'shelf_life_days' in data:
        ingredient.shelf_life_days = data['shelf_life_days']
    if 'image_url' in data:
        ingredient.image_url = data['image_url']
    
    try:
        db.session.commit()
        return jsonify({
            'id': ingredient.id,
            'name': ingredient.name,
            'description': ingredient.description,
            'current_stock': float(ingredient.current_stock),
            'unit_of_measure': ingredient.unit_of_measure,
            'category_id': ingredient.category_id,
            'supplier_id': ingredient.supplier_id,
            'reorder_point': ingredient.reorder_point
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
@requires_resource_permission('ingredient', 'delete')
def delete_ingredient(ingredient_id):
    """删除食材"""
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    try:
        db.session.delete(ingredient)
        db.session.commit()
        return jsonify({'message': 'Ingredient deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 采购订单API
@api.route('/purchase_orders', methods=['GET'])
@requires_resource_permission('purchase_order', 'read')
def get_purchase_orders():
    """获取所有采购订单"""
    orders = PurchaseOrder.query.all()
    return jsonify([{
        'id': order.id,
        'order_number': order.order_number,
        'supplier_id': order.supplier_id,
        'supplier_name': order.supplier.name if order.supplier else None,
        'order_date': order.order_date.strftime('%Y-%m-%d'),
        'expected_delivery_date': order.expected_delivery_date.strftime('%Y-%m-%d') if order.expected_delivery_date else None,
        'status': order.status,
        'total_amount': order.total_amount
    } for order in orders])

@api.route('/purchase_orders', methods=['POST'])
@requires_resource_permission('purchase_order', 'create')
def create_purchase_order():
    """创建新采购订单"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['supplier_id', 'items']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查供应商是否存在
    supplier = Supplier.query.get(data['supplier_id'])
    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404
    
    # 生成订单号
    import uuid
    order_number = f'PO_{uuid.uuid4().hex[:8].upper()}_{datetime.now().strftime("%Y%m%d")}'
    
    # 创建采购订单
    order = PurchaseOrder(
        order_number=order_number,
        supplier_id=data['supplier_id'],
        order_date=data.get('order_date', datetime.now().date()),
        expected_delivery_date=data.get('expected_delivery_date'),
        status=data.get('status', 'pending'),
        total_amount=0  # 初始化为0，后续计算
    )
    
    try:
        db.session.add(order)
        db.session.flush()  # 获取order.id
        
        # 添加采购订单详情
        total_amount = 0
        for item_data in data['items']:
            # 验证订单详情数据
            item_required_fields = ['ingredient_id', 'quantity', 'unit_price']
            item_is_valid, item_error = validate_data(item_data, item_required_fields)
            if not item_is_valid:
                return jsonify(item_error), 400
            
            # 检查食材是否存在
            ingredient = Ingredient.query.get(item_data['ingredient_id'])
            if not ingredient:
                return jsonify({'error': f'Ingredient {item_data["ingredient_id"]} not found'}), 404
            
            # 创建采购订单详情
            order_item = PurchaseOrderItem(
                order_id=order.id,
                ingredient_id=item_data['ingredient_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                unit_of_measure=item_data.get('unit_of_measure', ingredient.unit_of_measure)
            )
            db.session.add(order_item)
            total_amount += order_item.unit_price * order_item.quantity
        
        # 更新订单总金额
        order.total_amount = total_amount
        
        db.session.commit()
        return jsonify({
            'id': order.id,
            'order_number': order.order_number,
            'supplier_id': order.supplier_id,
            'supplier_name': supplier.name,
            'order_date': order.order_date.strftime('%Y-%m-%d'),
            'expected_delivery_date': order.expected_delivery_date.strftime('%Y-%m-%d') if order.expected_delivery_date else None,
            'status': order.status,
            'total_amount': order.total_amount
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/purchase_orders/<int:order_id>', methods=['GET'])
@requires_resource_permission('purchase_order', 'read')
def get_purchase_order_detail(order_id):
    """获取采购订单详情"""
    order = PurchaseOrder.query.get(order_id)
    if not order:
        return jsonify({'error': 'Purchase order not found'}), 404
    
    # 获取采购订单详情
    order_items = PurchaseOrderItem.query.filter_by(order_id=order_id).all()
    items = [{
        'id': item.id,
        'ingredient_id': item.ingredient_id,
        'ingredient_name': item.ingredient.name,
        'quantity': item.quantity,
        'unit_price': item.unit_price,
        'unit_of_measure': item.unit_of_measure,
        'subtotal': item.unit_price * item.quantity
    } for item in order_items]
    
    return jsonify({
        'id': order.id,
        'order_number': order.order_number,
        'supplier_id': order.supplier_id,
        'supplier_name': order.supplier.name if order.supplier else None,
        'order_date': order.order_date.strftime('%Y-%m-%d'),
        'expected_delivery_date': order.expected_delivery_date.strftime('%Y-%m-%d') if order.expected_delivery_date else None,
        'status': order.status,
        'total_amount': order.total_amount,
        'items': items
    })

# 库存交易API
@api.route('/inventory_transactions', methods=['GET'])
@requires_resource_permission('inventory', 'read')
def get_inventory_transactions():
    """获取所有库存交易"""
    transactions = InventoryTransaction.query.order_by(InventoryTransaction.transaction_date.desc()).all()
    return jsonify([{
        'id': transaction.id,
        'transaction_type': transaction.transaction_type,
        'ingredient_id': transaction.ingredient_id,
        'ingredient_name': transaction.ingredient.name if transaction.ingredient else None,
        'quantity': transaction.quantity,
        'unit_of_measure': transaction.unit_of_measure,
        'transaction_date': transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
        'reference_id': transaction.reference_id,
        'reference_type': transaction.reference_type,
        'notes': transaction.notes
    } for transaction in transactions])

@api.route('/inventory_transactions', methods=['POST'])
@requires_resource_permission('inventory', 'create')
def create_inventory_transaction():
    """创建新库存交易"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['transaction_type', 'ingredient_id', 'quantity']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查食材是否存在
    ingredient = Ingredient.query.get(data['ingredient_id'])
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    # 创建库存交易
    transaction = InventoryTransaction(
        transaction_type=data['transaction_type'],
        ingredient_id=data['ingredient_id'],
        quantity=data['quantity'],
        unit_of_measure=data.get('unit_of_measure', ingredient.unit_of_measure),
        transaction_date=data.get('transaction_date', datetime.now()),
        reference_id=data.get('reference_id'),
        reference_type=data.get('reference_type'),
        notes=data.get('notes')
    )
    
    try:
        # 更新食材库存
        if data['transaction_type'] == 'in':
            ingredient.current_stock += data['quantity']
        elif data['transaction_type'] == 'out':
            if ingredient.current_stock < data['quantity']:
                return jsonify({'error': 'Insufficient stock'}), 400
            ingredient.current_stock -= data['quantity']
        
        db.session.add(transaction)
        db.session.commit()
        return jsonify({
            'id': transaction.id,
            'transaction_type': transaction.transaction_type,
            'ingredient_id': transaction.ingredient_id,
            'ingredient_name': ingredient.name,
            'quantity': transaction.quantity,
            'unit_of_measure': transaction.unit_of_measure,
            'transaction_date': transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'reference_id': transaction.reference_id,
            'reference_type': transaction.reference_type,
            'notes': transaction.notes,
            'new_stock_level': float(ingredient.current_stock)
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 菜品食材关联API
@api.route('/dishes/<int:dish_id>/ingredients', methods=['GET'])
def get_dish_ingredients(dish_id):
    """获取菜品的食材组成"""
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    
    dish_ingredients = DishIngredient.query.filter_by(dish_id=dish_id).all()
    return jsonify([{
        'id': di.id,
        'ingredient_id': di.ingredient_id,
        'ingredient_name': di.ingredient.name,
        'quantity_required': di.quantity_required,
        'unit_of_measure': di.unit_of_measure
    } for di in dish_ingredients])

@api.route('/dishes/<int:dish_id>/ingredients', methods=['POST'])
@requires_resource_permission('dish', 'update')
def add_dish_ingredient(dish_id):
    """为菜品添加食材"""
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['ingredient_id', 'quantity_required']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查食材是否存在
    ingredient = Ingredient.query.get(data['ingredient_id'])
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    # 检查菜品是否已添加该食材
    existing_dish_ingredient = DishIngredient.query.filter_by(
        dish_id=dish_id,
        ingredient_id=data['ingredient_id']
    ).first()
    if existing_dish_ingredient:
        return jsonify({'error': 'Ingredient already added to dish'}), 400
    
    # 添加菜品食材关联
    dish_ingredient = DishIngredient(
        dish_id=dish_id,
        ingredient_id=data['ingredient_id'],
        quantity_required=data['quantity_required'],
        unit_of_measure=data.get('unit_of_measure', 'g')
    )
    
    try:
        db.session.add(dish_ingredient)
        db.session.commit()
        return jsonify({
            'id': dish_ingredient.id,
            'ingredient_id': dish_ingredient.ingredient_id,
            'ingredient_name': ingredient.name,
            'quantity_required': dish_ingredient.quantity_required,
            'unit_of_measure': dish_ingredient.unit_of_measure
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 客户订单API
@api.route('/orders', methods=['GET'])
@requires_resource_permission('order', 'read')
def get_orders():
    """获取所有订单"""
    orders = CustomerOrder.query.all()
    return jsonify([{
        'id': order.id,
        'customer_id': order.customer_id,
        'customer_name': order.customer.name,
        'order_date': order.order_date.strftime('%Y-%m-%d'),
        'status': order.status,
        'total_amount': order.total_amount
    } for order in orders])

@api.route('/orders', methods=['POST'])
@requires_resource_permission('order', 'create')
def create_order():
    """创建新订单"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['customer_id', 'items']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查客户是否存在
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # 创建订单
    order = CustomerOrder(
        customer_id=data['customer_id'],
        order_date=data.get('order_date', datetime.now().date()),
        status=data.get('status', 'pending'),
        total_amount=0  # 初始化为0，后续计算
    )
    
    try:
        db.session.add(order)
        db.session.flush()  # 获取order.id
        
        # 添加订单详情
        total_amount = 0
        for item_data in data['items']:
            # 验证订单详情数据
            item_required_fields = ['dish_id', 'quantity']
            item_is_valid, item_error = validate_data(item_data, item_required_fields)
            if not item_is_valid:
                return jsonify(item_error), 400
            
            # 检查菜品是否存在
            dish = Dish.query.get(item_data['dish_id'])
            if not dish:
                return jsonify({'error': f'Dish {item_data["dish_id"]} not found'}), 404
            
            # 创建订单详情
            order_item = OrderItem(
                order_id=order.id,
                dish_id=item_data['dish_id'],
                quantity=item_data['quantity'],
                price=item_data.get('price', 0)
            )
            db.session.add(order_item)
            total_amount += order_item.price * order_item.quantity
        
        # 更新订单总金额
        order.total_amount = total_amount
        
        db.session.commit()
        return jsonify({
            'id': order.id,
            'customer_id': order.customer_id,
            'customer_name': customer.name,
            'order_date': order.order_date.strftime('%Y-%m-%d'),
            'status': order.status,
            'total_amount': order.total_amount
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/orders/<int:order_id>', methods=['GET'])
@requires_resource_permission('order', 'read')
def get_order_detail(order_id):
    """获取订单详情"""
    order = CustomerOrder.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # 获取订单详情
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    items = [{
        'id': item.id,
        'dish_id': item.dish_id,
        'dish_name': item.dish.name,
        'quantity': item.quantity,
        'price': item.price,
        'subtotal': item.price * item.quantity
    } for item in order_items]
    
    return jsonify({
        'id': order.id,
        'customer_id': order.customer_id,
        'customer_name': order.customer.name,
        'order_date': order.order_date.strftime('%Y-%m-%d'),
        'status': order.status,
        'total_amount': order.total_amount,
        'items': items
    })

# 排餐表API
@api.route('/meal_schedules', methods=['GET'])
@requires_resource_permission('meal_schedule', 'read')
def get_meal_schedules():
    """获取所有排餐表"""
    schedules = DeliverySchedule.query.all()
    return jsonify([{
        'id': schedule.id,
        'date': schedule.date.strftime('%Y-%m-%d'),
        'description': schedule.description,
        'status': schedule.status
    } for schedule in schedules])

@api.route('/meal_schedules', methods=['POST'])
@requires_resource_permission('meal_schedule', 'create')
def create_meal_schedule():
    """创建新排餐表"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['date']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查排餐表是否已存在
    existing_schedule = DeliverySchedule.query.filter_by(date=data['date']).first()
    if existing_schedule:
        return jsonify({'error': 'Meal schedule already exists for this date'}), 400
    
    # 创建排餐表
    schedule = DeliverySchedule(
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        description=data.get('description'),
        status=data.get('status', 'draft')
    )
    
    try:
        db.session.add(schedule)
        db.session.commit()
        return jsonify({
            'id': schedule.id,
            'date': schedule.date.strftime('%Y-%m-%d'),
            'description': schedule.description,
            'status': schedule.status
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/meal_schedules/<int:schedule_id>', methods=['GET'])
@requires_resource_permission('meal_schedule', 'read')
def get_meal_schedule_detail(schedule_id):
    """获取排餐表详情"""
    schedule = DeliverySchedule.query.get(schedule_id)
    if not schedule:
        return jsonify({'error': 'Meal schedule not found'}), 404
    
    # 获取排餐表详情
    schedule_items = DeliveryAssignment.query.filter_by(schedule_id=schedule_id).all()
    items = [{
        'id': item.id,
        'customer_id': item.customer_id,
        'customer_name': item.customer.name,
        'dish_id': item.dish_id,
        'dish_name': item.dish.name,
        'category_id': item.category_id,
        'category_name': item.category.name,
        'quantity': item.quantity,
        'status': item.status
    } for item in schedule_items]
    
    return jsonify({
        'id': schedule.id,
        'date': schedule.date.strftime('%Y-%m-%d'),
        'description': schedule.description,
        'status': schedule.status,
        'items': items
    })

@api.route('/meal_schedules/<int:schedule_id>/items', methods=['POST'])
@requires_resource_permission('meal_schedule', 'update')
def add_meal_schedule_item(schedule_id):
    """为排餐表添加排餐项"""
    schedule = DeliverySchedule.query.get(schedule_id)
    if not schedule:
        return jsonify({'error': 'Meal schedule not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['customer_id', 'dish_id', 'category_id']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查客户、菜品、分类是否存在
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    dish = Dish.query.get(data['dish_id'])
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    
    category = MenuCategory.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    # 添加排餐项
    schedule_item = DeliveryAssignment(
        schedule_id=schedule_id,
        customer_id=data['customer_id'],
        dish_id=data['dish_id'],
        quantity=data.get('quantity', 1),
        status=data.get('status', 'scheduled')
    )
    
    try:
        db.session.add(schedule_item)
        db.session.commit()
        return jsonify({
            'id': schedule_item.id,
            'customer_id': schedule_item.customer_id,
            'customer_name': customer.name,
            'dish_id': schedule_item.dish_id,
            'dish_name': dish.name,
            'category_id': schedule_item.category_id,
            'category_name': category.name,
            'quantity': schedule_item.quantity,
            'status': schedule_item.status
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 配送路线API
@api.route('/delivery_routes', methods=['GET'])
@requires_resource_permission('delivery', 'read')
def get_delivery_routes():
    """获取所有配送路线"""
    routes = DeliveryRoute.query.all()
    return jsonify([{
        'id': route.id,
        'route_name': route.route_name,
        'description': route.description,
        'estimated_duration_minutes': route.estimated_duration_minutes,
        'status': route.status
    } for route in routes])

@api.route('/delivery_routes', methods=['POST'])
@requires_resource_permission('delivery', 'create')
def create_delivery_route():
    """创建新配送路线"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['route_name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查配送路线是否已存在
    existing_route = DeliveryRoute.query.filter_by(route_name=data['route_name']).first()
    if existing_route:
        return jsonify({'error': 'Delivery route already exists'}), 400
    
    # 创建配送路线
    route = DeliveryRoute(
        route_name=data['route_name'],
        description=data.get('description'),
        estimated_duration_minutes=data.get('estimated_duration_minutes', 0),
        status=data.get('status', 'active')
    )
    
    try:
        db.session.add(route)
        db.session.commit()
        return jsonify({
            'id': route.id,
            'route_name': route.route_name,
            'description': route.description,
            'estimated_duration_minutes': route.estimated_duration_minutes,
            'status': route.status
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/delivery_routes/<int:route_id>', methods=['GET'])
@requires_resource_permission('delivery', 'read')
def get_delivery_route_detail(route_id):
    """获取配送路线详情"""
    route = DeliveryRoute.query.get(route_id)
    if not route:
        return jsonify({'error': 'Delivery route not found'}), 404
    
    return jsonify({
        'id': route.id,
        'route_name': route.route_name,
        'description': route.description,
        'estimated_duration_minutes': route.estimated_duration_minutes,
        'status': route.status
    })

# 配送状态更新API
@api.route('/delivery_assignments/<int:assignment_id>/status', methods=['PUT'])
@requires_resource_permission('delivery', 'update')
def update_delivery_status(assignment_id):
    """更新配送状态"""
    assignment = DeliveryAssignment.query.get(assignment_id)
    if not assignment:
        return jsonify({'error': 'Delivery assignment not found'}), 404
    
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    # 验证状态值
    valid_statuses = ['scheduled', 'in_progress', 'delivered', 'failed']
    if data['status'] not in valid_statuses:
        return jsonify({'error': f'Invalid status. Valid statuses are: {valid_statuses}'}), 400
    
    # 更新配送状态
    old_status = assignment.status
    assignment.status = data['status']
    
    # 记录状态更新
    status_update = DeliveryStatusUpdate(
        assignment_id=assignment_id,
        old_status=old_status,
        new_status=data['status'],
        timestamp=datetime.now(),
        notes=data.get('notes')
    )
    
    try:
        db.session.add(status_update)
        db.session.commit()
        return jsonify({
            'id': assignment.id,
            'status': assignment.status,
            'last_updated': status_update.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 配送状态历史API
@api.route('/delivery_assignments/<int:assignment_id>/status_history', methods=['GET'])
@requires_resource_permission('delivery', 'read')
def get_delivery_status_history(assignment_id):
    """获取配送状态历史"""
    assignment = DeliveryAssignment.query.get(assignment_id)
    if not assignment:
        return jsonify({'error': 'Delivery assignment not found'}), 404
    
    status_history = DeliveryStatusUpdate.query.filter_by(assignment_id=assignment_id).order_by(DeliveryStatusUpdate.timestamp.desc()).all()
    return jsonify([{
        'id': update.id,
        'old_status': update.old_status,
        'new_status': update.new_status,
        'timestamp': update.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'notes': update.notes
    } for update in status_history])

# 菜单分类API
@api.route('/menu_categories', methods=['GET'])
def get_menu_categories():
    """获取所有菜单分类"""
    categories = MenuCategory.query.all()
    return jsonify([{
        'id': category.id,
        'name': category.name,
        'description': category.description
    } for category in categories])

@api.route('/menu_categories', methods=['POST'])
def create_menu_category():
    """创建新菜单分类"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查菜单分类是否已存在
    existing_category = MenuCategory.query.filter_by(name=data['name']).first()
    if existing_category:
        return jsonify({'error': 'Menu category already exists'}), 400
    
    # 创建菜单分类
    category = MenuCategory(
        name=data['name'],
        description=data.get('description')
    )
    
    try:
        db.session.add(category)
        db.session.commit()
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/menu_categories/<int:category_id>', methods=['GET'])
def get_menu_category_detail(category_id):
    """获取菜单分类详情"""
    category = MenuCategory.query.get(category_id)
    if not category:
        return jsonify({'error': 'Menu category not found'}), 404
    
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    })

@api.route('/menu_categories/<int:category_id>', methods=['PUT'])
def update_menu_category(category_id):
    """更新菜单分类"""
    category = MenuCategory.query.get(category_id)
    if not category:
        return jsonify({'error': 'Menu category not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 更新菜单分类
    if 'name' in data:
        # 检查菜单分类名称是否已被其他分类使用
        existing_category = MenuCategory.query.filter_by(name=data['name']).filter(MenuCategory.id != category_id).first()
        if existing_category:
            return jsonify({'error': 'Menu category name already exists'}), 400
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']
    
    try:
        db.session.commit()
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/menu_categories/<int:category_id>', methods=['DELETE'])
def delete_menu_category(category_id):
    """删除菜单分类"""
    category = MenuCategory.query.get(category_id)
    if not category:
        return jsonify({'error': 'Menu category not found'}), 404
    
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Menu category deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 服务分类API
@api.route('/service_categories', methods=['GET'])
def get_service_categories():
    """获取所有服务分类"""
    categories = ServiceCategory.query.all()
    return jsonify([{
        'id': category.id,
        'name': category.name,
        'description': category.description
    } for category in categories])

@api.route('/service_categories', methods=['POST'])
@requires_resource_permission('service', 'create')
def create_service_category():
    """创建新服务分类"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查服务分类是否已存在
    existing_category = ServiceCategory.query.filter_by(name=data['name']).first()
    if existing_category:
        return jsonify({'error': 'Service category already exists'}), 400
    
    # 创建服务分类
    category = ServiceCategory(
        name=data['name'],
        description=data.get('description')
    )
    
    try:
        db.session.add(category)
        db.session.commit()
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/service_categories/<int:category_id>', methods=['GET'])
def get_service_category_detail(category_id):
    """获取服务分类详情"""
    category = ServiceCategory.query.get(category_id)
    if not category:
        return jsonify({'error': 'Service category not found'}), 404
    
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    })

@api.route('/service_categories/<int:category_id>', methods=['PUT'])
@requires_resource_permission('service', 'update')
def update_service_category(category_id):
    """更新服务分类"""
    category = ServiceCategory.query.get(category_id)
    if not category:
        return jsonify({'error': 'Service category not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 更新服务分类
    if 'name' in data:
        # 检查服务分类名称是否已被其他分类使用
        existing_category = ServiceCategory.query.filter_by(name=data['name']).filter(ServiceCategory.id != category_id).first()
        if existing_category:
            return jsonify({'error': 'Service category name already exists'}), 400
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']
    
    try:
        db.session.commit()
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)



# 服务项目API
@api.route('/service_items', methods=['GET'])
def get_service_items():
    """获取所有服务项目"""
    items = ServiceItem.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'duration_minutes': item.duration_minutes,
        'category_id': item.category_id,
        'category_name': item.category.name if item.category else None,
        'is_active': item.is_active
    } for item in items])

@api.route('/service_items', methods=['POST'])
@requires_resource_permission('service', 'create')
def create_service_item():
    """创建新服务项目"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name', 'price', 'duration_minutes', 'category_id']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查服务项目是否已存在
    existing_item = ServiceItem.query.filter_by(name=data['name']).first()
    if existing_item:
        return jsonify({'error': 'Service item already exists'}), 400
    
    # 检查服务分类是否存在
    category = ServiceCategory.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Service category not found'}), 404
    
    # 创建服务项目
    item = ServiceItem(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        duration_minutes=data['duration_minutes'],
        category_id=data['category_id'],
        is_active=data.get('is_active', True)
    )
    
    try:
        db.session.add(item)
        db.session.commit()
        return jsonify({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'duration_minutes': item.duration_minutes,
            'category_id': item.category_id,
            'category_name': category.name,
            'is_active': item.is_active
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/service_items/<int:item_id>', methods=['GET'])
def get_service_item_detail(item_id):
    """获取服务项目详情"""
    item = ServiceItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Service item not found'}), 404
    
    return jsonify({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'duration_minutes': item.duration_minutes,
        'category_id': item.category_id,
        'category_name': item.category.name if item.category else None,
        'is_active': item.is_active
    })

@api.route('/service_items/<int:item_id>', methods=['PUT'])
@requires_resource_permission('service', 'update')
def update_service_item(item_id):
    """更新服务项目"""
    item = ServiceItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Service item not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    if 'name' in data:
        # 检查服务项目名称是否已被其他项目使用
        existing_item = ServiceItem.query.filter_by(name=data['name']).filter(ServiceItem.id != item_id).first()
        if existing_item:
            return jsonify({'error': 'Service item name already exists'}), 400
        item.name = data['name']
    
    # 更新其他字段
    if 'description' in data:
        item.description = data['description']
    if 'price' in data:
        item.price = data['price']
    if 'duration_minutes' in data:
        item.duration_minutes = data['duration_minutes']
    if 'category_id' in data:
        # 检查服务分类是否存在
        category = ServiceCategory.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Service category not found'}), 404
        item.category_id = data['category_id']
    if 'is_active' in data:
        item.is_active = data['is_active']
    
    try:
        db.session.commit()
        return jsonify({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'duration_minutes': item.duration_minutes,
            'category_id': item.category_id,
            'category_name': item.category.name if item.category else None,
            'is_active': item.is_active
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)



# 服务套餐API
@api.route('/service_packages', methods=['GET'])
def get_service_packages():
    """获取所有服务套餐"""
    packages = ServicePackage.query.all()
    return jsonify([{
        'id': package.id,
        'name': package.name,
        'description': package.description,
        'price': package.price,
        'is_active': package.is_active
    } for package in packages])

@api.route('/service_packages', methods=['POST'])
@requires_resource_permission('service', 'create')
def create_service_package():
    """创建新服务套餐"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['name', 'price', 'items']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查服务套餐是否已存在
    existing_package = ServicePackage.query.filter_by(name=data['name']).first()
    if existing_package:
        return jsonify({'error': 'Service package already exists'}), 400
    
    # 创建服务套餐
    package = ServicePackage(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        is_active=data.get('is_active', True)
    )
    
    try:
        db.session.add(package)
        db.session.flush()  # 获取package.id
        
        # 添加服务套餐项目
        for item_data in data['items']:
            # 验证套餐项目数据
            item_required_fields = ['service_item_id', 'quantity']
            item_is_valid, item_error = validate_data(item_data, item_required_fields)
            if not item_is_valid:
                return jsonify(item_error), 400
            
            # 检查服务项目是否存在
            service_item = ServiceItem.query.get(item_data['service_item_id'])
            if not service_item:
                return jsonify({'error': f'Service item {item_data["service_item_id"]} not found'}), 404
            
            # 创建服务套餐项目
            package_item = ServicePackageItem(
                package_id=package.id,
                service_item_id=item_data['service_item_id'],
                quantity=item_data['quantity']
            )
            db.session.add(package_item)
        
        db.session.commit()
        return jsonify({
            'id': package.id,
            'name': package.name,
            'description': package.description,
            'price': package.price,
            'is_active': package.is_active
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/service_packages/<int:package_id>', methods=['GET'])
def get_service_package_detail(package_id):
    """获取服务套餐详情"""
    package = ServicePackage.query.get(package_id)
    if not package:
        return jsonify({'error': 'Service package not found'}), 404
    
    # 获取服务套餐项目
    package_items = ServicePackageItem.query.filter_by(package_id=package_id).all()
    items = [{
        'id': pi.id,
        'service_item_id': pi.service_item_id,
        'service_item_name': pi.service_item.name,
        'quantity': pi.quantity,
        'item_price': pi.service_item.price,
        'subtotal': pi.service_item.price * pi.quantity
    } for pi in package_items]
    
    return jsonify({
        'id': package.id,
        'name': package.name,
        'description': package.description,
        'price': package.price,
        'is_active': package.is_active,
        'items': items
    })

# 服务预订API
@api.route('/service_bookings', methods=['GET'])
@requires_resource_permission('service', 'read')
def get_service_bookings():
    """获取所有服务预订"""
    bookings = ServiceBooking.query.order_by(ServiceBooking.booking_date.desc()).all()
    return jsonify([{
        'id': booking.id,
        'booking_number': booking.booking_number,
        'customer_id': booking.customer_id,
        'customer_name': booking.customer.name if booking.customer else None,
        'service_item_id': booking.service_item_id,
        'service_item_name': booking.service_item.name if booking.service_item else None,
        'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
        'start_time': booking.start_time.strftime('%H:%M') if booking.start_time else None,
        'duration_minutes': booking.duration_minutes,
        'status': booking.status,
        'price': booking.service_item.price if booking.service_item else None
    } for booking in bookings])

@api.route('/service_bookings', methods=['POST'])
@requires_resource_permission('service', 'create')
def create_service_booking():
    """创建新服务预订"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['customer_id', 'service_item_id', 'booking_date', 'start_time']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查客户是否存在
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # 检查服务项目是否存在
    service_item = ServiceItem.query.get(data['service_item_id'])
    if not service_item:
        return jsonify({'error': 'Service item not found'}), 404
    
    # 生成预订号
    import uuid
    booking_number = f'SB_{uuid.uuid4().hex[:8].upper()}_{datetime.now().strftime("%Y%m%d")}'
    
    # 创建服务预订
    booking = ServiceBooking(
        booking_number=booking_number,
        customer_id=data['customer_id'],
        service_item_id=data['service_item_id'],
        booking_date=datetime.strptime(data['booking_date'], '%Y-%m-%d').date(),
        start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
        duration_minutes=data.get('duration_minutes', service_item.duration_minutes),
        status=data.get('status', 'confirmed'),
        price=data.get('price', service_item.price),
        notes=data.get('notes')
    )
    
    try:
        db.session.add(booking)
        db.session.commit()
        return jsonify({
            'id': booking.id,
            'booking_number': booking.booking_number,
            'customer_id': booking.customer_id,
            'customer_name': customer.name,
            'service_item_id': booking.service_item_id,
            'service_item_name': service_item.name,
            'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
            'start_time': booking.start_time.strftime('%H:%M'),
            'duration_minutes': booking.duration_minutes,
            'status': booking.status,
            'price': booking.price
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/service_bookings/<int:booking_id>', methods=['GET'])
@requires_resource_permission('service', 'read')
def get_service_booking_detail(booking_id):
    """获取服务预订详情"""
    booking = ServiceBooking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Service booking not found'}), 404
    
    return jsonify({
        'id': booking.id,
        'booking_number': booking.booking_number,
        'customer_id': booking.customer_id,
        'customer_name': booking.customer.name if booking.customer else None,
        'service_item_id': booking.service_item_id,
        'service_item_name': booking.service_item.name if booking.service_item else None,
        'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
        'start_time': booking.start_time.strftime('%H:%M') if booking.start_time else None,
        'duration_minutes': booking.duration_minutes,
        'status': booking.status,
        'price': booking.price,
        'notes': booking.notes
    })

@api.route('/service_bookings/<int:booking_id>', methods=['PUT'])
@requires_resource_permission('service', 'update')
def update_service_booking(booking_id):
    """更新服务预订"""
    booking = ServiceBooking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Service booking not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 更新服务预订信息
    if 'customer_id' in data:
        # 检查客户是否存在
        customer = Customer.query.get(data['customer_id'])
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        booking.customer_id = data['customer_id']
    if 'service_item_id' in data:
        # 检查服务项目是否存在
        service_item = ServiceItem.query.get(data['service_item_id'])
        if not service_item:
            return jsonify({'error': 'Service item not found'}), 404
        booking.service_item_id = data['service_item_id']
    if 'booking_date' in data:
        booking.booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
    if 'start_time' in data:
        booking.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
    if 'duration_minutes' in data:
        booking.duration_minutes = data['duration_minutes']
    if 'status' in data:
        booking.status = data['status']
    if 'price' in data:
        booking.price = data['price']
    if 'notes' in data:
        booking.notes = data['notes']
    
    try:
        db.session.commit()
        return jsonify({
            'id': booking.id,
            'booking_number': booking.booking_number,
            'customer_id': booking.customer_id,
            'customer_name': booking.customer.name if booking.customer else None,
            'service_item_id': booking.service_item_id,
            'service_item_name': booking.service_item.name if booking.service_item else None,
            'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
            'start_time': booking.start_time.strftime('%H:%M') if booking.start_time else None,
            'duration_minutes': booking.duration_minutes,
            'status': booking.status,
            'price': booking.price,
            'notes': booking.notes
        })
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/service_categories/<int:category_id>', methods=['DELETE'])
@requires_resource_permission('service', 'delete')
def delete_service_category(category_id):
    """删除服务分类"""
    category = ServiceCategory.query.get(category_id)
    if not category:
        return jsonify({'error': 'Service category not found'}), 404
    
    # 检查是否有服务项目关联
    service_items = ServiceItem.query.filter_by(category_id=category_id).first()
    if service_items:
        return jsonify({'error': 'Cannot delete category with associated service items'}), 400
    
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Service category deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)









@api.route('/service_items/<int:item_id>', methods=['DELETE'])
@requires_resource_permission('service', 'delete')
def delete_service_item(item_id):
    """删除服务项目"""
    item = ServiceItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Service item not found'}), 404
    
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Service item deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/service_records', methods=['GET'])
@requires_resource_permission('service', 'read')
def get_service_records():
    """获取所有服务记录"""
    records = ServiceBooking.query.all()
    return jsonify([{
        'id': record.id,
        'customer_id': record.customer_id,
        'customer_name': record.customer.name if record.customer else None,
        'service_item_id': record.service_item_id,
        'service_item_name': record.service_item.name if record.service_item else None,
        'staff_id': record.staff_id,
        'staff_name': record.staff.username if record.staff else None,
        'start_time': record.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': record.end_time.strftime('%Y-%m-%d %H:%M:%S') if record.end_time else None,
        'duration': record.duration,
        'status': record.status,
        'notes': record.notes
    } for record in records])

@api.route('/service_records', methods=['POST'])
@requires_resource_permission('service', 'create')
def create_service_record():
    """创建新服务记录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['customer_id', 'service_item_id', 'staff_id', 'start_time']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 创建服务记录
    record = ServiceBooking(
        customer_id=data['customer_id'],
        service_item_id=data['service_item_id'],
        staff_id=data['staff_id'],
        start_time=datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S'),
        end_time=datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S') if data.get('end_time') else None,
        duration=data.get('duration'),
        status=data.get('status', 'scheduled'),
        notes=data.get('notes')
    )
    
    try:
        db.session.add(record)
        db.session.commit()
        return jsonify({
            'id': record.id,
            'customer_id': record.customer_id,
            'service_item_id': record.service_item_id,
            'staff_id': record.staff_id,
            'start_time': record.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': record.end_time.strftime('%Y-%m-%d %H:%M:%S') if record.end_time else None,
            'duration': record.duration,
            'status': record.status,
            'notes': record.notes
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 月子餐管理API
@api.route('/confinement_meal_plans', methods=['GET'])
@requires_resource_permission('confinement_meal', 'read')
def get_confinement_meal_plans():
    """获取所有月子餐计划"""
    plans = ConfinementMealPlan.query.all()
    return jsonify([{
        'id': plan.id,
        'customer_id': plan.customer_id,
        'customer_name': plan.customer.name if plan.customer else None,
        'start_date': plan.start_date.strftime('%Y-%m-%d'),
        'end_date': plan.end_date.strftime('%Y-%m-%d') if plan.end_date else None,
        'status': plan.status
    } for plan in plans])

@api.route('/confinement_meal_plans', methods=['POST'])
@requires_resource_permission('confinement_meal', 'create')
def create_confinement_meal_plan():
    """创建新月子餐计划"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['customer_id', 'start_date']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查客户是否已存在月子餐计划
    existing_plan = ConfinementMealPlan.query.filter_by(customer_id=data['customer_id']).first()
    if existing_plan:
        return jsonify({'error': 'Confinement meal plan already exists for this customer'}), 400
    
    # 创建月子餐计划
    plan = ConfinementMealPlan(
        customer_id=data['customer_id'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
        status=data.get('status', 'active')
    )
    
    try:
        db.session.add(plan)
        db.session.commit()
        return jsonify({
            'id': plan.id,
            'customer_id': plan.customer_id,
            'start_date': plan.start_date.strftime('%Y-%m-%d'),
            'end_date': plan.end_date.strftime('%Y-%m-%d') if plan.end_date else None,
            'status': plan.status
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 送餐管理API
@api.route('/delivery_records', methods=['GET'])
@requires_resource_permission('delivery', 'read')
def get_delivery_records():
    """获取所有送餐记录"""
    records = DeliveryAssignment.query.all()
    return jsonify([{
        'id': record.id,
        'customer_id': record.customer_id,
        'customer_name': record.customer.name if record.customer else None,
        'delivery_staff_id': record.delivery_staff_id,
        'delivery_staff_name': record.delivery_staff.username if record.delivery_staff else None,
        'order_id': record.order_id,
        'meal_schedule_item_id': record.meal_schedule_item_id,
        'start_time': record.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': record.end_time.strftime('%Y-%m-%d %H:%M:%S') if record.end_time else None,
        'duration': record.duration,
        'distance': record.distance,
        'status': record.status,
        'notes': record.notes
    } for record in records])

@api.route('/delivery_records', methods=['POST'])
@requires_resource_permission('delivery', 'create')
def create_delivery_record():
    """创建新送餐记录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['customer_id', 'delivery_staff_id', 'start_time']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 创建送餐记录
    record = DeliveryAssignment(
        customer_id=data['customer_id'],
        delivery_staff_id=data['delivery_staff_id'],
        order_id=data.get('order_id'),
        start_time=datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S'),
        end_time=datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S') if data.get('end_time') else None,
        duration=data.get('duration'),
        distance=data.get('distance'),
        status=data.get('status', 'pending'),
        notes=data.get('notes')
    )
    
    try:
        db.session.add(record)
        db.session.commit()
        return jsonify({
            'id': record.id,
            'customer_id': record.customer_id,
            'delivery_staff_id': record.delivery_staff_id,
            'start_time': record.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': record.end_time.strftime('%Y-%m-%d %H:%M:%S') if record.end_time else None,
            'duration': record.duration,
            'distance': record.distance,
            'status': record.status,
            'notes': record.notes
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# AI数据分析API
@api.route('/ai_analysis_results', methods=['GET'])
@requires_resource_permission('ai_analysis', 'read')
def get_ai_analysis_results():
    """获取所有AI分析结果"""
    results = AIAnalysisResult.query.all()
    return jsonify([{
        'id': result.id,
        'analysis_type': result.analysis_type,
        'analysis_data': result.analysis_data,
        'result': result.result,
        'recommendation': result.recommendation,
        'created_at': result.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for result in results])

@api.route('/ai_analysis_results', methods=['POST'])
@requires_resource_permission('ai_analysis', 'create')
def create_ai_analysis_result():
    """创建新AI分析结果"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['analysis_type', 'analysis_data', 'result']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 创建AI分析结果
    result = AIAnalysisResult(
        analysis_type=data['analysis_type'],
        analysis_data=data['analysis_data'],
        result=data['result'],
        recommendation=data.get('recommendation')
    )
    
    try:
        db.session.add(result)
        db.session.commit()
        return jsonify({
            'id': result.id,
            'analysis_type': result.analysis_type,
            'analysis_data': result.analysis_data,
            'result': result.result,
            'recommendation': result.recommendation,
            'created_at': result.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@api.route('/ai_analysis/analyze', methods=['POST'])
@requires_resource_permission('ai_analysis', 'create')
def analyze_data():
    """执行AI数据分析"""
    from utils.ai_analyzer import AIAnalyzer
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    analysis_type = data.get('analysis_type')
    if not analysis_type:
        return jsonify({'error': 'Analysis type is required'}), 400
    
    analyzer = AIAnalyzer()
    
    try:
        # 根据分析类型执行相应的分析
        if analysis_type == 'dish_quality':
            days = data.get('days', 30)
            result = analyzer.analyze_dish_quality(days)
        elif analysis_type == 'cost_effectiveness':
            result = analyzer.analyze_cost_effectiveness()
        elif analysis_type == 'sales_performance':
            days = data.get('days', 30)
            result = analyzer.analyze_sales_performance(days)
        elif analysis_type == 'nutritional_balance':
            result = analyzer.analyze_nutritional_balance()
        else:
            return jsonify({'error': 'Invalid analysis type'}), 400
        
        # 保存分析结果到数据库
        ai_result = AIAnalysisResult(
            analysis_type=analysis_type,
            analysis_data=result,
            result=result,
            recommendation='\n'.join(result.get('recommendations', []))
        )
        db.session.add(ai_result)
        db.session.commit()
        
        return jsonify({
            'message': 'Analysis completed successfully',
            'analysis_type': analysis_type,
            'result': result,
            'analysis_id': ai_result.id
        }), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 供应商管理API
@api.route('/suppliers', methods=['GET'])
def get_suppliers():
    """获取所有供应商"""
    suppliers = Supplier.query.all()
    return jsonify([{
        'id': supplier.id,
        'name': supplier.name,
        'contact_person': supplier.contact_person,
        'phone': supplier.phone,
        'address': supplier.address,
        'description': supplier.description,
        'created_at': supplier.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for supplier in suppliers])



# 食材采购API
@api.route('/ingredient_purchases', methods=['GET'])
def get_ingredient_purchases():
    """获取所有食材采购记录"""
    purchases = PurchaseOrder.query.all()
    return jsonify([{
        'id': purchase.id,
        'ingredient_id': purchase.ingredient_id,
        'ingredient_name': purchase.ingredient.name,
        'supplier_id': purchase.supplier_id,
        'supplier_name': purchase.supplier.name,
        'purchase_date': purchase.purchase_date.strftime('%Y-%m-%d %H:%M:%S'),
        'quantity': purchase.quantity,
        'unit_price': purchase.unit_price,
        'total_price': purchase.total_price,
        'batch_number': purchase.batch_number,
        'shelf_life': purchase.shelf_life,
        'notes': purchase.notes,
        'created_by': purchase.creator.username if purchase.creator else None
    } for purchase in purchases])

@api.route('/ingredient_purchases', methods=['POST'])
@requires_resource_permission('ingredient_purchase', 'create')
def create_ingredient_purchase():
    """创建新食材采购记录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['ingredient_id', 'supplier_id', 'quantity', 'unit_price', 'total_price']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查食材是否存在
    ingredient = Ingredient.query.get(data['ingredient_id'])
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    # 检查供应商是否存在
    supplier = Supplier.query.get(data['supplier_id'])
    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404
    
    # 创建食材采购记录
    purchase = PurchaseOrder(
        supplier_id=data['supplier_id'],
        purchase_date=data.get('purchase_date', datetime.now()),
        total_amount=data['total_price'],
        batch_number=data.get('batch_number'),
        notes=data.get('notes'),
        created_by=data.get('created_by')
    )
    
    # 创建采购订单明细
    purchase_item = PurchaseOrderItem(
        purchase_order_id=purchase.id,
        ingredient_id=data['ingredient_id'],
        quantity=data['quantity'],
        unit_price=data['unit_price'],
        total_price=data['total_price']
    )
    db.session.add(purchase_item)
    
    try:
        db.session.add(purchase)
        # 更新食材库存
        ingredient.stock += data['quantity']
        db.session.commit()
        return jsonify({
            'id': purchase.id,
            'ingredient_id': purchase.ingredient_id,
            'ingredient_name': ingredient.name,
            'supplier_id': purchase.supplier_id,
            'supplier_name': supplier.name,
            'purchase_date': purchase.purchase_date.strftime('%Y-%m-%d %H:%M:%S'),
            'quantity': purchase.quantity,
            'unit_price': purchase.unit_price,
            'total_price': purchase.total_price,
            'batch_number': purchase.batch_number,
            'shelf_life': purchase.shelf_life,
            'notes': purchase.notes,
            'created_by': purchase.creator.username if purchase.creator else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 图片识别API
@api.route('/image_recognition/ingredient', methods=['POST'])
@requires_resource_permission('ingredient', 'create')
def recognize_ingredient_image():
    """识别食材图片并获取信息"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        return jsonify({'error': 'Invalid file format'}), 400
    
    try:
        # 保存文件
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        filepath = os.path.join('uploads', 'ingredient_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_' + file.filename)
        file.save(filepath)
        
        # 模拟食材识别结果
        # 实际项目中，这里应该调用OCR API进行食材识别
        ingredient_info = {
            'name': '西红柿',
            'nutrition_info': {
                'vitamin_c': 13.7,
                'vitamin_a': 42,
                'potassium': 237
            },
            'calorie': 18,
            'shelf_life': 7
        }
        
        return jsonify({
            'message': 'Ingredient image recognized successfully',
            'image_url': filepath,
            'ingredient_info': ingredient_info
        }), 200
    except Exception as e:
        return handle_error(e)

@api.route('/image_recognition/physical_exam', methods=['POST'])
@requires_resource_permission('customer', 'create')
def recognize_physical_exam():
    """识别体检表图片并获取信息"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        return jsonify({'error': 'Invalid file format'}), 400
    
    try:
        # 保存文件
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        filepath = os.path.join('uploads', 'physical_exam_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_' + file.filename)
        file.save(filepath)
        
        # 模拟体检表识别结果
        # 实际项目中，这里应该调用OCR API进行体检表识别
        health_conditions = {
            'height': 165,
            'weight': 55,
            'blood_pressure': '120/80',
            'blood_sugar': 5.2,
            'allergies': ['青霉素']
        }
        
        return jsonify({
            'message': 'Physical exam image recognized successfully',
            'image_url': filepath,
            'health_conditions': health_conditions
        }), 200
    except Exception as e:
        return handle_error(e)

# 月子餐外卖API
@api.route('/confinement_meal/takeaway', methods=['POST'])
@requires_resource_permission('confinement_meal', 'create')
def create_takeaway_order():
    """创建月子餐外卖订单"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证数据
    required_fields = ['customer_id', 'delivery_address', 'items']
    is_valid, error = validate_data(data, required_fields)
    if not is_valid:
        return jsonify(error), 400
    
    # 检查客户是否存在
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # 创建外卖类型的月子餐计划
    plan = ConfinementMealPlan(
        customer_id=data['customer_id'],
        start_date=datetime.now().date(),
        end_date=data.get('end_date'),
        status='active',
        type='takeaway'
    )
    
    try:
        db.session.add(plan)
        db.session.commit()
        return jsonify({
            'message': 'Takeaway order created successfully',
            'plan_id': plan.id,
            'customer_id': plan.customer_id,
            'start_date': plan.start_date.strftime('%Y-%m-%d'),
            'end_date': plan.end_date.strftime('%Y-%m-%d') if plan.end_date else None,
            'type': plan.type
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# 查询和打印API
@api.route('/reports/customer_meals/<int:customer_id>', methods=['GET'])
def get_customer_meals_report(customer_id):
    """获取客户餐食记录报告"""
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # 获取客户的餐食记录
    # 1. 客户菜单记录
    customer_menus = CustomerMenuSelection.query.filter_by(customer_id=customer_id).all()
    # 2. 订单记录
    orders = CustomerOrder.query.filter_by(customer_id=customer_id).all()
    # 3. 排餐记录
    schedule_items = DeliveryAssignment.query.filter_by(customer_id=customer_id).all()
    # 4. 月子餐记录
    confinement_plan = ConfinementMealPlan.query.filter_by(customer_id=customer_id).first()
    confinement_meals = []
    if confinement_plan:
        week_plans = ConfinementWeekPlan.query.filter_by(meal_plan_id=confinement_plan.id).all()
        for week_plan in week_plans:
            day_plans = ConfinementDayPlan.query.filter_by(week_plan_id=week_plan.id).all()
            for day_plan in day_plans:
                meal_items = ConfinementMealItem.query.filter_by(day_plan_id=day_plan.id).all()
                for meal_item in meal_items:
                    confinement_meals.append({
                        'week': week_plan.week_number,
                        'day': day_plan.day_of_week,
                        'category': meal_item.category.name if meal_item.category else None,
                        'dish': meal_item.dish.name if meal_item.dish else None
                    })
    
    return jsonify({
        'customer': {
            'id': customer.id,
            'name': customer.name,
            'check_in_date': customer.check_in_date.strftime('%Y-%m-%d') if customer.check_in_date else None,
            'check_out_date': customer.check_out_date.strftime('%Y-%m-%d') if customer.check_out_date else None
        },
        'customer_menus_count': len(customer_menus),
        'orders_count': len(orders),
        'schedule_items_count': len(schedule_items),
        'confinement_meals': confinement_meals
    })

@api.route('/reports/customer_services/<int:customer_id>', methods=['GET'])
def get_customer_services_report(customer_id):
    """获取客户服务记录报告"""
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # 获取客户的服务记录
    service_records = ServiceBooking.query.filter_by(customer_id=customer_id).all()
    services = []
    for record in service_records:
        services.append({
            'id': record.id,
            'service_item': record.service_item.name if record.service_item else None,
            'staff': record.staff.username if record.staff else None,
            'start_time': record.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': record.end_time.strftime('%Y-%m-%d %H:%M:%S') if record.end_time else None,
            'duration': record.duration,
            'status': record.status,
            'notes': record.notes
        })
    
    return jsonify({
        'customer': {
            'id': customer.id,
            'name': customer.name
        },
        'services_count': len(services),
        'services': services
    })

@api.route('/reports/staff_workload/<int:staff_id>', methods=['GET'])
def get_staff_workload_report(staff_id):
    """获取员工工作量报告"""
    staff = User.query.get(staff_id)
    if not staff:
        return jsonify({'error': 'Staff not found'}), 404
    
    # 获取员工的服务记录
    service_records = ServiceBooking.query.filter_by(staff_id=staff_id).all()
    delivery_records = DeliveryAssignment.query.filter_by(delivery_staff_id=staff_id).all()
    
    workload = {
        'total_service_hours': sum((record.duration or 0) / 60 for record in service_records),
        'total_delivery_hours': sum((record.duration or 0) / 60 for record in delivery_records),
        'total_service_count': len(service_records),
        'total_delivery_count': len(delivery_records)
    }
    
    return jsonify({
        'staff': {
            'id': staff.id,
            'username': staff.username,
            'role': staff.role
        },
        'workload': workload,
        'service_records': [{
            'customer': record.customer.name if record.customer else None,
            'service_item': record.service_item.name if record.service_item else None,
            'duration': record.duration,
            'date': record.start_time.strftime('%Y-%m-%d')
        } for record in service_records],
        'delivery_records': [{
            'customer': record.customer.name if record.customer else None,
            'distance': record.distance,
            'duration': record.duration,
            'date': record.start_time.strftime('%Y-%m-%d')
        } for record in delivery_records]
    })
