from fastapi import FastAPI, HTTPException,Depends
from typing import List
from Crud import crud,models,schemas
from Crud.database import SessionLocal,engine
from sqlalchemy.orm import Session
from Crud.Seed import seed_data
from datetime import datetime,timedelta
from dateutil import parser


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/seed-data")
def seed_datat(db: Session = Depends(get_db)):
    seed_data(db)
    return {"message": "Data seeded successfully"}
        
@app.get("/products",response_model=list[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    products = crud.get_products(db,0,100)
    return products

@app.post("/product/", response_model=schemas.Product)
def create_product(product: schemas.CreateProduct, db: Session = Depends(get_db)):
    category  = crud.get_category(db,product.category)
    if category:
        product.category = category.id
    else:
        created_category = schemas.CreateCategory(name=product.category)
        product.category = crud.create_category(db,created_category).id
    created_product =  crud.create_product(db=db, product=product)
    created_inventory = crud.create_inventory(db=db,inventory=schemas.CreateInventory(quantity=product.quantity,product_id=created_product.id))
    return created_product

@app.put("/update-inventory",response_model=schemas.Inventory)
def update_inventory(inventory:schemas.UpdateInventory,db: Session = Depends(get_db)):
    updated_inventory = crud.update_inventory(db=db,inventory=inventory)
    return updated_inventory

@app.get("/low-inventory",response_model=list[schemas.Inventory])
def get_low_inventory(db:Session = Depends(get_db)):
    return crud.get_low_inventory_alerts(db=db)

@app.get("/get-inventory-by-product",response_model=list[schemas.Inventory])
def get_inventory_by_product(name:str,db:Session = Depends(get_db)):
    product = crud.get_product_by_name(db=db,name = name)
    return crud.get_inventory(db=db,product_id = product.id)

@app.get("/get-sales-data",response_model=list[schemas.Sales])
def get_sales(db:Session = Depends(get_db)):
    return crud.get_sales_data(db=db)

@app.post("/get-sales-by-filter",response_model=list[schemas.Sales])
def get_sales_from_dates(filters:schemas.SalesFilter,db:Session = Depends(get_db)):
    sales = []
    if filters.start_date and filters.end_date != "":
        sales_by_date = crud.get_sales_by_date_range(db=db,start_date=filters.start_date,end_date=filters.end_date)
        sales = sales_by_date
    if filters.product != "":
        product = crud.get_product_by_name(db=db,product=filters.product)
        sales_by_product = crud.get_sales_by_product(db=db,product_ids=[product.id])
        if sales == []:
            sales = sales_by_product
        else:
            sales = list(set(sales)&set(sales_by_product))
    if filters.category != "":
        category = crud.get_category(db=db,name=filters.category)
        product_ids = crud.get_product_by_category(db=db,category_id=category.id)
        sales_by_category = crud.get_sales_by_product(db=db,product_ids=product_ids)
        if sales == []:
            sales = sales_by_category
        else:
            sales = list(set(sales)&set(sales_by_category))
    return sales
    
@app.post("/get-revenue",response_model=schemas.RevenueModel)
def get_revenue(type: str,db : Session = Depends(get_db)):
    if type.lower() == "daily":
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=1)
    elif type.lower() == "weekly":
        start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
        end_date = start_date + timedelta(days=6)
    elif type.lower() == "monthly":
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = (start_date + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
    elif type.lower() == 'yearly':
        start_date = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    else:
        start_date = datetime.now()
        end_date = datetime.now()
    sales = crud.get_sales_by_date_range(db=db,start_date=start_date,end_date=end_date)
    total_quantity = 0
    total_revenue = 0.0
    for sale in sales:
        total_quantity += sale.quantity
        total_revenue += sale.revenue
    return schemas.RevenueModel(TotalArticlesSold = str(total_quantity),TotalRevenueGenerated="$"+str(total_revenue))

@app.post("/comparing-revenue",response_model=schemas.RevenueModelComparisonResponse)
def compare_revenue(filters:schemas.RevenueCompare,db:Session = Depends(get_db)):
    first_sales = []
    second_sales = []
    # Getting data for first set of parameters
    if filters.first_start_date and filters.first_end_date != "":
        sales_by_date = crud.get_sales_by_date_range(db=db,start_date=filters.first_start_date,end_date=filters.first_end_date)
        first_sales = sales_by_date
    if filters.first_category != "":
        category = crud.get_category(db=db,name=filters.first_category)
        product_ids = crud.get_product_by_category(db=db,category_id=category.id)
        sales_by_category = crud.get_sales_by_product(db=db,product_ids=product_ids)
        if first_sales == []:
            first_sales = sales_by_category
        else:
            first_sales = list(set(first_sales)&set(sales_by_category))
    
    # Getting data for second set of parameters
    if filters.second_start_date and filters.second_end_date != "":
        sales_by_date = crud.get_sales_by_date_range(db=db,start_date=filters.second_start_date,end_date=filters.second_end_date)
        second_sales = sales_by_date
    if filters.second_category != "":
        category = crud.get_category(db=db,name=filters.second_category)
        product_ids = crud.get_product_by_category(db=db,category_id=category.id)
        sales_by_category = crud.get_sales_by_product(db=db,product_ids=product_ids)
        if second_sales == []:
            second_sales = sales_by_category
        else:
            second_sales = list(set(second_sales)&set(sales_by_category))
    total_quantity_first = 0
    total_revenue_first = 0.0
    total_quantity_second = 0
    total_revenue_second = 0.0
    for sale in first_sales:
        total_quantity_first += sale.quantity
        total_revenue_first += sale.revenue
    for sale in second_sales:
        total_quantity_second += sale.quantity
        total_revenue_second += sale.revenue
    return schemas.RevenueModelComparisonResponse(First_TotalArticlesSold = str(total_quantity_first),First_TotalRevenueGenerated="$"+str(total_revenue_first),Second_TotalArticlesSold = str(total_quantity_second),Second_TotalRevenueGenerated="$"+str(total_revenue_second))

    