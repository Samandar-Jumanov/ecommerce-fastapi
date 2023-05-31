from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os 
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends , HTTPException, status
from models import models
from sqlalchemy.orm import Session
import jwt 
from fastapi.security import OAuth2PasswordBearer
from typing import Tuple 
load_dotenv()
DB = os.environ.get('DB')
secret = os.environ.get('secret')
algorithm = os.environ.get('algo')
engine = create_engine(DB)
SessionLocal = sessionmaker(autoflush=False , autocommit = False  , bind = engine)


def get_db():
   db = SessionLocal()
   try:
       yield db
       print('Connnected to db')
   finally:
       db.close()

Base = declarative_base()

pswd_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])

class Password:

    @staticmethod
    def hash(password):
        return pswd_context.hash(password)
    
    @staticmethod
    def verify(plain_password, encrypted_password):
        return pswd_context.verify(plain_password, encrypted_password)

#Token generation
def token_res(token: str):
    return {'access_token': token}

def decode(token: str):
    try:
        decoded_token = jwt.decode(token, secret, algorithms=[algorithm])
        expiry_date = datetime.fromtimestamp(decoded_token['expiry_date'])
        if expiry_date > datetime.now():
            return 'Invalid token'
    except:
        pass

def sign_token(userId: int) -> Tuple[str, int]:
    expiry_date = datetime.now() + timedelta(minutes=20)
    payload = {
        'userId': userId,
        'expiry_date': expiry_date.timestamp()
    }
    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token, 200

#auth 
oauth2 = OAuth2PasswordBearer(tokenUrl='/users/signin')

def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    try:
        payload = decode(token)
        userId = payload['userId']
        user = db.query(models.UserModel).filter(models.UserModel.id == userId).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user')


