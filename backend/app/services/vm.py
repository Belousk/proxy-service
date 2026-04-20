from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.models import VirtualMachine, User
from fastapi import HTTPException, status

async def activate_vm_with_key(db: AsyncSession, activation_key: str, user_id: int):
    # 1. Проверяем, существует ли такой ключ у текущего пользователя
    user_query = await db.execute(
        select(User).where(and_(User.id == user_id, User.activation_key == activation_key))
    )
    user = user_query.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid activation key or key already used"
        )

    # 2. Ищем свободную виртуалку (где нет хозяина и она активна)
    vm_query = await db.execute(
        select(VirtualMachine).where(
            and_(VirtualMachine.current_user_id == None, VirtualMachine.is_active == True)
        ).limit(1)
    )
    vm = vm_query.scalars().first()
    
    if not vm:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="no_free_vms"
        )

    # 3. Привязываем VM к юзеру и «сжигаем» ключ
    vm.current_user_id = user.id
    user.activation_key = None  # Ключ одноразовый
    
    await db.commit()
    await db.refresh(vm)
    return vm



async def get_free_vm(db: AsyncSession):
    """Находит первую виртуалку, где current_user_id IS NULL и она активна"""
    query = select(VirtualMachine).where(
        and_(
            VirtualMachine.current_user_id == None,
            VirtualMachine.is_active == True
        )
    ).limit(1)
    
    result = await db.execute(query)
    return result.scalars().first()

async def activate_proxy_by_key(db: AsyncSession, activation_key: str):
    """Логика активации ключа и привязки прокси"""
    # 1. Ищем пользователя по ключу
    user_query = select(User).where(User.activation_key == activation_key)
    user_result = await db.execute(user_query)
    user = user_result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Неверный или уже использованный ключ активации"
        )
    
    # 2. Проверяем, нет ли у пользователя уже привязанной VM
    existing_vm_query = select(VirtualMachine).where(VirtualMachine.current_user_id == user.id)
    existing_vm_result = await db.execute(existing_vm_query)
    if existing_vm_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас уже есть активное подключение"
        )
    
    # 3. Ищем свободную VM
    vm = await get_free_vm(db)
    if not vm:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="no_free_vms" # Код ошибки из ТЗ для WebSocket/Frontend
        )
    
    # 4. Привязываем VM к пользователю и аннулируем ключ (одноразовый по ТЗ)
    vm.current_user_id = user.id
    user.activation_key = None # Делаем ключ невалидным
    
    await db.commit()
    await db.refresh(vm)
    return vm