from fastapi import APIRouter

from .routes import cv_routes, cover_letter_routes, user_routes

api_router = APIRouter()

api_router.include_router(user_routes.router)
api_router.include_router(cv_routes.router)
api_router.include_router(cover_letter_routes.router) 