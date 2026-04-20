from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.schemas import UserCreate, UserOut, Token
from app.services import user as user_service
from app.services.email import send_activation_email
from app.api.deps import oauth2_scheme
from typing import List

from sqlalchemy import select
from app.models.models import User
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Passwords do not match"
        )
    existing_user = await user_service.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this email already exists"
        )
    
    new_user = await user_service.create_user(db, user_data)
    
    
    send_activation_email.delay(new_user.email, new_user.activation_key)
    
    return new_user




@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    # 1. Ищем пользователя
    user = await user_service.get_user_by_email(db, form_data.username)
    
    # 2. Проверяем существование и пароль
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Генерируем токен
    access_token = create_access_token(subject=user.email)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserOut)
async def get_me(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme) # Вот эта строка заставит кнопку появиться!
):
    # Пока просто для теста возвращаем заглушку или ищем юзера
    from app.core.security import jwt, settings
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user = await user_service.get_user_by_email(db, payload.get("sub"))
    return user


 # Убедись, что в UserOut есть поле activation_key

@router.get("/users/list", response_model=List[UserOut])
async def get_users_list(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users