from pydantic import BaseModel
import datetime
# Product
class Product(BaseModel):
    id : int
    name: str
    price: str
    brand: str

class CreateProduct(BaseModel):
    name:str
    price:str
    brand:str
    is_active:bool
    quantity:int
    category:str
    
    
# Category    
class Category(BaseModel):
    id:int
    name:str
    products: list[Product]

class CreateCategory(BaseModel):
    name: str
    

# Inventory    
class Inventory(BaseModel):
    id:int
    product_id:int
    quantity:int

class CreateInventory(BaseModel):
    product_id:int
    quantity:int 

class UpdateInventory(BaseModel):
    id:int
    product_id:int
    quantity:int    

# Sales
class Sales(BaseModel):
    id:int
    product_id:int
    quantity:int
    sale_date:datetime
    revenue:float
    class Config:
        arbitrary_types_allowed = True

# Datetime model
class SalesFilter(BaseModel):
    start_date: datetime
    end_date: datetime
    category: str
    product: str
    
    class Config:
        arbitrary_types_allowed = True

# Revenue Compare Model
class RevenueCompare(BaseModel):
    first_start_date: datetime
    first_end_date: datetime
    first_category: str
    second_start_date: datetime
    second_end_date: datetime
    second_category: str
    
    class Config:
        arbitrary_types_allowed = True

class RevenueModelComparisonResponse(BaseModel):
    First_TotalArticlesSold: str
    First_TotalRevenueGenerated: str
    Second_TotalArticlesSold: str
    Second_TotalRevenueGenerated: str
        
# Revenue model
class RevenueModel(BaseModel):
    TotalArticlesSold: str
    TotalRevenueGenerated: str