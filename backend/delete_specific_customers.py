from app import app
from extensions import db
from models import (
    Customer, CustomerOrder, OrderItem, DeliveryStatusUpdate,
    ServiceBooking, ServiceFeedback,
    CustomerMenuSelection, CustomerDietaryPreference,
    ConfinementMealPlan, ConfinementWeekPlan, ConfinementDayPlan, ConfinementMealItem,
    CustomerWeChatLink
)

def delete_customer_data(customer_id):
    """删除指定客户及其相关数据"""
    try:
        # 1. 删除配送状态更新（关联订单）
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).all()
        for order in orders:
            # 删除订单状态更新
            status_updates = DeliveryStatusUpdate.query.filter_by(order_id=order.id).all()
            for update in status_updates:
                db.session.delete(update)
            # 删除订单详情
            order_items = OrderItem.query.filter_by(order_id=order.id).all()
            for item in order_items:
                db.session.delete(item)
            # 删除订单
            db.session.delete(order)
        
        # 2. 删除服务反馈和服务预订
        bookings = ServiceBooking.query.filter_by(customer_id=customer_id).all()
        for booking in bookings:
            # 删除服务反馈
            feedback = ServiceFeedback.query.filter_by(booking_id=booking.id).first()
            if feedback:
                db.session.delete(feedback)
            # 删除服务预订
            db.session.delete(booking)
        
        # 3. 删除客户菜单选择
        menu_selections = CustomerMenuSelection.query.filter_by(customer_id=customer_id).all()
        for selection in menu_selections:
            db.session.delete(selection)
        
        # 4. 删除客户饮食偏好
        dietary_preferences = CustomerDietaryPreference.query.filter_by(customer_id=customer_id).all()
        for preference in dietary_preferences:
            db.session.delete(preference)
        
        # 5. 删除月子餐相关数据
        meal_plans = ConfinementMealPlan.query.filter_by(customer_id=customer_id).all()
        for plan in meal_plans:
            # 删除周计划
            week_plans = ConfinementWeekPlan.query.filter_by(meal_plan_id=plan.id).all()
            for week_plan in week_plans:
                # 删除日计划
                day_plans = ConfinementDayPlan.query.filter_by(week_plan_id=week_plan.id).all()
                for day_plan in day_plans:
                    # 删除餐单项
                    meal_items = ConfinementMealItem.query.filter_by(day_plan_id=day_plan.id).all()
                    for item in meal_items:
                        db.session.delete(item)
                    db.session.delete(day_plan)
                db.session.delete(week_plan)
            db.session.delete(plan)
        
        # 6. 删除客户微信关联
        wechat_link = CustomerWeChatLink.query.filter_by(customer_id=customer_id).first()
        if wechat_link:
            db.session.delete(wechat_link)
        
        # 7. 删除客户本身
        customer = Customer.query.get(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return True, f'删除客户 {customer.name} 及其相关数据成功'
        else:
            return False, '未找到指定客户'
    
    except Exception as e:
        db.session.rollback()
        return False, f'删除失败: {str(e)}'

def delete_specific_customers():
    """删除张女士、李女士、王女士及其相关数据"""
    with app.app_context():
        # 客户ID列表（从界面看到的ID）
        customer_ids = [1, 2, 3]
        
        for customer_id in customer_ids:
            success, message = delete_customer_data(customer_id)
            print(f'客户ID {customer_id}: {message}')
        
        # 验证删除结果
        remaining_customers = Customer.query.filter(Customer.id.in_(customer_ids)).all()
        if not remaining_customers:
            print('\n删除完成：张女士、李女士、王女士及其相关数据已全部删除')
        else:
            print(f'\n删除后仍存在 {len(remaining_customers)} 条记录：')
            for customer in remaining_customers:
                print(f'  - ID: {customer.id}, 姓名: {customer.name}')

if __name__ == '__main__':
    delete_specific_customers()
