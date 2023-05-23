from models import models, schemas
from sqlalchemy.orm import Session 
from helpers import get_db
from fastapi import Depends , status  , APIRouter
from helpers import get_current_user
import product 
router = APIRouter(
    prefix='/products',
    tags=['products']
)

#post new product

@router.post('/create' , status_code=status.HTTP_201_CREATED)
def post_product(products : schemas.ProductSchema, db : Session = Depends(get_db),  current_user: models.UserModel = Depends(get_current_user)):
    return product.create(products, db , current_user)

#get product by id 
@router.get('/product/{pid}' )
def get_specific(pid : int , db : Session = Depends(get_db)  ):
   return product.get_proudct_by_id(pid , db )

#delete product
@router.delete('/product/{pid}' )
def get_specific(pid : int , db : Session = Depends(get_db) , curr_user : models.UserModel = Depends(get_current_user)):
    return product.get_proudct_by_id(pid , db , curr_user )

#update product
@router.patch('/product/{pid}')
def updateProduct(  products : schemas.ProductSchema, pid : int , db : Session = Depends(get_db), current_user : models.UserModel=Depends(get_db) ):
   return  product.update_product(pid , db , current_user, products)
    

#get all products
@router.get('/products')
def allProducts( db : Session = Depends(get_db)):
   return product.get_all_products(db)