from app import app, db
from models import ServiceCategory, ServiceItem
from datetime import datetime

# 母婴服务分类和项目数据
mother_baby_services = [
    {
        "category": "产后护理",
        "description": "产后妈妈的护理服务",
        "items": [
            {"name": "产后伤口护理", "description": "产后会阴或腹部伤口的护理", "duration_minutes": 30, "price": 200},
            {"name": "产后恶露观察", "description": "产后恶露的观察和记录", "duration_minutes": 20, "price": 150},
            {"name": "产后子宫复旧", "description": "产后子宫恢复情况的检查和护理", "duration_minutes": 30, "price": 250},
            {"name": "产后乳房护理", "description": "产后乳房护理和乳腺炎预防", "duration_minutes": 40, "price": 300},
            {"name": "产后形体恢复", "description": "产后形体恢复指导和练习", "duration_minutes": 60, "price": 400}
        ]
    },
    {
        "category": "新生儿护理",
        "description": "新生儿的护理服务",
        "items": [
            {"name": "新生儿洗澡", "description": "专业新生儿洗澡服务", "duration_minutes": 30, "price": 180},
            {"name": "新生儿抚触", "description": "专业新生儿抚触服务", "duration_minutes": 20, "price": 150},
            {"name": "新生儿脐带护理", "description": "新生儿脐带的护理", "duration_minutes": 15, "price": 120},
            {"name": "新生儿黄疸监测", "description": "新生儿黄疸的监测", "duration_minutes": 20, "price": 160},
            {"name": "新生儿喂养指导", "description": "新生儿喂养方法指导", "duration_minutes": 40, "price": 280}
        ]
    },
    {
        "category": "健康检查",
        "description": "母婴健康检查服务",
        "items": [
            {"name": "产后42天检查", "description": "产后42天的全面检查", "duration_minutes": 60, "price": 500},
            {"name": "新生儿体检", "description": "新生儿的全面体检", "duration_minutes": 45, "price": 350},
            {"name": "母乳成分分析", "description": "母乳成分的分析", "duration_minutes": 30, "price": 400},
            {"name": "微量元素检测", "description": "微量元素的检测", "duration_minutes": 20, "price": 250},
            {"name": "骨密度检测", "description": "骨密度的检测", "duration_minutes": 20, "price": 300}
        ]
    },
    {
        "category": "营养指导",
        "description": "母婴营养指导服务",
        "items": [
            {"name": "月子餐营养指导", "description": "月子餐的营养搭配指导", "duration_minutes": 60, "price": 450},
            {"name": "母乳喂养指导", "description": "母乳喂养的方法指导", "duration_minutes": 40, "price": 300},
            {"name": "产后营养补充", "description": "产后营养补充建议", "duration_minutes": 30, "price": 250},
            {"name": "新生儿营养评估", "description": "新生儿营养状况评估", "duration_minutes": 30, "price": 280},
            {"name": "体重管理咨询", "description": "产后体重管理咨询", "duration_minutes": 45, "price": 350}
        ]
    },
    {
        "category": "心理咨询",
        "description": "母婴心理咨询服务",
        "items": [
            {"name": "产后抑郁筛查", "description": "产后抑郁的筛查", "duration_minutes": 40, "price": 300},
            {"name": "产后心理疏导", "description": "产后心理问题的疏导", "duration_minutes": 60, "price": 500},
            {"name": "亲子关系指导", "description": "亲子关系的建立指导", "duration_minutes": 50, "price": 400},
            {"name": "家庭关系调适", "description": "产后家庭关系的调适", "duration_minutes": 60, "price": 450},
            {"name": "压力管理咨询", "description": "产后压力管理咨询", "duration_minutes": 45, "price": 350}
        ]
    }
]

def add_mother_baby_services():
    """添加母婴服务分类和项目"""
    try:
        print("开始添加母婴服务分类和项目...")
        
        for service_data in mother_baby_services:
            # 检查服务分类是否已存在
            category = ServiceCategory.query.filter_by(name=service_data["category"]).first()
            if not category:
                # 创建服务分类
                category = ServiceCategory(
                    name=service_data["category"],
                    description=service_data["description"]
                )
                db.session.add(category)
                db.session.flush()
                print(f"创建服务分类: {service_data['category']}")
            else:
                print(f"服务分类已存在: {service_data['category']}")
            
            # 添加服务项目
            for item_data in service_data["items"]:
                # 检查服务项目是否已存在
                item = ServiceItem.query.filter_by(name=item_data["name"]).first()
                if not item:
                    # 创建服务项目
                    item = ServiceItem(
                        name=item_data["name"],
                        description=item_data["description"],
                        category_id=category.id,
                        duration_minutes=item_data["duration_minutes"],
                        price=item_data["price"]
                    )
                    db.session.add(item)
                    print(f"  - 创建服务项目: {item_data['name']}")
                else:
                    print(f"  - 服务项目已存在: {item_data['name']}")
        
        # 提交更改
        db.session.commit()
        print("\n母婴服务分类和项目添加成功！")
        
    except Exception as e:
        db.session.rollback()
        print(f"添加过程中出现错误: {str(e)}")

if __name__ == "__main__":
    with app.app_context():
        add_mother_baby_services()
