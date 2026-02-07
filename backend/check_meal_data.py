from app import app, db
from models import *

with app.app_context():
    # 检查菜品数据
    print('=== 菜品数据 ===')
    dishes = Dish.query.all()
    print(f'菜品数量: {len(dishes)}')
    for dish in dishes:
        print(f'  - {dish.name} (ID: {dish.id})')
    print()
    
    # 检查菜单数据
    print('=== 菜单数据 ===')
    menus = Menu.query.all()
    print(f'菜单数量: {len(menus)}')
    for menu in menus:
        print(f'  - {menu.name} (ID: {menu.id})')
    print()
    
    # 检查每日菜单数据
    print('=== 每日菜单数据 ===')
    daily_menus = DailyMenu.query.all()
    print(f'每日菜单数量: {len(daily_menus)}')
    for daily_menu in daily_menus:
        print(f'  - {daily_menu.date} (ID: {daily_menu.id}, 菜单: {daily_menu.menu.name if daily_menu.menu else "无"})')
    print()
    
    # 检查每日菜单菜品关联
    print('=== 每日菜单菜品关联 ===')
    daily_menu_dishes = DailyMenuDish.query.all()
    print(f'每日菜单菜品关联数量: {len(daily_menu_dishes)}')
    for dmd in daily_menu_dishes:
        dish_name = dmd.dish.name if dmd.dish else "无"
        daily_menu_date = dmd.daily_menu.date if dmd.daily_menu else "无"
        print(f'  - 日期: {daily_menu_date}, 菜品: {dish_name}, 餐次: {dmd.meal_time}')
    print()
    
    # 检查月子餐计划数据
    print('=== 月子餐计划数据 ===')
    confinement_plans = ConfinementMealPlan.query.all()
    print(f'月子餐计划数量: {len(confinement_plans)}')
    for plan in confinement_plans:
        print(f'  - {plan.name} (ID: {plan.id})')
    print()
    
    # 检查月子餐周计划数据
    print('=== 月子餐周计划数据 ===')
    week_plans = ConfinementWeekPlan.query.all()
    print(f'月子餐周计划数量: {len(week_plans)}')
    for plan in week_plans:
        print(f'  - 计划: {plan.meal_plan.name if plan.meal_plan else "无"}, 周数: {plan.week_number}')
    print()
    
    # 检查月子餐日计划数据
    print('=== 月子餐日计划数据 ===')
    day_plans = ConfinementDayPlan.query.all()
    print(f'月子餐日计划数量: {len(day_plans)}')
    for plan in day_plans:
        week_plan = plan.week_plan
        meal_plan = week_plan.meal_plan.name if week_plan and week_plan.meal_plan else "无"
        print(f'  - 计划: {meal_plan}, 周数: {week_plan.week_number if week_plan else "无"}, 天数: {plan.day_number}')
    print()
    
    # 检查月子餐菜品数据
    print('=== 月子餐菜品数据 ===')
    meal_items = ConfinementMealItem.query.all()
    print(f'月子餐菜品数量: {len(meal_items)}')
    for item in meal_items:
        dish_name = item.dish.name if item.dish else "无"
        day_plan = item.day_plan
        if day_plan:
            week_plan = day_plan.week_plan
            meal_plan = week_plan.meal_plan.name if week_plan and week_plan.meal_plan else "无"
            print(f'  - 计划: {meal_plan}, 周数: {week_plan.week_number if week_plan else "无"}, 天数: {day_plan.day_number}, 餐次: {item.meal_time}, 菜品: {dish_name}')
        else:
            print(f'  - 餐次: {item.meal_time}, 菜品: {dish_name}')
