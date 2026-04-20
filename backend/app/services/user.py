import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import User
from app.schemas.schemas import UserCreate
from app.core.security import get_password_hash

async def create_user(db: AsyncSession, user_in: UserCreate):
    hashed_pass = get_password_hash(user_in.password)
    act_key = secrets.token_hex(16) 
    
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_pass,
        activation_key=act_key, 
        is_active=False
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


class UserService:

    @staticmethod
    async def refresh_user_key(db: AsyncSession, user: User):
        # 1. Генерируем новый уникальный ключ
        new_key = str(uuid.uuid4())
        
        # 2. Обновляем пользователя
        user.activation_key = new_key
        user.is_active = False  # Если нужно деактивировать до подтверждения
        
        await db.commit()
        await db.refresh(user)

        # 3. Отправляем задачу в Celery (раскомментируй, когда настроишь Celery)
        # from app.core.tasks import send_email_task
        # send_email_task.delay(user.email, new_key)
        
        return user