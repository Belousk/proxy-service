from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user # Твоя функция проверки JWT
from app.services.user import UserService
from app.models.models import User

router = APIRouter()

@router.post("/refresh-key")
async def refresh_key(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        updated_user = await UserService.refresh_user_key(db, current_user)
        return {
            "status": "success",
            "message": "Новый ключ сгенерирован и отправлен на почту",
            "new_key": updated_user.activation_key # Можно скрыть, если только через почту
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении ключа: {str(e)}"
        )