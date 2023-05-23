from fastapi import APIRouter, Depends, status
import users 
from helpers import get_db
from models import schemas
from sqlalchemy.orm import Session 


router = APIRouter(
    prefix='/users',
    tags =['users']
)

@router.get('/')
def getUsers(db : Session = Depends(get_db)):
    return users.get_all_users(db)

@router.post('/create', status_code=status.HTTP_201_CREATED)
def sign_up(user:schemas.UserSchema, db : Session = Depends(get_db)):
    return users.signup(user , db)

@router.post('/signin')
def sigin(user : schemas.UserSignInSchema, db : Session = Depends(get_db)):
    return users.signin(user , db)


