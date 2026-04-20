import logging
from app.core.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="send_activation_email")
def send_activation_email(email: str, key: str):
    logger.info(f"🚀 [CELERY] Начинаем отправку письма для: {email}")
    
    # Здесь могла бы быть логика smtplib
    # Сейчас мы просто имитируем задержку и выводим ключ
    import time
    time.sleep(2) 
    
    logger.info(f"✅ [CELERY] Письмо отправлено! Ключ активации: {key}")
    return {"status": "success", "to": email}