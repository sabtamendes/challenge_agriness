from src.celery_app import celery
from src.config.redis_config import update_key, delete_key
from src.repository.batch_repository import BatchRepository


@celery.task
def process_batch_message(message: dict):
    from src.main import create_app

    app = create_app()

    with app.app_context():
        action = message.get("action")
        batch_id = message.get("batch_id")
        status = message.get("status")
        piglet_count = message.get("piglet_count")

        if action == "create":
            BatchRepository().create_batch(batch_id, status, piglet_count)
            update_key(batch_id, piglet_count)

        elif action == "update":
            BatchRepository().update_batch(batch_id, piglet_count)
            update_key(batch_id, piglet_count)

        elif action == "delete":
            BatchRepository().delete_batch(batch_id)
            delete_key(batch_id)

        else:
            raise ValueError("Unknown message action")
