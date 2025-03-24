from celery import Celery
from app.config import CELERY_BROKER_URL

celery = Celery('app', broker=CELERY_BROKER_URL)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_expires=3600,
)