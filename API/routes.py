# api/routes.py
from fastapi import APIRouter, HTTPException

router = APIRouter()

ACCESS_TOKEN = ""


@router.post("/token")
async def get_token():
    # Логика получения токена
    # Вернуть токен или ошибку
    return {"access_token": ACCESS_TOKEN}


@router.get("/limits")
async def get_limits():
    # Логика получения дневных лимитов
    # Вернуть лимиты или ошибку
    return {"daily_limits": "1000"}


@router.get("/resumes")
async def fetch_resumes(params: dict):
    resumes = []
    return resumes
