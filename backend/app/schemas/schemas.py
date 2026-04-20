from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# --- Схемы для User ---

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    password_confirm: str # Нужно для валидации при регистрации

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    activation_key: Optional[str] = None
    # Позволяет Pydantic читать данные прямо из объектов SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

# --- Схемы для Virtual Machine (Proxy) ---

class VMBase(BaseModel):
    name: str
    host: str
    port: int
    protocol: str = "socks5"

class VMOut(VMBase):
    id: int
    is_active: bool
    current_user_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class VMUpdate(BaseModel):
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    is_active: Optional[bool] = None

class VMCreate(VMBase):
    pass
# --- Схемы для Аутентификации ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Схема для Активации (Десктопное приложение) ---

class ActivationRequest(BaseModel):
    key: str


# Базовая схема для VM (то, что общее)
class VMBase(BaseModel):
    name: str
    host: str
    port: int
    protocol: str = "socks5"
    is_active: bool = True

# Схема для создания VM через API (например, админом)
class VMCreate(VMBase):
    pass

# Схема для ответа API
class VMOut(VMBase):
    id: int
    current_user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# Схема для запроса активации прокси из десктопного приложения
class ProxyActivationRequest(BaseModel):
    activation_key: str