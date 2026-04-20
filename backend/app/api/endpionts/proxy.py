from fastapi import APIRouter, Depends, status
from app.services.proxy_service import ProxyService

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.schemas import VMOut, VMCreate, VMUpdate, ProxyActivationRequest
from app.services import vm as vm_service
from app.models.models import User

from typing import List
from app.models.models import VirtualMachine

router = APIRouter()

@router.post("/activate")
async def activate_server(key: str, user_id: int, db: AsyncSession = Depends(get_db)):
    return await ProxyService.activate_proxy(db, key, user_id)

@router.get("/list", response_model=List[VMOut])
async def list_servers(db = Depends(get_db)):
    return await ProxyService.get_all_servers(db)

@router.post("/create", response_model=VMOut, status_code=status.HTTP_201_CREATED)
async def create_server(vm_data: VMCreate, db = Depends(get_db)):
    return await ProxyService.create_server(db, vm_data)

@router.patch("/{vm_id}", response_model=VMOut)
async def update_server(vm_id: int, vm_data: VMUpdate, db = Depends(get_db)):
    return await ProxyService.update_server(db, vm_id, vm_data)

@router.delete("/{vm_id}")
async def delete_server(vm_id: int, db = Depends(get_db)):
    return await ProxyService.delete_server(db, vm_id)