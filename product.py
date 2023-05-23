from models import models, schemas
from fastapi import HTTPException, status, Depends, UploadFile, File, Request
from sqlalchemy.orm import Session 
from datetime import datetime 
from helpers import get_current_user
from dotenv import load_dotenv
import shutil
import uuid
id = uuid.uuid4()
load_dotenv()
import os
from datetime import datetime

 


def create(products: schemas.ProductSchema, db: Session, current_user: models.UserModel = Depends(get_current_user), file: UploadFile= File(...)):


    filename  = str(id)
    with open(f'images{filename}') as buffer:
        shutil.copyfileobj(file.file , buffer ) 

    new_product = models.Product(
        product_name=products.product_name,
        product_price=products.product_price,
        product_image=filename,
        product_description=products.product_description,
        added_date=datetime.now(),
        owner_id=current_user.id,
        owner_location=products.owner_location
    )

    
   #
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)




def update_product(pid: int, products: schemas.ProductSchema, db: Session, current_user:int):

    product = db.query(models.Product).filter(models.Product.id == pid).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to update this product")

    product.product_name = products.product_name
    product.product_price = products.product_price
    product.product_description = products.product_description
    product.owner_location = products.owner_location

    try:
        db.commit()
        db.refresh(product)
        return product
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)
    


def get_proudct_by_id(pid : int , db : Session):
    product = db.query(models.Product).filter(models.Product.id == pid).first()
    return product


def delete_product( pid : int , db : Session , curr_user : Depends(get_current_user)):
    user = curr_user.id 
    if not user:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail='Invalid user')
    deletable = db.query(models.Product).filter(models.Product.id == pid).first()
    if not deletable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid product')
    db.delete(deletable)
    db.commit()
    return 'Deleted succesfuly'
    



def get_all_products(db : Session):
    products = db.query(models.Product).all()
    try:
        return products
    except  Exception as error:
        return HTTPException(status_code=500, detail=error)
    
