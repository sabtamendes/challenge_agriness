from src.models.batch_model import Batch
from src.init_db import db


class BatchRepository:
    def create_batch(self, batch_id, status, piglet_count):
        new_batch = Batch(batch_id=batch_id, status=status, piglet_count=piglet_count)
        db.session.add(new_batch)
        db.session.commit()
        return new_batch

    def list_all_batches_by_status(self, status):
        batches = Batch.query.filter_by(status=status).all()
        return batches

    def list_all_batches(self):
        batches = Batch.query.all()
        return batches

    def update_batch(self, batch_id, piglet_count):
        batch = Batch.query.filter_by(batch_id=batch_id).first()
        if not batch:
            return None
        batch.piglet_count = piglet_count
        db.session.commit()
        return batch

    def delete_batch(self, batch_id):
        batch = Batch.query.filter_by(batch_id=batch_id).first()
        if not batch:
            return None
        db.session.delete(batch)
        db.session.commit()
        return batch
