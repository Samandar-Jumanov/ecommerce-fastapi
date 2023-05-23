from pydantic import BaseModel, EmailStr, datetime_parse
from datetime import datetime

from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    joined_date: datetime
   


class UserOut(BaseModel):
    username : str 
    email : str 
    joined_date : datetime 

    class Config:
        orm_mode = True 




class UserSignInSchema(BaseModel):
    username : str 
    password : str 


class UserSingInSchemaOut(BaseModel):
    username : str
    class Config:
        orm_mode = True 


class ProductSchema(BaseModel):
    product_name : str
    product_image : str 
    product_price :int
    product_description: str 
    owner_location : str 
    added_date : datetime
    owner_id : int 



class Stripe(BaseModel):
    stripe_id : int  
    amount : str 
    currency : str 
    description : str 
    paid : datetime 