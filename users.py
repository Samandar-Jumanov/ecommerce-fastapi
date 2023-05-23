from sqlalchemy.orm import Session 
from models import schemas , models
from datetime import datetime
from helpers import Password, sign_token
from fastapi import HTTPException, status


def get_all_users(db : Session):
    all_users =  db.query(models.UserModel).all()
    try:
        return all_users
    except Exception as error:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = error)
    



def signup(user: schemas.UserSchema, db: Session):
    try:
        new_user = models.UserModel(
            username=user.username,
            email=user.email,
            password=Password.hash(user.password),
            joined_date = datetime.now()
        )

        #make a token
        token = sign_token(new_user.id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return { "user":new_user ,"token": token}
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)



def signin(user: schemas.UserSignInSchema , db : Session):
    available_user = db.query(models.UserModel).filter(models.UserModel.username == user.username).first()
    available_password = Password.verify(user.password , available_user.password)
    token = sign_token(available_user.id)
    if not available_user or not available_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cannot find user for the provided email or password')
    
    return {'User' : available_user , "token":token}





