from models import Dish, OrderItem, CustomerOrder, Ingredient, DishIngredient, ServiceFeedback
from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd
from collections import defaultdict

class AIAnalyzer:
    """AI数据分析器"""
    
    def analyze_dish_quality(self, days=30):
        """分析菜品品质"""
        # 计算开始日期
        start_date = datetime.now() - timedelta(days=days)
        
        # 获取指定时间范围内的订单
        orders = CustomerOrder.query.filter(CustomerOrder.order_date >= start_date.date()).all()
        
        # 统计每个菜品的销售情况和评价
        dish_stats = defaultdict(lambda: {
            'sales_count': 0,
            'total_amount': 0,
            'feedback_count': 0,
            'total_rating': 0
        })
        
        # 统计销售数据
        for order in orders:
            for item in order.order_items:
                dish_id = item.dish_id
                dish_stats[dish_id]['sales_count'] += item.quantity
                dish_stats[dish_id]['total_amount'] += item.price * item.quantity
        
        # 这里可以添加客户评价数据的统计
        # 假设我们有一个评价系统，这里暂时跳过
        
        # 计算每个菜品的品质得分
        quality_results = []
        for dish_id, stats in dish_stats.items():
            dish = Dish.query.get(dish_id)
            if not dish:
                continue
            
            # 计算基础得分
            sales_score = min(stats['sales_count'] / 10, 5)  # 销售数量得分
            
            # 计算平均评分（如果有）
            avg_rating = stats['total_rating'] / stats['feedback_count'] if stats['feedback_count'] > 0 else 3.5
            
            # 综合得分
            quality_score = (sales_score * 0.6 + avg_rating * 0.4) / 5
            
            quality_results.append({
                'dish_id': dish_id,
                'dish_name': dish.name,
                'category': dish.category.name if dish.category else '未知',
                'sales_count': stats['sales_count'],
                'total_amount': stats['total_amount'],
                'avg_rating': avg_rating,
                'quality_score': round(quality_score, 2)
            })
        
        # 按品质得分排序
        quality_results.sort(key=lambda x: x['quality_score'], reverse=True)
        
        # 生成建议
        recommendations = self._generate_quality_recommendations(quality_results)
        
        return {
            'analysis_type': 'dish_quality',
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'total_dishes': len(quality_results),
            'top_performing_dishes': quality_results[:5],
            'bottom_performing_dishes': quality_results[-5:],
            'recommendations': recommendations
        }
    
    def analyze_cost_effectiveness(self):
        """分析菜品性价比"""
        # 获取所有菜品
        dishes = Dish.query.all()
        
        # 分析每个菜品的成本和收益
        cost_effectiveness_results = []
        
        for dish in dishes:
            # 计算菜品成本
            total_cost = 0
            dish_ingredients = DishIngredient.query.filter_by(dish_id=dish.id).all()
            
            for di in dish_ingredients:
                ingredient = Ingredient.query.get(di.ingredient_id)
                if ingredient:
                    total_cost += ingredient.stock * di.quantity  # 这里简化计算，实际应该使用成本价格
            
            # 计算菜品收益
            total_revenue = 0
            sales_count = 0
            
            order_items = OrderItem.query.filter_by(dish_id=dish.id).all()
            for item in order_items:
                total_revenue += item.price * item.quantity
                sales_count += item.quantity
            
            # 计算性价比
            if total_cost > 0:
                profit_margin = (total_revenue - total_cost) / total_revenue if total_revenue > 0 else 0
                cost_effectiveness = profit_margin * (sales_count / max(sales_count, 1))
            else:
                profit_margin = 0
                cost_effectiveness = 0
            
            cost_effectiveness_results.append({
                'dish_id': dish.id,
                'dish_name': dish.name,
                'category': dish.category.name if dish.category else '未知',
                'total_cost': round(total_cost, 2),
                'total_revenue': round(total_revenue, 2),
                'sales_count': sales_count,
                'profit_margin': round(profit_margin, 2),
                'cost_effectiveness': round(cost_effectiveness, 2)
            })
        
        # 按性价比排序
        cost_effectiveness_results.sort(key=lambda x: x['cost_effectiveness'], reverse=True)
        
        # 生成建议
        recommendations = self._generate_cost_effectiveness_recommendations(cost_effectiveness_results)
        
        return {
            'analysis_type': 'cost_effectiveness',
            'total_dishes': len(cost_effectiveness_results),
            'top_cost_effective_dishes': cost_effectiveness_results[:5],
            'bottom_cost_effective_dishes': cost_effectiveness_results[-5:],
            'recommendations': recommendations
        }
    
    def analyze_sales_performance(self, days=30):
        """分析销售表现"""
        # 计算开始日期
        start_date = datetime.now() - timedelta(days=days)
        
        # 获取指定时间范围内的订单
        orders = CustomerOrder.query.filter(CustomerOrder.order_date >= start_date.date()).all()
        
        # 统计销售数据
        sales_by_dish = defaultdict(lambda: {
            'sales_count': 0,
            'total_amount': 0
        })
        
        sales_by_category = defaultdict(lambda: {
            'sales_count': 0,
            'total_amount': 0
        })
        
        sales_by_date = defaultdict(lambda: {
            'sales_count': 0,
            'total_amount': 0
        })
        
        for order in orders:
            order_date = order.order_date.strftime('%Y-%m-%d')
            sales_by_date[order_date]['sales_count'] += 1
            sales_by_date[order_date]['total_amount'] += order.total_amount
            
            for item in order.order_items:
                dish = item.dish
                if dish:
                    # 按菜品统计
                    sales_by_dish[dish.id]['sales_count'] += item.quantity
                    sales_by_dish[dish.id]['total_amount'] += item.price * item.quantity
                    
                    # 按分类统计
                    category_id = dish.category_id
                    if category_id:
                        category = dish.category
                        if category:
                            sales_by_category[category.name]['sales_count'] += item.quantity
                            sales_by_category[category.name]['total_amount'] += item.price * item.quantity
        
        # 转换为列表格式
        dish_sales = []
        for dish_id, stats in sales_by_dish.items():
            dish = Dish.query.get(dish_id)
            if dish:
                dish_sales.append({
                    'dish_id': dish_id,
                    'dish_name': dish.name,
                    'category': dish.category.name if dish.category else '未知',
                    'sales_count': stats['sales_count'],
                    'total_amount': stats['total_amount']
                })
        
        category_sales = []
        for category_name, stats in sales_by_category.items():
            category_sales.append({
                'category_name': category_name,
                'sales_count': stats['sales_count'],
                'total_amount': stats['total_amount']
            })
        
        date_sales = []
        for date, stats in sorted(sales_by_date.items()):
            date_sales.append({
                'date': date,
                'sales_count': stats['sales_count'],
                'total_amount': stats['total_amount']
            })
        
        # 排序
        dish_sales.sort(key=lambda x: x['total_amount'], reverse=True)
        category_sales.sort(key=lambda x: x['total_amount'], reverse=True)
        
        # 生成建议
        recommendations = self._generate_sales_recommendations(dish_sales, category_sales, date_sales)
        
        return {
            'analysis_type': 'sales_performance',
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'total_orders': len(orders),
            'total_sales_amount': sum(order.total_amount for order in orders),
            'top_selling_dishes': dish_sales[:5],
            'top_selling_categories': category_sales[:3],
            'sales_trend': date_sales,
            'recommendations': recommendations
        }
    
    def analyze_nutritional_balance(self):
        """分析营养均衡性"""
        # 获取所有菜品
        dishes = Dish.query.all()
        
        # 分析每个菜品的营养成分
        # 这里简化处理，实际应该根据食材计算营养成分
        nutritional_results = []
        
        for dish in dishes:
            # 假设我们有一个营养成分计算函数
            nutrition = self._calculate_nutrition(dish)
            
            nutritional_results.append({
                'dish_id': dish.id,
                'dish_name': dish.name,
                'category': dish.category.name if dish.category else '未知',
                'calories': nutrition['calories'],
                'protein': nutrition['protein'],
                'carbohydrates': nutrition['carbohydrates'],
                'fat': nutrition['fat'],
                'fiber': nutrition['fiber'],
                'balance_score': nutrition['balance_score']
            })
        
        # 按营养均衡得分排序
        nutritional_results.sort(key=lambda x: x['balance_score'], reverse=True)
        
        # 生成建议
        recommendations = self._generate_nutritional_recommendations(nutritional_results)
        
        return {
            'analysis_type': 'nutritional_balance',
            'total_dishes': len(nutritional_results),
            'most_balanced_dishes': nutritional_results[:5],
            'least_balanced_dishes': nutritional_results[-5:],
            'recommendations': recommendations
        }
    
    def _calculate_nutrition(self, dish):
        """计算菜品的营养成分"""
        # 这里简化处理，实际应该根据食材计算营养成分
        # 假设每个菜品都有一些基础营养成分
        base_nutrition = {
            'calories': 200 + np.random.randint(0, 300),
            'protein': 10 + np.random.randint(0, 20),
            'carbohydrates': 20 + np.random.randint(0, 30),
            'fat': 5 + np.random.randint(0, 15),
            'fiber': 2 + np.random.randint(0, 8)
        }
        
        # 计算营养均衡得分
        # 基于蛋白质、碳水化合物和脂肪的比例
        protein_ratio = base_nutrition['protein'] * 4 / base_nutrition['calories']
        carb_ratio = base_nutrition['carbohydrates'] * 4 / base_nutrition['calories']
        fat_ratio = base_nutrition['fat'] * 9 / base_nutrition['calories']
        
        # 理想比例：蛋白质20-30%，碳水化合物45-65%，脂肪20-35%
        ideal_protein = 0.25
        ideal_carb = 0.55
        ideal_fat = 0.20
        
        # 计算得分
        balance_score = 1 - (
            abs(protein_ratio - ideal_protein) +
            abs(carb_ratio - ideal_carb) +
            abs(fat_ratio - ideal_fat)
        )
        balance_score = max(0, min(1, balance_score))
        
        base_nutrition['balance_score'] = round(balance_score, 2)
        return base_nutrition
    
    def _generate_quality_recommendations(self, quality_results):
        """生成品质分析建议"""
        recommendations = []
        
        # 分析表现最好的菜品
        top_dishes = quality_results[:3]
        if top_dishes:
            recommendations.append(f"推荐重点推广以下菜品：{', '.join([d['dish_name'] for d in top_dishes])}，这些菜品品质得分较高，深受顾客喜爱。")
        
        # 分析表现较差的菜品
        bottom_dishes = quality_results[-3:]
        if bottom_dishes:
            recommendations.append(f"建议改进以下菜品：{', '.join([d['dish_name'] for d in bottom_dishes])}，这些菜品品质得分较低，可能需要调整配方或提高质量。")
        
        return recommendations
    
    def _generate_cost_effectiveness_recommendations(self, cost_results):
        """生成性价比分析建议"""
        recommendations = []
        
        # 分析性价比高的菜品
        top_dishes = cost_results[:3]
        if top_dishes:
            recommendations.append(f"推荐重点推广以下高性价比菜品：{', '.join([d['dish_name'] for d in top_dishes])}，这些菜品利润率较高，销售情况良好。")
        
        # 分析性价比低的菜品
        bottom_dishes = cost_results[-3:]
        if bottom_dishes:
            recommendations.append(f"建议优化以下菜品的成本结构：{', '.join([d['dish_name'] for d in bottom_dishes])}，这些菜品性价比偏低，可能需要调整配方或定价。")
        
        return recommendations
    
    def _generate_sales_recommendations(self, dish_sales, category_sales, date_sales):
        """生成销售分析建议"""
        recommendations = []
        
        # 分析热销菜品
        top_dishes = dish_sales[:3]
        if top_dishes:
            recommendations.append(f"建议增加以下热销菜品的供应量：{', '.join([d['dish_name'] for d in top_dishes])}，这些菜品销量较高，市场需求大。")
        
        # 分析热销分类
        if category_sales:
            top_category = category_sales[0]
            recommendations.append(f"{top_category['category_name']}类菜品销量最高，建议丰富该类别菜品的种类，满足顾客需求。")
        
        # 分析销售趋势
        if len(date_sales) > 7:
            # 计算最近7天的平均销售额
            recent_sales = list(date_sales.values())[-7:]
            avg_recent_sales = sum(s['total_amount'] for s in recent_sales) / 7
            
            # 计算之前7天的平均销售额
            previous_sales = list(date_sales.values())[-14:-7]
            if previous_sales:
                avg_previous_sales = sum(s['total_amount'] for s in previous_sales) / 7
                
                if avg_recent_sales > avg_previous_sales:
                    growth_rate = (avg_recent_sales - avg_previous_sales) / avg_previous_sales
                    recommendations.append(f"销售额近期增长{round(growth_rate * 100, 2)}%，建议乘胜追击，推出更多促销活动。")
                else:
                    decline_rate = (avg_previous_sales - avg_recent_sales) / avg_previous_sales
                    recommendations.append(f"销售额近期下降{round(decline_rate * 100, 2)}%，建议分析原因，调整菜单或促销策略。")
        
        return recommendations
    
    def _generate_nutritional_recommendations(self, nutritional_results):
        """生成营养分析建议"""
        recommendations = []
        
        # 分析营养均衡的菜品
        balanced_dishes = nutritional_results[:3]
        if balanced_dishes:
            recommendations.append(f"推荐重点推广以下营养均衡的菜品：{', '.join([d['dish_name'] for d in balanced_dishes])}，这些菜品营养成分搭配合理，有利于健康。")
        
        # 分析营养不均衡的菜品
        unbalanced_dishes = nutritional_results[-3:]
        if unbalanced_dishes:
            recommendations.append(f"建议改进以下菜品的营养搭配：{', '.join([d['dish_name'] for d in unbalanced_dishes])}，这些菜品营养成分搭配不够合理，可能需要调整配方。")
        
        return recommendations
