from flask import Blueprint, jsonify, request
from src.services.batch_service import BatchService

batches_bp = Blueprint("batches", __name__)


@batches_bp.route("/", methods=["POST"])
def create_batch():
    params = request.get_json()
    batch_id = params.get("batch_id")
    status = params.get("status")
    piglet_count = params.get("piglet_count")

    batch_service = BatchService()
    response = batch_service.create_batch(
        batch_id=batch_id, status=status, piglet_count=piglet_count
    )

    return response


@batches_bp.route("/", methods=["GET"])
def get_all_batches():
    status = request.args.get("status")

    if status:
        batches = BatchService()
        response = batches.list_all_batches_by_status(status)
        
        return response

    batches = BatchService()
    response = batches.list_all_batches()

    return response


@batches_bp.route("/<batch_id>", methods=["PATCH"])
def update_specific_batch(batch_id):

    data = request.get_json()
    piglet_count = data.get("piglet_count")
    
    batch_service = BatchService()
    response = batch_service.update_batch(batch_id, piglet_count)

    return response


@batches_bp.route("/<batch_id>", methods=["DELETE"])
def delete_specific_batch(batch_id):

    batch_service = BatchService()
    response, status_code = batch_service.delete_batch(batch_id)

    return jsonify(response), status_code
