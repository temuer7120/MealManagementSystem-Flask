from app import app, db
from models import *

with app.app_context():
    # 检查所有主要表的数据
    tables_to_check = [
        ('Customer', Customer),
        ('CustomerOrder', CustomerOrder),
        ('OrderItem', OrderItem),
        ('Dish', Dish),
        ('Ingredient', Ingredient),
        ('Menu', Menu),
        ('ServiceItem', ServiceItem),
        ('ServiceBooking', ServiceBooking),
        ('User', User),
        ('Role', Role)
    ]
    
    for table_name, table_model in tables_to_check:
        count = table_model.query.count()
        print(f'{table_name}: {count}')
        
        # 如果有数据，显示前5条
        if count > 0:
            items = table_model.query.limit(5).all()
            for item in items:
                print(f'  - {item}')
        print()
