import logging
from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel, ValidationError
from typing import Annotated

import auth
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from auth import get_current_user


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)

# Pydantic model for the product data
class ProductBase(BaseModel):
    title:str
    description:str
    price:float

# Dependency to get the database session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

'''@app.get("/",status_code=status.HTTP_200_OK)
def user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    return {"User":user}'''


# API endpoint to create a new product
@app.post("/products/",status_code=status.HTTP_201_CREATED)
def create_product(user:user_dependency,product:ProductBase,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    else:
        try:
            db_product=models.Product(**product.dict())
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(e))
        db.add(db_product)
        db.commit()
        logger.info("Created product with ID: %s", db_product.id)
        return db_product

# API endpoint to retrieve all products
@app.get("/products/",status_code=status.HTTP_200_OK)
def read_products(user:user_dependency,db:db_dependency,skip:int=0,limit:int=10):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    else:
        product=db.query(models.Product).offset(skip).limit(limit).all()
        return product

# API endpoint to retrieve a specific product by ID
@app.get("/products/{product_id}",status_code=status.HTTP_200_OK)
def read_product(user:user_dependency,product_id:int,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    else:
        product=db.query(models.Product).filter(models.Product.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Product not found')
        return product

# API endpoint to update a product by ID
@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
def update_product(user:user_dependency,product_id: int, product_data: ProductBase, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    else:
        existing_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if existing_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    # Update the existing product with the new data
        existing_product.title = product_data.title
        existing_product.description = product_data.description
        existing_product.price = product_data.price
        db.commit()
        logger.info("Updated product with ID: %s", product_id)
        return existing_product


# API endpoint to delete a product by ID
@app.delete("/products/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(user:user_dependency,product_id: int, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    else:
        product=db.query(models.Product).filter(models.Product.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Product not found')
        db.delete(product)
        db.commit()
        logger.info("Deleted product with ID: %s", product_id)
        return {"message":"Product deleted"}
