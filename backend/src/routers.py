from fastapi import APIRouter

from src.tree.api import router as tree_router

api_router = APIRouter()


api_router.include_router(tree_router, prefix='/trees', tags=['trees'])
