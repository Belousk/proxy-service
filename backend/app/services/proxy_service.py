from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import VirtualMachine
from app.schemas.schemas import VMCreate, VMUpdate

class ProxyService:
    @staticmethod
    async def create_server(db: AsyncSession, vm_data: VMCreate):
        # Здесь могла быть сложная логика:
        # Например, проверка доступности IP, выбор порта или лимитов
        new_vm = VirtualMachine(
            **vm_data.model_dump(),
        )
        db.add(new_vm)
        await db.commit()
        await db.refresh(new_vm)
        return new_vm

    @staticmethod
    async def get_all_servers(db: AsyncSession):
        result = await db.execute(select(VirtualMachine).order_by(VirtualMachine.id))
        return result.scalars().all()
    
    @staticmethod
    async def update_server(db: AsyncSession, vm_id: int, vm_data: VMUpdate):
        result = await db.execute(select(VirtualMachine).where(VirtualMachine.id == vm_id))
        vm = result.scalar_one_or_none()
        if not vm:
            raise HTTPException(status_code=404, detail="Сервер не найден")
        
        # Обновляем только те поля, которые прислали
        for key, value in vm_data.model_dump(exclude_unset=True).items():
            setattr(vm, key, value)
        
        await db.commit()
        await db.refresh(vm)
        return vm
    

    @staticmethod
    async def delete_server(db: AsyncSession, vm_id: int):
        result = await db.execute(select(VirtualMachine).where(VirtualMachine.id == vm_id))
        vm = result.scalar_one_or_none()
        if not vm:
            raise HTTPException(status_code=404, detail="Сервер не найден")
        
        await db.delete(vm)
        await db.commit()
        return {"detail": "Сервер удален"}

    @staticmethod
    async def activate_proxy(db: AsyncSession, key: str, user_id: int):
        # 1. Ищем пользователя по ключу
        result = await db.execute(
            select(User).where(User.activation_key == key, User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="Неверный ключ или ID пользователя")

        # 2. Ищем свободный сервер
        vm_result = await db.execute(
            select(VirtualMachine).where(VirtualMachine.current_user_id == None)
        )
        vm = vm_result.scalar_one_or_none()

        if not vm:
            raise HTTPException(status_code=503, detail="Нет свободных серверов")

        # 3. Процесс активации
        user.activation_key = None  # Сжигаем ключ
        user.is_active = True
        vm.current_user_id = user.id # Закрепляем сервер за юзером
        
        await db.commit()
        return {"status": "success", "server": vm.name, "host": vm.host}