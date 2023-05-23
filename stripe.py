from fastapi import APIRouter, Depends 


stripe_router = APIRouter(
    prefix='/payments'
)


@stripe_router.post('/payment')
def stripe():
    pass 
