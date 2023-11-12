# E-Commerce API

This is the backend API for an e-commerce website built in FastAPI and Python. It provides various endpoints to manage products, inventory, and sales data.

## Installation
1. **Database Configuration**
Change the database connection string in the file named database.py so you can connect to your database accordingly. You can also create an empty database and then run the project with updated connection string so it should be able to create new tables in that database.

2. **Install python libraries**
Install the python libraries by going into the directory where requirements.txt file is located and running the following command: pip install -r "requirements.txt

2. **Run the project**
In the app directory, where the main.py file is location run the following command to get the project running and then hit the /seed-data endpoint: python -m uvicorn main:app --reload

## Endpoints

1. **Seed Data**

   - Endpoint: `/seed-data`
   - Method: `POST`
   - Description: There is a script.py file in the directory which contains the data that can be seeded into the database. So after successfully running the project you can hit this endpoint to seed data into the database.

2. **Get Products**

   - Endpoint: `/products`
   - Method: `GET`
   - Description: This endpoint retrieves a list of products from the database.

3. **Create Product**

   - Endpoint: `/products`
   - Method: `POST`
   - Description: This endpoint is used to register new product into the database.

4. **Update Inventory**

   - Endpoint: `/update-inventory`
   - Method: `PUT`
   - Description: This endpoint updates the inventory for a product, so we can manage the quantity increase or decrease of products via this endpoint.

5. **Low Inventory Alerts**

   - Endpoint: `/low-inventory-alerts`
   - Method: `GET`
   - Description: This endpoint provides us with the products that have low inventory left. Currently it is set to 50 but it can be changed as well.

6. **Get Inventory By Product**

   - Endpoint: `/inventory/{product_id}`
   - Method: `GET`
   - Description: Retrieves inventory details for a specific product.

7. **Get Sales Data**

   - Endpoint: `/sales`
   - Method: `GET`
   - Description: Retrieves overall sales data.

8. **Get Sales by Filter**

   - Endpoint: `/sales/filter`
   - Method: `GET`
   - Description: Retrieves sales data based on specified filters such as sales for a specific product, category or during a specific time perido.

9. **Get Revenue**

   - Endpoint: `/revenue`
   - Method: `GET`
   - Description: Retrieves overall revenue data with type as a parameter. You can pass different values ("Daily","Weekly","Monthly","Yearly") as the parameter to get the revenue in that time period.

10. **Comparing Revenue**

    - Endpoint: `/compare-revenue`
    - Method: `GET`
    - Description: Compares revenue across different periods and categories. We'll provide the start and end data for both periods or Both categories and it will provide us with revenue of both these filters.

## Database Schema

### Product

- `name`: Name of the product.
- `brand`: Brand of the product.
- `price`: Price of the product.
- `category_id`: Foreign key referencing the `Category` table.
- `is_active`: Indicates whether the product is active.

### Category

- `name`: Name of the category.
- `products`: Relationship with the `Product` table.

### Inventory

- `product_id`: Foreign key referencing the `Product` table.
- `quantity`: Quantity of the product in inventory.

### Sales

- `quantity`: Quantity of the product sold.
- `product_id`: Foreign key referencing the `Product` table.
- `revenue`: Revenue generated from the sale.
- `sales_date`: Date of the sale.

Feel free to expand on each section, provide more details, and add examples as needed. Ensure that the information is up-to-date as your project evolves.
