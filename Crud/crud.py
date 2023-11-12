from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models,schemas
from datetime import datetime
# Product
def get_products(db: Session, skip:int=0,limit:int=100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product_by_name(db: Session, name:str):
    return db.query(models.Product).filter(models.Product.name==name).first()

def get_product_by_category(db:Session,category_id:int):
    return db.query(models.Product.id).filter(models.Product.category_id == category_id).all()

def create_product(db:Session,product:schemas.CreateProduct):
    created_product = models.Product(name=product.name,brand=product.brand,price=product.price,is_active=product.is_active,category_id=product.category)
    db.add(created_product)
    db.commit()
    db.refresh(created_product)
    return created_product

# Category
def get_categories(db:Session,skip:int=0,limit=100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category(db:Session,name:str):
    return db.query(models.Category).filter(models.Category.name==name).first()

def create_category(db:Session,category:schemas.CreateCategory):
    created_category = models.Category(name=category.name)
    db.add(created_category)
    db.commit()
    db.refresh(created_category)
    return created_category

# Inventory
def get_inventory(db:Session,product_id:str):
    return db.query(models.Inventory).filter(models.Inventory.product_id==product_id).all()

def get_low_inventory_alerts(db:Session):
    return db.query(models.Inventory).filter(models.Inventory.quantity < 50).all()

def create_inventory(db:Session,inventory:schemas.CreateInventory):
    created_inventory = models.Inventory(product_id=inventory.product_id,quantity=inventory.quantity)
    db.add(created_inventory)
    db.commit()
    db.refresh(created_inventory)
    return created_inventory

def update_inventory(db:Session,inventory:schemas.UpdateInventory):
    existing_inventory = db.query(models.Inventory).filter(models.Inventory.id==inventory.id).first()
    if existing_inventory:
        existing_inventory.quantity = inventory.quantity
        db.commit()
        db.refresh(existing_inventory)
    return existing_inventory    

# Sales
def get_sales_data(db:Session):
    return db.query(models.Sales).all()

def get_sales_by_date_range(db:Session,start_date:datetime,end_date:datetime):
    return db.query(models.Sales).filter(
    and_(models.Sales.sale_date > start_date, models.Sales.sale_date < end_date)
    ).all()
    
def get_sales_by_product(db:Session,product_ids:list[int]):
    flat_product_ids = [product_id for sublist in product_ids for product_id in sublist]

    return (
        db.query(models.Sales)
        .filter(models.Sales.product_id.in_(flat_product_ids))
        .all()
    )






