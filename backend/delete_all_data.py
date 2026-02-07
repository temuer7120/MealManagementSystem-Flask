from extensions import db
from models import (
    # 关联表和子表（先删除）
    ServiceFeedback, ServicePackageItem, ServiceBooking,
    OrderItem, DeliveryStatusUpdate, DeliveryAssignment,
    CustomerWeChatLink, CustomerMenuSelection, CustomerDietaryPreference,
    ConfinementMealItem, ConfinementDayPlan, ConfinementWeekPlan, ConfinementMealPlan,
    AIAnalysisResult, AIAnalysisJob, GeneratedReport, Alert,
    InventoryAlert, InventoryTransaction, DishIngredient, PurchaseOrderItem, PurchaseOrder,
    MenuDish, DailyMenuDish, UserRole, RolePermission,
    # 父表（后删除）
    ServicePackage, ServiceItem, ServiceCategory,
    CustomerOrder, DeliverySchedule, DeliveryRoute, WeChatUser, Customer,
    Dish, MenuCategory, Menu, DailyMenu,
    Ingredient, IngredientCategory, Supplier,
    User, Role, Permission,
    ReportTemplate, AlertRule
)

def delete_all_data():
    """删除数据库中所有表的数据，按外键依赖的反向顺序执行"""
    try:
        # 1. 删除关联表和子表数据
        tables_to_truncate = [
            ServiceFeedback, ServicePackageItem, ServiceBooking,
            OrderItem, DeliveryStatusUpdate, DeliveryAssignment,
            CustomerWeChatLink, CustomerMenuSelection, CustomerDietaryPreference,
            ConfinementMealItem, ConfinementDayPlan, ConfinementWeekPlan, ConfinementMealPlan,
            AIAnalysisResult, AIAnalysisJob, GeneratedReport, Alert,
            InventoryAlert, InventoryTransaction, DishIngredient, PurchaseOrderItem, PurchaseOrder,
            MenuDish, DailyMenuDish, UserRole, RolePermission,
            # 2. 删除父表数据
            ServicePackage, ServiceItem, ServiceCategory,
            CustomerOrder, DeliverySchedule, DeliveryRoute, WeChatUser, Customer,
            Dish, MenuCategory, Menu, DailyMenu,
            Ingredient, IngredientCategory, Supplier,
            User, Role, Permission,
            ReportTemplate, AlertRule
        ]
        
        for table in tables_to_truncate:
            try:
                # 使用 TRUNCATE 清空表数据，重置自增ID
                db.session.query(table).delete()
                print(f"清空表 {table.__tablename__} 数据成功")
            except Exception as e:
                print(f"清空表 {table.__tablename__} 数据失败: {e}")
        
        # 提交事务
        db.session.commit()
        print("\n所有表数据删除完成！")
        
    except Exception as e:
        print(f"删除数据时发生错误: {e}")
        db.session.rollback()

if __name__ == "__main__":
    from app import app
    with app.app_context():
        delete_all_data()
