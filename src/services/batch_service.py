from flask import jsonify
from src.repository.batch_repository import BatchRepository
from src.tasks import process_batch_message


class BatchService:
    def __init__(self, batch_repository=BatchRepository()):
        self.batch_repository = batch_repository

    def create_batch(self, batch_id, status, piglet_count):
        if batch_id is None or status is None or piglet_count is None:
            return {"message": "Missing required parameters"}, 400

        response = self.batch_repository.create_batch(
            batch_id=batch_id, status=status, piglet_count=piglet_count
        )

        if not response:
            return {"message": "Batch creation failed"}, 500

        process_batch_message.apply_async(
            args=[
                {
                    "action": "create",
                    "batch_id": batch_id,
                    "status": status,
                    "piglet_count": piglet_count,
                }
            ]
        )

        return response.to_dict(), 201

    def list_all_batches_by_status(self, status):
        batches = self.batch_repository.list_all_batches_by_status(status)
        return [batch.to_dict() for batch in batches], 200

    def list_all_batches(self):
        batches = self.batch_repository.list_all_batches()
        return jsonify([batch.to_dict() for batch in batches]), 200

    def update_batch(self, batch_id, piglet_count):
        if batch_id is None or piglet_count is None:
            return {"message": "Missing required parameters"}, 400

        response = self.batch_repository.update_batch(batch_id, piglet_count)
        if not response:
            return {"message": "Batch not found"}, 404

        process_batch_message.apply_async(
            args=[
                {
                    "action": "update",
                    "batch_id": batch_id,
                    "piglet_count": piglet_count,
                }
            ]
        )

        return {"message": "Batch updated successfully!"}, 200

    def delete_batch(self, batch_id):
        batch = self.batch_repository.delete_batch(batch_id)

        if not batch:
            return {"message": "Batch not found"}, 404

        process_batch_message.apply_async(
            args=[
                {
                    "action": "delete",
                    "batch_id": batch_id,
                }
            ]
        )

        return {"message": "Batch deleted successfully!"}, 200
