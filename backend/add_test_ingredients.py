#!/usr/bin/env python3
"""
添加测试食材数据到数据库
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Ingredient, IngredientCategory

# 测试食材数据
test_ingredients = [
    {
        'name': '西红柿',
        'description': '新鲜的西红柿，富含维生素C',
        'category_id': None,
        'unit_of_measure': '个',
        'current_stock': 50,
        'minimum_stock': 10,
        'maximum_stock': 100,
        'reorder_point': 20,
        'unit_cost': 2.5,
        'nutrition_info': {'蛋白质': '0.9g', '碳水化合物': '4g', '脂肪': '0.2g'},
        'calories_per_unit': 18,
        'shelf_life_days': 7,
        'storage_conditions': {'温度': '2-8°C', '湿度': '85-90%'},
        'image_url': None,
        'is_active': True
    },
    {
        'name': '鸡蛋',
        'description': '新鲜鸡蛋，富含蛋白质',
        'category_id': None,
        'unit_of_measure': '个',
        'current_stock': 100,
        'minimum_stock': 30,
        'maximum_stock': 200,
        'reorder_point': 50,
        'unit_cost': 1.2,
        'nutrition_info': {'蛋白质': '6.3g', '碳水化合物': '0.6g', '脂肪': '5.3g'},
        'calories_per_unit': 78,
        'shelf_life_days': 30,
        'storage_conditions': {'温度': '2-8°C', '湿度': '70-80%'},
        'image_url': None,
        'is_active': True
    },
    {
        'name': '大米',
        'description': '优质大米，口感香糯',
        'category_id': None,
        'unit_of_measure': 'kg',
        'current_stock': 20,
        'minimum_stock': 5,
        'maximum_stock': 50,
        'reorder_point': 10,
        'unit_cost': 6.5,
        'nutrition_info': {'蛋白质': '7.5g', '碳水化合物': '77g', '脂肪': '0.9g'},
        'calories_per_unit': 346,
        'shelf_life_days': 180,
        'storage_conditions': {'温度': '15-25°C', '湿度': '50-60%'},
        'image_url': None,
        'is_active': True
    },
    {
        'name': '青菜',
        'description': '新鲜青菜，富含维生素',
        'category_id': None,
        'unit_of_measure': '斤',
        'current_stock': 30,
        'minimum_stock': 5,
        'maximum_stock': 50,
        'reorder_point': 10,
        'unit_cost': 3.8,
        'nutrition_info': {'蛋白质': '2.6g', '碳水化合物': '2.8g', '脂肪': '0.3g'},
        'calories_per_unit': 23,
        'shelf_life_days': 3,
        'storage_conditions': {'温度': '0-4°C', '湿度': '90-95%'},
        'image_url': None,
        'is_active': True
    },
    {
        'name': '猪肉',
        'description': '新鲜猪肉，肥瘦相间',
        'category_id': None,
        'unit_of_measure': '斤',
        'current_stock': 15,
        'minimum_stock': 5,
        'maximum_stock': 30,
        'reorder_point': 8,
        'unit_cost': 28.5,
        'nutrition_info': {'蛋白质': '20.3g', '碳水化合物': '1.1g', '脂肪': '10.8g'},
        'calories_per_unit': 189,
        'shelf_life_days': 3,
        'storage_conditions': {'温度': '-18°C以下', '湿度': '75-85%'},
        'image_url': None,
        'is_active': True
    }
]

def add_test_data():
    """添加测试数据到数据库"""
    with app.app_context():
        # 检查是否已有食材数据
        existing_ingredients = Ingredient.query.count()
        if existing_ingredients > 0:
            print(f"数据库中已有 {existing_ingredients} 条食材数据，跳过添加")
            return
        
        print("开始添加测试食材数据...")
        
        # 添加测试食材
        for ingredient_data in test_ingredients:
            try:
                # 检查是否已存在同名食材
                existing = Ingredient.query.filter_by(name=ingredient_data['name']).first()
                if existing:
                    print(f"食材 {ingredient_data['name']} 已存在，跳过")
                    continue
                
                # 创建新食材
                ingredient = Ingredient(**ingredient_data)
                db.session.add(ingredient)
                print(f"添加食材: {ingredient_data['name']}")
            except Exception as e:
                print(f"添加食材 {ingredient_data['name']} 失败: {e}")
                db.session.rollback()
                continue
        
        # 提交事务
        try:
            db.session.commit()
            print(f"成功添加 {len(test_ingredients)} 条食材数据")
        except Exception as e:
            print(f"提交事务失败: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_test_data()
