from fastapi import FastAPI
from models import models
from helpers import  engine, get_db
import users_router
import product_router
import stripe


app = FastAPI()


models.Base.metadata.create_all(engine)
get_db()

app.include_router(users_router.router)
app.include_router(product_router.router)
app.include_router(stripe.stripe_router)


