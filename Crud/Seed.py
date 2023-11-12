from sqlalchemy.orm import Session
from .models import Product,Category,Inventory,Sales

def seed_data(db: Session):
    products = [
        {"name": "Nike Jacket", "brand": "NIKE","price":"2500$","is_active":True,"category_id":"2"},
        {"name": "Black Hoodie", "brand": "Adidas","price":"650$","is_active":True,"category_id":"1"},
        {"name": "Yellow shirt", "brand": "Polo","price":"50$","is_active":True,"category_id":"5"},
        {"name": "Black Sweatshirt", "brand": "Nike","price":"200$","is_active":True,"category_id":"3"},
        {"name": "Blue casual", "brand": "Polo","price":"150$","is_active":True,"category_id":"4"},
        {"name": "Red Casual", "brand": "Lacoste","price":"250$","is_active":True,"category_id":"4"},
        {"name": "White Hoodie", "brand": "Puma","price":"350$","is_active":True,"category_id":"1"},
        {"name": "Denim Jacket", "brand": "Denim","price":"450$","is_active":True,"category_id":"2"}
        ]
    
    categories = [
        {"name":"Hoodies"},
        {"name":"Jackets"},
        {"name":"SweatShirts"},
        {"name":"Casuals"},
        {"name":"T-Shirts"},
    ]
    
    inventory = [
        {"product_id":1,"quantity":100},
        {"product_id":2,"quantity":550},
        {"product_id":3,"quantity":900},
        {"product_id":4,"quantity":200},
        {"product_id":5,"quantity":800},
        {"product_id":6,"quantity":300},
        {"product_id":7,"quantity":500},
        {"product_id":8,"quantity":400}
    ]
    
    sales = [
        {"product_id":1,"quantity":4,"revenue":1000.0},
        {"product_id":1,"quantity":10,"revenue":2500.0},
        {"product_id":2,"quantity":2,"revenue":1300.0},
        {"product_id":2,"quantity":4,"revenue":2600.0},
        {"product_id":3,"quantity":25,"revenue":1750.0},
        {"product_id":3,"quantity":50,"revenue":2500.0},
        {"product_id":4,"quantity":6,"revenue":1200.0},
        {"product_id":4,"quantity":9,"revenue":1800.0},
        {"product_id":5,"quantity":4,"revenue":600.0},
        {"product_id":5,"quantity":6,"revenue":900.0},
        {"product_id":6,"quantity":4,"revenue":1000.0},
        {"product_id":6,"quantity":8,"revenue":2000.0},
        {"product_id":7,"quantity":10,"revenue":2500.0},
        {"product_id":7,"quantity":4,"revenue":1400.0},
        {"product_id":8,"quantity":4,"revenue":1800.0},
        {"product_id":8,"quantity":2,"revenue":900.0},
    ]

    for item in categories:
        db_item = Category(**item)
        db.add(db_item)
    
    db.commit()
    db.refresh(db_item)
    
    for item in products:
        db_item = Product(**item)
        db.add(db_item)
    db.commit()
    
    for item in inventory:
        db_item = Inventory(**item)
        db.add(db_item)
    
    for item in sales:
        db_item = Sales(**item)
        db.add(db_item)
    db.commit()
