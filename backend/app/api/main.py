from fastapi import APIRouter

from app.api.routes import items, login, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(items.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(items.router, prefix="/companies", tags=["companies"])
api_router.include_router(items.router, prefix="/orders", tags=["orders"])
api_router.include_router(items.router, prefix="/portfolios", tags=["portfolios"])
api_router.include_router(items.router, prefix="/trades", tags=["trades"])
