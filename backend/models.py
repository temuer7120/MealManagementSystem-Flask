from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(db.Model):
    """基础模型，包含标准字段和乐观锁"""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)
    version = db.Column(db.Integer, default=0, nullable=False)

class MenuCategory(BaseModel):
    """菜单分类模型"""
    __tablename__ = 'menu_category'
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<MenuCategory {self.name}>'

class Dish(BaseModel):
    """菜品模型"""
    __tablename__ = 'dish'
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    ingredients = db.Column(db.JSON)
    dietary_restrictions = db.Column(db.JSON)
    calories_per_serving = db.Column(db.Numeric(6, 2))
    price = db.Column(db.Numeric(10, 2), default=0)
    preparation_time = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), index=True)
    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    category = db.relationship('MenuCategory', backref=db.backref('dishes', lazy=True))
    
    def __repr__(self):
        return f'<Dish {self.name}>'

class Menu(BaseModel):
    """菜单模型"""
    __tablename__ = 'menu'
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    week_number = db.Column(db.Integer, index=True)
    year = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='draft', index=True)
    total_calories = db.Column(db.Numeric(8, 2))
    total_price = db.Column(db.Numeric(10, 2))
    
    def __repr__(self):
        return f'<Menu {self.name}>'

class MenuDish(BaseModel):
    """菜单与菜品的关联模型"""
    __tablename__ = 'menu_dish'
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    day_of_week = db.Column(db.Integer, nullable=False, index=True)
    meal_type = db.Column(db.String(20), nullable=False, index=True)
    serving_time = db.Column(db.Time)
    sort_order = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), index=True)
    
    menu = db.relationship('Menu', backref=db.backref('menu_dishes', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('menu_dishes', lazy=True))
    category = db.relationship('MenuCategory', backref=db.backref('menu_dishes', lazy=True))

class DailyMenu(BaseModel):
    """每日菜单模型"""
    __tablename__ = 'daily_menu'
    date = db.Column(db.Date, nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='planned', index=True)
    total_orders = db.Column(db.Integer, default=0)
    total_revenue = db.Column(db.Numeric(12, 2), default=0)
    
    def __repr__(self):
        return f'<DailyMenu {self.date}>'

class DailyMenuDish(BaseModel):
    """每日菜单与菜品的关联模型"""
    __tablename__ = 'daily_menu_dish'
    daily_menu_id = db.Column(db.Integer, db.ForeignKey('daily_menu.id'), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    meal_type = db.Column(db.String(20), nullable=False, index=True)
    quantity_available = db.Column(db.Integer, default=0)
    quantity_ordered = db.Column(db.Integer, default=0)
    quantity_prepared = db.Column(db.Integer, default=0)
    price_override = db.Column(db.Numeric(10, 2))
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), index=True)
    
    daily_menu = db.relationship('DailyMenu', backref=db.backref('daily_menu_dishes', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('daily_menu_dishes', lazy=True))
    category = db.relationship('MenuCategory', backref=db.backref('daily_menu_dishes', lazy=True))

class Customer(BaseModel):
    """客户模型"""
    __tablename__ = 'customer'
    name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    height_cm = db.Column(db.Numeric(5, 2))
    weight_kg = db.Column(db.Numeric(5, 2))
    check_in_date = db.Column(db.Date, index=True)
    check_out_date = db.Column(db.Date, index=True)
    id_card_number = db.Column(db.String(20), unique=True, index=True)
    id_card_image_url = db.Column(db.String(500))
    physical_exam_report_url = db.Column(db.String(500))
    health_conditions = db.Column(db.JSON)
    dietary_restrictions = db.Column(db.JSON)
    allergies = db.Column(db.JSON)
    preferred_foods = db.Column(db.JSON)
    meal_plan_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='active', index=True)
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class CustomerDietaryPreference(BaseModel):
    """客户饮食偏好模型"""
    __tablename__ = 'customer_dietary_preference'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    preference_type = db.Column(db.String(50), nullable=False, index=True)
    preference_value = db.Column(db.String(200))
    severity = db.Column(db.String(20), default='medium')
    notes = db.Column(db.Text)
    
    customer = db.relationship('Customer', backref=db.backref('dietary_preferences', lazy=True))

