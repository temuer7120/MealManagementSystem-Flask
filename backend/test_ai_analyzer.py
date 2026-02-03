from app import create_app
from utils.ai_analyzer import AIAnalyzer

# 创建Flask应用实例
app = create_app()

# 直接测试AI分析器
def test_ai_analyzer():
    with app.app_context():
        analyzer = AIAnalyzer()
        
        print("=== Testing Dish Quality Analysis ===")
        dish_quality_result = analyzer.analyze_dish_quality(days=30)
        print(f"Total Dishes: {dish_quality_result.get('total_dishes')}")
        print("Top Performing Dishes:")
        for dish in dish_quality_result.get('top_performing_dishes', [])[:3]:
            print(f"  - {dish.get('dish_name')}: {dish.get('quality_score')}")
        print("Recommendations:")
        for rec in dish_quality_result.get('recommendations', []):
            print(f"  - {rec}")
        print()
        
        print("=== Testing Cost Effectiveness Analysis ===")
        cost_effectiveness_result = analyzer.analyze_cost_effectiveness()
        print(f"Total Dishes: {cost_effectiveness_result.get('total_dishes')}")
        print("Top Cost Effective Dishes:")
        for dish in cost_effectiveness_result.get('top_cost_effective_dishes', [])[:3]:
            print(f"  - {dish.get('dish_name')}: {dish.get('cost_effectiveness')}")
        print("Recommendations:")
        for rec in cost_effectiveness_result.get('recommendations', []):
            print(f"  - {rec}")
        print()
        
        print("=== Testing Sales Performance Analysis ===")
        sales_performance_result = analyzer.analyze_sales_performance(days=30)
        print(f"Total Orders: {sales_performance_result.get('total_orders')}")
        print(f"Total Sales Amount: {sales_performance_result.get('total_sales_amount')}")
        print("Top Selling Dishes:")
        for dish in sales_performance_result.get('top_selling_dishes', [])[:3]:
            print(f"  - {dish.get('dish_name')}: {dish.get('total_amount')}")
        print("Recommendations:")
        for rec in sales_performance_result.get('recommendations', []):
            print(f"  - {rec}")
        print()
        
        print("=== Testing Nutritional Balance Analysis ===")
        nutritional_balance_result = analyzer.analyze_nutritional_balance()
        print(f"Total Dishes: {nutritional_balance_result.get('total_dishes')}")
        print("Most Balanced Dishes:")
        for dish in nutritional_balance_result.get('most_balanced_dishes', [])[:3]:
            print(f"  - {dish.get('dish_name')}: {dish.get('balance_score')}")
        print("Recommendations:")
        for rec in nutritional_balance_result.get('recommendations', []):
            print(f"  - {rec}")
        print()

if __name__ == "__main__":
    test_ai_analyzer()
