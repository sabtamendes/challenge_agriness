from celery import Celery
import os
import dotenv

dotenv.load_dotenv()

def make_celery(app=None):
    broker_url = app.config['CELERY_BROKER_URL'] if app else os.getenv('CELERY_BROKER_URL', 'pyamqp://guest@rabbitmq:5672//')
    result_backend = app.config['CELERY_RESULT_BACKEND'] if app else os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
    
    celery = Celery(
        __name__,
        broker=broker_url,
        backend=result_backend
    )
    
    celery.conf.update(
        broker_url=broker_url,
        result_backend=result_backend,
        broker_connection_retry_on_startup=True
    )

    if app:
        celery.conf.update(app.config)
    return celery

celery = make_celery()


import src.tasks 

celery.conf.update({
    'task_default_queue': 'default',
    'task_queues': {
        'default': {
            'exchange': 'default',
            'exchange_type': 'direct',
            'routing_key': 'default',
            'durable': True,
        },
    },
})