class CustomerMenuSelection(BaseModel):
    """客户菜单选择模型"""
    __tablename__ = 'customer_menu_selection'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    daily_menu_id = db.Column(db.Integer, db.ForeignKey('daily_menu.id'), nullable=False, index=True)
    selection_date = db.Column(db.Date, nullable=False, index=True)
    meal_type = db.Column(db.String(20), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, default=1)
    special_instructions = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending', index=True)
    
    customer = db.relationship('Customer', backref=db.backref('menu_selections', lazy=True))
    daily_menu = db.relationship('DailyMenu', backref=db.backref('customer_selections', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('customer_selections', lazy=True))

class User(BaseModel):
    """用户模型"""
    __tablename__ = 'user'
    username = db.Column(db.String(100), nullable=False, unique=True, index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    department = db.Column(db.String(50))
    position = db.Column(db.String(50))
    avatar_url = db.Column(db.String(500))
    last_login_at = db.Column(db.DateTime, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    color_theme = db.Column(db.String(20))
    
    def set_password(self, password):
        """设置密码，自动加密"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def roles(self):
        """获取用户角色"""
        return [ur.role for ur in self.user_roles]
    
    @property
    def role(self):
        """获取用户第一个角色（兼容旧代码）"""
        roles = self.roles
        return roles[0].name if roles else 'user'

class Role(BaseModel):
    """角色模型"""
    __tablename__ = 'role'
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    is_system_role = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f'<Role {self.name}>'

class Permission(BaseModel):
    """权限模型"""
    __tablename__ = 'permission'
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    code = db.Column(db.String(50), nullable=False, unique=True, index=True)
    module = db.Column(db.String(50), index=True)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Permission {self.name}>'

class UserRole(BaseModel):
    """用户角色关联模型"""
    __tablename__ = 'user_role'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, index=True)
    
    user = db.relationship('User', backref=db.backref('user_roles', lazy=True))
    role = db.relationship('Role', backref=db.backref('user_roles', lazy=True))

class RolePermission(BaseModel):
    """角色权限关联模型"""
    __tablename__ = 'role_permission'
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, index=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), nullable=False, index=True)
    
    role = db.relationship('Role', backref=db.backref('role_permissions', lazy=True))
    permission = db.relationship('Permission', backref=db.backref('role_permissions', lazy=True))

class Supplier(BaseModel):
    """供应商模型"""
    __tablename__ = 'supplier'
    name = db.Column(db.String(100), nullable=False, index=True)
    code = db.Column(db.String(50), unique=True, index=True)
    contact_person = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    tax_id = db.Column(db.String(50))
    payment_terms = db.Column(db.Text)
    rating = db.Column(db.Numeric(3, 2))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<Supplier {self.name}>'

class IngredientCategory(BaseModel):
    """食材分类模型"""
    __tablename__ = 'ingredient_category'
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('ingredient_category.id'), nullable=True, index=True)
    
    def __repr__(self):
        return f'<IngredientCategory {self.name}>'

# 添加自引用关系
IngredientCategory.parent_category = db.relationship('IngredientCategory', backref=db.backref('subcategories', lazy=True), remote_side=[IngredientCategory.id])

class Ingredient(BaseModel):
    """食材模型"""
    __tablename__ = 'ingredient'
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('ingredient_category.id'), index=True)
    unit_of_measure = db.Column(db.String(20))
    current_stock = db.Column(db.Numeric(10, 3), default=0)
    minimum_stock = db.Column(db.Numeric(10, 3), default=0)
    maximum_stock = db.Column(db.Numeric(10, 3))
    reorder_point = db.Column(db.Numeric(10, 3))
    unit_cost = db.Column(db.Numeric(10, 2))
    nutrition_info = db.Column(db.JSON)
    calories_per_unit = db.Column(db.Numeric(8, 2))
    shelf_life_days = db.Column(db.Integer)
    storage_conditions = db.Column(db.JSON)
    image_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    category = db.relationship('IngredientCategory', backref=db.backref('ingredients', lazy=True))
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'

class PurchaseOrder(BaseModel):
    """采购订单模型"""
    __tablename__ = 'purchase_order'
    order_number = db.Column(db.String(50), unique=True, index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False, index=True)
    order_date = db.Column(db.Date, nullable=False, index=True)
    expected_delivery_date = db.Column(db.Date)
    actual_delivery_date = db.Column(db.Date)
    total_amount = db.Column(db.Numeric(12, 2), default=0)
    status = db.Column(db.String(20), default='draft', index=True)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    
    supplier = db.relationship('Supplier', backref=db.backref('purchase_orders', lazy=True))
    creator = db.relationship('User', foreign_keys=[created_by], backref=db.backref('created_purchase_orders', lazy=True))
    approver = db.relationship('User', foreign_keys=[approved_by], backref=db.backref('approved_purchase_orders', lazy=True))
    
    def __repr__(self):
        return f'<PurchaseOrder {self.order_number}>'

class PurchaseOrderItem(BaseModel):
    """采购订单详情模型"""
    __tablename__ = 'purchase_order_item'
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'), nullable=False, index=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False, index=True)
    quantity_ordered = db.Column(db.Numeric(10, 3), nullable=False)
    quantity_received = db.Column(db.Numeric(10, 3), default=0)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), default=0)
    batch_number = db.Column(db.String(100))
    expiry_date = db.Column(db.Date)
    
    purchase_order = db.relationship('PurchaseOrder', backref=db.backref('purchase_order_items', lazy=True))
    ingredient = db.relationship('Ingredient', backref=db.backref('purchase_order_items', lazy=True))
    
    def __repr__(self):
        return f'<PurchaseOrderItem Order:{self.purchase_order_id} Ingredient:{self.ingredient_id}>'

class DishIngredient(BaseModel):
    """菜品与食材的关联模型"""
    __tablename__ = 'dish_ingredient'
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False, index=True)
    quantity_required = db.Column(db.Numeric(10, 3), nullable=False)
    unit_of_measure = db.Column(db.String(20))
    notes = db.Column(db.Text)
    
    dish = db.relationship('Dish', backref=db.backref('dish_ingredients', lazy=True))
    ingredient = db.relationship('Ingredient', backref=db.backref('dish_ingredients', lazy=True))

class InventoryTransaction(BaseModel):
    """库存交易记录模型"""
    __tablename__ = 'inventory_transaction'
    transaction_type = db.Column(db.String(50), nullable=False, index=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False, index=True)
    quantity_change = db.Column(db.Numeric(10, 3), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2))
    total_value = db.Column(db.Numeric(10, 2))
    reference_id = db.Column(db.Integer)
    reference_type = db.Column(db.String(50))
    notes = db.Column(db.Text)
    performed_by = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    
    ingredient = db.relationship('Ingredient', backref=db.backref('inventory_transactions', lazy=True))
    performer = db.relationship('User', backref=db.backref('inventory_transactions', lazy=True))
    
    def __repr__(self):
        return f'<InventoryTransaction Type:{self.transaction_type} Ingredient:{self.ingredient_id}>'

class InventoryAlert(BaseModel):
    """库存告警模型"""
    __tablename__ = 'inventory_alert'
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False, index=True)
    alert_type = db.Column(db.String(50), nullable=False, index=True)
    current_value = db.Column(db.Numeric(10, 3))
    threshold_value = db.Column(db.Numeric(10, 3))
    message = db.Column(db.Text)
    severity = db.Column(db.String(20), default='warning', index=True)
    status = db.Column(db.String(20), default='active', index=True)
    acknowledged_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    
    ingredient = db.relationship('Ingredient', backref=db.backref('inventory_alerts', lazy=True))
    acknowledger = db.relationship('User', backref=db.backref('acknowledged_inventory_alerts', lazy=True))
    
    def __repr__(self):
        return f'<InventoryAlert Type:{self.alert_type} Status:{self.status}>'

class CustomerOrder(BaseModel):
    """客户订单模型"""
    __tablename__ = 'customer_order'
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    order_date = db.Column(db.DateTime, nullable=False, index=True)
    delivery_date = db.Column(db.Date)
    delivery_time_slot = db.Column(db.String(50))
    delivery_address = db.Column(db.Text)
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    total_items = db.Column(db.Integer, default=0)
    subtotal_amount = db.Column(db.Numeric(12, 2), default=0)
    tax_amount = db.Column(db.Numeric(12, 2), default=0)
    delivery_fee = db.Column(db.Numeric(10, 2), default=0)
    total_amount = db.Column(db.Numeric(12, 2), default=0)
    payment_method = db.Column(db.String(20))
    payment_status = db.Column(db.String(20), default='pending', index=True)
    order_status = db.Column(db.String(20), default='pending', index=True)
    notes = db.Column(db.Text)
    
    customer = db.relationship('Customer', backref=db.backref('customer_orders', lazy=True))

class OrderItem(BaseModel):
    """订单详情模型"""
    __tablename__ = 'order_item'
    order_id = db.Column(db.Integer, db.ForeignKey('customer_order.id'), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), default=0)
    total_price = db.Column(db.Numeric(10, 2), default=0)
    special_instructions = db.Column(db.Text)
    preparation_status = db.Column(db.String(20), default='pending', index=True)
    
    order = db.relationship('CustomerOrder', backref=db.backref('order_items', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('order_items', lazy=True))

class DeliverySchedule(BaseModel):
    """配送计划模型"""
    __tablename__ = 'delivery_schedule'
    date = db.Column(db.Date, nullable=False, index=True)
    time_slot = db.Column(db.String(50))
    total_orders = db.Column(db.Integer, default=0)
    total_customers = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending', index=True)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<DeliverySchedule {self.date}>'

class DeliveryAssignment(BaseModel):
    """配送分配模型"""
    __tablename__ = 'delivery_assignment'
    schedule_id = db.Column(db.Integer, db.ForeignKey('delivery_schedule.id'), nullable=False, index=True)
    delivery_staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    route_id = db.Column(db.Integer, db.ForeignKey('delivery_route.id'), nullable=True, index=True)
    total_assignments = db.Column(db.Integer, default=0)
    estimated_start_time = db.Column(db.DateTime)
    estimated_end_time = db.Column(db.DateTime)
    actual_start_time = db.Column(db.DateTime)
    actual_end_time = db.Column(db.DateTime)
    vehicle_type = db.Column(db.String(50))
    vehicle_number = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending', index=True)
    
    schedule = db.relationship('DeliverySchedule', backref=db.backref('delivery_assignments', lazy=True))
    delivery_staff = db.relationship('User', backref=db.backref('delivery_assignments', lazy=True))
    route = db.relationship('DeliveryRoute', backref=db.backref('delivery_assignments', lazy=True))
    
    def __repr__(self):
        return f'<DeliveryAssignment Schedule:{self.schedule_id} Staff:{self.delivery_staff_id}>'

class DeliveryRoute(BaseModel):
    """配送路线模型"""
    __tablename__ = 'delivery_route'
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    zone = db.Column(db.String(50))
    route_sequence = db.Column(db.JSON)
    estimated_distance_km = db.Column(db.Numeric(6, 2))
    estimated_duration_minutes = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<DeliveryRoute {self.name}>'

class DeliveryStatusUpdate(BaseModel):
    """配送状态更新模型"""
    __tablename__ = 'delivery_status_update'
    assignment_id = db.Column(db.Integer, db.ForeignKey('delivery_assignment.id'), nullable=False, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('customer_order.id'), nullable=True, index=True)
    status = db.Column(db.String(50), nullable=False, index=True)
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    notes = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    
    assignment = db.relationship('DeliveryAssignment', backref=db.backref('delivery_status_updates', lazy=True))
    order = db.relationship('CustomerOrder', backref=db.backref('delivery_status_updates', lazy=True))
    updater = db.relationship('User', backref=db.backref('delivery_status_updates', lazy=True))
    
    def __repr__(self):
        return f'<DeliveryStatusUpdate Assignment:{self.assignment_id} Status:{self.status}>'


class ServiceCategory(BaseModel):
    """服务分类模型"""
    __tablename__ = 'service_category'
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    icon_url = db.Column(db.String(500))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<ServiceCategory {self.name}>'

class ServiceItem(BaseModel):
    """服务项目模型"""
    __tablename__ = 'service_item'
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), index=True)
    duration_minutes = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2), default=0)
    discounted_price = db.Column(db.Numeric(10, 2))
    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    
    category = db.relationship('ServiceCategory', backref=db.backref('service_items', lazy=True))
    
    def __repr__(self):
        return f'<ServiceItem {self.name}>'

class ServicePackage(BaseModel):
    """服务套餐模型"""
    __tablename__ = 'service_package'
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    duration_days = db.Column(db.Integer)
    total_price = db.Column(db.Numeric(10, 2), default=0)
    discounted_price = db.Column(db.Numeric(10, 2))
    services_included = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<ServicePackage {self.name}>'

class ServicePackageItem(BaseModel):
    """服务套餐项目关联模型"""
    __tablename__ = 'service_package_item'
    package_id = db.Column(db.Integer, db.ForeignKey('service_package.id'), nullable=False, index=True)
    service_item_id = db.Column(db.Integer, db.ForeignKey('service_item.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, default=1)
    frequency = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    package = db.relationship('ServicePackage', backref=db.backref('service_package_items', lazy=True))
    service_item = db.relationship('ServiceItem', backref=db.backref('service_package_items', lazy=True))
    
    def __repr__(self):
        return f'<ServicePackageItem Package:{self.package_id} Service:{self.service_item_id}>'

class ServiceBooking(BaseModel):
    """服务预约模型"""
    __tablename__ = 'service_booking'
    booking_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    service_item_id = db.Column(db.Integer, db.ForeignKey('service_item.id'), nullable=True, index=True)
    package_id = db.Column(db.Integer, db.ForeignKey('service_package.id'), nullable=True, index=True)
    booking_date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    duration_minutes = db.Column(db.Integer)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    status = db.Column(db.String(20), default='pending', index=True)
    notes = db.Column(db.Text)
    cancellation_reason = db.Column(db.Text)
    
    customer = db.relationship('Customer', backref=db.backref('service_bookings', lazy=True))
    service_item = db.relationship('ServiceItem', backref=db.backref('service_bookings', lazy=True))
    package = db.relationship('ServicePackage', backref=db.backref('service_bookings', lazy=True))
    assigned_staff = db.relationship('User', backref=db.backref('assigned_service_bookings', lazy=True))
    
    def __repr__(self):
        return f'<ServiceBooking {self.booking_number}>'

class ServiceFeedback(BaseModel):
    """服务反馈模型"""
    __tablename__ = 'service_feedback'
    booking_id = db.Column(db.Integer, db.ForeignKey('service_booking.id'), nullable=False, unique=True, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    suggestions = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=False, nullable=False)
    
    booking = db.relationship('ServiceBooking', backref=db.backref('feedback', uselist=False, lazy=True))
    customer = db.relationship('Customer', backref=db.backref('service_feedbacks', lazy=True))
    
    def __repr__(self):
        return f'<ServiceFeedback Booking:{self.booking_id} Rating:{self.rating}>'

class ConfinementMealPlan(BaseModel):
    """月子餐计划模型"""
    __tablename__ = 'confinement_meal_plan'
    plan_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    start_date = db.Column(db.Date, nullable=False, index=True)
    end_date = db.Column(db.Date, index=True)
    total_days = db.Column(db.Integer)
    total_weeks = db.Column(db.Integer)
    meal_plan_type = db.Column(db.String(20), index=True)
    total_calories_per_day = db.Column(db.Numeric(8, 2))
    total_price = db.Column(db.Numeric(12, 2), default=0)
    discount_amount = db.Column(db.Numeric(10, 2))
    final_price = db.Column(db.Numeric(12, 2), default=0)
    status = db.Column(db.String(20), default='draft', index=True)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    
    customer = db.relationship('Customer', backref=db.backref('confinement_meal_plans', lazy=True))
    creator = db.relationship('User', foreign_keys=[created_by], backref=db.backref('created_confinement_meal_plans', lazy=True))
    approver = db.relationship('User', foreign_keys=[approved_by], backref=db.backref('approved_confinement_meal_plans', lazy=True))
    
    def __repr__(self):
        return f'<ConfinementMealPlan {self.plan_number}>'

class ConfinementWeekPlan(BaseModel):
    """月子餐周计划模型"""
    __tablename__ = 'confinement_week_plan'
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('confinement_meal_plan.id'), nullable=False, index=True)
    week_number = db.Column(db.Integer, nullable=False, index=True)
    focus_area = db.Column(db.String(100))
    nutrition_goals = db.Column(db.JSON)
    avoid_foods = db.Column(db.JSON)
    recommended_foods = db.Column(db.JSON)
    notes = db.Column(db.Text)
    
    meal_plan = db.relationship('ConfinementMealPlan', backref=db.backref('week_plans', lazy=True))
    
    def __repr__(self):
        return f'<ConfinementWeekPlan Plan:{self.meal_plan_id} Week:{self.week_number}>'

class ConfinementDayPlan(BaseModel):
    """月子餐日计划模型"""
    __tablename__ = 'confinement_day_plan'
    week_plan_id = db.Column(db.Integer, db.ForeignKey('confinement_week_plan.id'), nullable=False, index=True)
    day_number = db.Column(db.Integer, nullable=False, index=True)
    date = db.Column(db.Date)
    total_calories = db.Column(db.Numeric(8, 2))
    nutrition_summary = db.Column(db.JSON)
    special_notes = db.Column(db.Text)
    
    week_plan = db.relationship('ConfinementWeekPlan', backref=db.backref('day_plans', lazy=True))
    
    def __repr__(self):
        return f'<ConfinementDayPlan Week:{self.week_plan_id} Day:{self.day_number}>'

class ConfinementMealItem(BaseModel):
    """月子餐单项模型"""
    __tablename__ = 'confinement_meal_item'
    day_plan_id = db.Column(db.Integer, db.ForeignKey('confinement_day_plan.id'), nullable=False, index=True)
    meal_type = db.Column(db.String(50), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    serving_time = db.Column(db.Time)
    quantity = db.Column(db.Integer, default=1)
    calories = db.Column(db.Numeric(8, 2))
    nutrition_details = db.Column(db.JSON)
    special_instructions = db.Column(db.Text)
    
    day_plan = db.relationship('ConfinementDayPlan', backref=db.backref('meal_items', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('confinement_meal_items', lazy=True))
    
    def __repr__(self):
        return f'<ConfinementMealItem Day:{self.day_plan_id} Type:{self.meal_type} Dish:{self.dish_id}>'

class WeChatUser(BaseModel):
    """微信用户模型"""
    __tablename__ = 'wechat_user'
    openid = db.Column(db.String(100), nullable=False, unique=True, index=True)
    unionid = db.Column(db.String(100), unique=True, index=True)
    nickname = db.Column(db.String(100))
    avatar_url = db.Column(db.String(500))
    gender = db.Column(db.Integer)
    country = db.Column(db.String(50))
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    last_login_at = db.Column(db.DateTime, index=True)
    session_key = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<WeChatUser {self.nickname}>'

class CustomerWeChatLink(BaseModel):
    """客户微信关联模型"""
    __tablename__ = 'customer_wechat_link'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, unique=True, index=True)
    wechat_user_id = db.Column(db.Integer, db.ForeignKey('wechat_user.id'), nullable=False, unique=True, index=True)
    linked_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    
    customer = db.relationship('Customer', backref=db.backref('wechat_link', uselist=False, lazy=True))
    wechat_user = db.relationship('WeChatUser', backref=db.backref('customer_link', uselist=False, lazy=True))
    
    def __repr__(self):
        return f'<CustomerWeChatLink Customer:{self.customer_id} WeChat:{self.wechat_user_id}>'


class AIAnalysisJob(BaseModel):
    """AI分析任务模型"""
    __tablename__ = 'ai_analysis_job'
    job_type = db.Column(db.String(50), nullable=False, index=True)
    parameters = db.Column(db.JSON)
    status = db.Column(db.String(20), default='pending', index=True)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    result_summary = db.Column(db.Text)
    error_message = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    
    creator = db.relationship('User', backref=db.backref('created_ai_analysis_jobs', lazy=True))
    
    def __repr__(self):
        return f'<AIAnalysisJob Type:{self.job_type} Status:{self.status}>'

class AIAnalysisResult(BaseModel):
    """AI分析结果模型"""
    __tablename__ = 'ai_analysis_result'
    job_id = db.Column(db.Integer, db.ForeignKey('ai_analysis_job.id'), nullable=False, index=True)
    analysis_type = db.Column(db.String(50), nullable=False, index=True)
    input_data = db.Column(db.JSON)
    result_data = db.Column(db.JSON)
    insights = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    confidence_score = db.Column(db.Numeric(5, 4))
    visualization_url = db.Column(db.String(500))
    
    job = db.relationship('AIAnalysisJob', backref=db.backref('analysis_results', lazy=True))
    
    def __repr__(self):
        return f'<AIAnalysisResult Type:{self.analysis_type} Job:{self.job_id}>'

class ReportTemplate(BaseModel):
    """报告模板模型"""
    __tablename__ = 'report_template'
    template_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    template_type = db.Column(db.String(20), index=True)
    description = db.Column(db.Text)
    template_content = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<ReportTemplate {self.template_name}>'

class GeneratedReport(BaseModel):
    """生成报告模型"""
    __tablename__ = 'generated_report'
    report_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    template_id = db.Column(db.Integer, db.ForeignKey('report_template.id'), nullable=False, index=True)
    report_type = db.Column(db.String(50), index=True)
    period_start = db.Column(db.Date)
    period_end = db.Column(db.Date)
    report_data = db.Column(db.JSON)
    insights = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    file_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='generated', index=True)
    generated_by = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    
    template = db.relationship('ReportTemplate', backref=db.backref('generated_reports', lazy=True))
    generator = db.relationship('User', backref=db.backref('generated_reports', lazy=True))
    
    def __repr__(self):
        return f'<GeneratedReport {self.report_number}>'

class AlertRule(BaseModel):
    """告警规则模型"""
    __tablename__ = 'alert_rule'
    rule_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    rule_type = db.Column(db.String(50), index=True)
    condition = db.Column(db.JSON)
    severity = db.Column(db.String(20), default='warning', index=True)
    notification_channels = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<AlertRule {self.rule_name}>'

class Alert(BaseModel):
    """告警模型"""
    __tablename__ = 'alert'
    alert_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('alert_rule.id'), index=True)
    entity_type = db.Column(db.String(50), index=True)
    entity_id = db.Column(db.Integer, index=True)
    entity_name = db.Column(db.String(100), index=True)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='medium', index=True)
    data = db.Column(db.JSON)
    status = db.Column(db.String(20), default='active', index=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    resolved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    resolution_notes = db.Column(db.Text)
    acknowledged_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    
    rule = db.relationship('AlertRule', backref=db.backref('alerts', lazy=True))
    resolver = db.relationship('User', foreign_keys=[resolved_by], backref=db.backref('resolved_alerts', lazy=True))
    acknowledger = db.relationship('User', foreign_keys=[acknowledged_by], backref=db.backref('acknowledged_alerts', lazy=True))
    
    def __repr__(self):
        return f'<Alert {self.alert_code} - {self.status}>'
