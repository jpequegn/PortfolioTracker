from fastapi import APIRouter
from app.api.endpoints import portfolios, assets, holdings, transactions

api_router = APIRouter()
api_router.include_router(portfolios.router, prefix="/portfolios", tags=["portfolios"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(holdings.router, prefix="/holdings", tags=["holdings"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])