from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True) 
    hashed_password: Mapped[str] = mapped_column(String(255)) 
    is_active: Mapped[bool] = mapped_column(Boolean, default=True) 
    
    # Ключ активации (одноразовый)
    activation_key: Mapped[Optional[str]] = mapped_column(String(64), unique=True, nullable=True)
    
    # Связь с виртуалкой
    vm = relationship("VirtualMachine", back_populates="current_user", uselist=False)

class VirtualMachine(Base, TimestampMixin):
    __tablename__ = "virtual_machines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    host: Mapped[str] = mapped_column(String(255))
    port: Mapped[int] = mapped_column(Integer)
    protocol: Mapped[str] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    current_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    current_user = relationship("User", back_populates="vm")